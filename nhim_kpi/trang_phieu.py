# -*- coding: utf-8 -*-
"""PHIẾU ĐÁNH GIÁ 120 ĐIỂM – Tự chấm / Cấp trên chấm / Cấp có thẩm quyền xác nhận."""
from tkinter import messagebox

import customtkinter as ctk

from . import tinh_diem as td
from .cau_hinh import PHIEU_NHAP, PHIEU_DA_GUI
from .giao_dien_chung import (F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, BAC_HA, BAC_HA_DAM, XANH,
                              XANH_DAM, VANG, VANG_DAM, TIM, The, nut, CanvasNhim, ti_le)
from .luu_tru import bay_gio

RONG_COT = [50, 430, 80, 90, 120, 120, 120]   # STT | Tiêu chí | Tối đa | Hệ thống | 3 cột chấm


class TrangPhieu(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=NEN)
        self.app = app
        self.o = {}         # (mã tiêu chí, cột) -> CTkEntry
        self.nhan_tong = {}  # (nhóm, cột) -> CTkLabel
        self.phieu = None
        self.ky_id = None

    # ------------------------------------------------------------------
    def lam_moi(self):
        for w in self.winfo_children():
            w.destroy()
        self.o, self.nhan_tong = {}, {}
        kho = self.app.kho
        self.ky_id = self.app.ky_id_dang_chon() or (kho.ds_ky[0]["id"] if kho.ds_ky else None)
        if not self.ky_id:
            ctk.CTkLabel(self, text="Chưa có kỳ mục tiêu nào. Hãy tạo kỳ ở mục 📅 Kỳ mục tiêu trước nhé!",
                         font=F(15), text_color=CHU_NHAT).pack(pady=60)
            return
        self.phieu = kho.lay_phieu(self.ky_id)
        ky = kho.tim_ky(self.ky_id)

        than = ctk.CTkFrame(self, fg_color="transparent")
        than.pack(fill="both", expand=True)
        trai = ctk.CTkScrollableFrame(than, fg_color=NEN, width=int(260))
        trai.pack(side="left", fill="y", padx=(6, 4), pady=4)
        phai = ctk.CTkFrame(than, fg_color="transparent")
        phai.pack(side="left", fill="both", expand=True, padx=(4, 6), pady=4)

        self._ve_thong_tin(trai, ky)
        self._ve_bang(phai)
        self._tinh_lai()

    # ---------------- cột trái: thông tin phiếu ----------------
    def _ve_thong_tin(self, khung, ky):
        nd = self.app.kho.du_lieu["nguoi_dung"]
        self.the_tong = The(khung)
        self.the_tong.pack(fill="x", pady=4)
        self.nhim = CanvasNhim(self.the_tong, 130, THE, "binh_thuong")
        self.nhim.pack(pady=(10, 0))
        self.lbl_diem = ctk.CTkLabel(self.the_tong, text="", font=F(22, True), text_color=CHU)
        self.lbl_diem.pack()
        self.lbl_xl = ctk.CTkLabel(self.the_tong, text="", font=F(12, True), text_color="white", corner_radius=12)
        self.lbl_xl.pack(pady=(2, 4))
        self.lbl_nguon = ctk.CTkLabel(self.the_tong, text="", font=F(11), text_color=CHU_NHAT,
                                      wraplength=int(220 * ti_le(self)))
        self.lbl_nguon.pack(pady=(0, 10))

        for tieu_de, noi_dung in (
                ("👤 Thông tin người đánh giá",
                 f"{nd.get('ho_ten') or '[...] (nhập ở mục ⚙️ Cài đặt)'}\n{nd.get('chuc_vu') or ''}\n{nd.get('don_vi') or ''}"),
                ("📅 Kỳ đánh giá", f"{ky['ten']}\n{ky['loai']} {ky['nam']}"),
                ("🚩 Kỳ mục tiêu liên kết", ky["ten"])):
            t = The(khung)
            t.pack(fill="x", pady=4)
            ctk.CTkLabel(t, text=tieu_de, font=F(13, True), text_color=CHU).pack(anchor="w", padx=12, pady=(10, 2))
            ctk.CTkLabel(t, text=noi_dung.strip(), font=F(12), text_color=CHU_NHAT, justify="left",
                         wraplength=int(220 * ti_le(self))).pack(anchor="w", padx=12, pady=(0, 10))

        # Luồng phê duyệt
        t = The(khung)
        t.pack(fill="x", pady=4)
        ctk.CTkLabel(t, text="🔁 Luồng phê duyệt", font=F(13, True), text_color=CHU).pack(anchor="w", padx=12, pady=(10, 4))
        da_gui = self.phieu["trang_thai"] == PHIEU_DA_GUI
        buoc = [("Tự đánh giá", da_gui),
                ("Cấp trên trực tiếp chấm", td.cot_co_du_lieu(self.phieu, "cap_tren")),
                ("Cấp có thẩm quyền xác nhận", td.cot_co_du_lieu(self.phieu, "tham_quyen"))]
        for i, (ten, xong) in enumerate(buoc, 1):
            ctk.CTkLabel(t, text=f"{'✅' if xong else '⏳'}  {i}. {ten}", font=F(12),
                         text_color=CHU if xong else CHU_NHAT).pack(anchor="w", padx=14, pady=1)
        ctk.CTkLabel(t, text=f"Trạng thái: {self.phieu['trang_thai']}", font=F(12, True),
                     text_color=HONG_DAM).pack(anchor="w", padx=14, pady=(4, 10))

        # Ý kiến trao đổi / chỉ đạo
        t = The(khung)
        t.pack(fill="x", pady=4)
        ctk.CTkLabel(t, text="💬 Ý kiến trao đổi / chỉ đạo", font=F(13, True), text_color=CHU).pack(anchor="w", padx=12, pady=(10, 4))
        for yk in self.phieu.get("y_kien", [])[-6:]:
            ctk.CTkLabel(t, text=f"{yk['thoi_gian']}\n{yk['noi_dung']}", font=F(11), text_color=CHU,
                         fg_color=NEN, corner_radius=10, justify="left", anchor="w",
                         wraplength=int(210 * ti_le(self))).pack(fill="x", padx=10, pady=2)
        self.o_y_kien = ctk.CTkTextbox(t, height=60)
        self.o_y_kien.pack(fill="x", padx=10, pady=4)
        nut(t, "Gửi ý kiến", self._gui_y_kien, mau=XANH_DAM, height=30).pack(padx=10, pady=(0, 10), anchor="e")

    # ---------------- cột phải: bảng tiêu chí ----------------
    def _ve_bang(self, khung):
        ch = self.app.kho.cau_hinh
        khoa_tu_cham = self.phieu["trang_thai"] == PHIEU_DA_GUI

        thanh = ctk.CTkFrame(khung, fg_color="transparent")
        thanh.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(thanh, text="📝  Danh sách tiêu chí đánh giá", font=F(16, True), text_color=CHU).pack(side="left")
        if khoa_tu_cham:
            nut(thanh, "🔓 Mở lại phiếu", self._mo_lai, mau=TIM, mau_chu=CHU).pack(side="right", padx=3)
        else:
            nut(thanh, "📤 Gửi đánh giá", self._gui, mau=BAC_HA_DAM).pack(side="right", padx=3)
        nut(thanh, "💾 Lưu nháp", self._luu_nhap, mau=XANH_DAM).pack(side="right", padx=3)
        if not khoa_tu_cham:
            nut(thanh, "✨ Kế thừa điểm hệ thống", self._ke_thua, mau=VANG, mau_chu=CHU).pack(side="right", padx=3)

        ctk.CTkLabel(khung, text="Ô để trống sẽ tự kế thừa: Tự chấm ← Hệ thống · Cấp trên ← Tự chấm · "
                                 "Thẩm quyền ← Cấp trên.  Ô vàng là ô cá nhân tự chấm.",
                     font=F(11), text_color=CHU_NHAT).pack(anchor="w", pady=(0, 4))

        bang = ctk.CTkScrollableFrame(khung, fg_color=THE, corner_radius=16, border_width=2, border_color="#F3DCD4")
        bang.pack(fill="both", expand=True)
        self.bang = bang
        tieu_de = ["STT", "Tiêu chí chấm điểm", "Điểm tối đa", "Hệ thống đánh giá"] + \
                  [td.TEN_COT[c].replace("Điểm ", "") for c in td.COT_DIEM]
        for j, t in enumerate(tieu_de):
            ctk.CTkLabel(bang, text=t, font=F(12, True), text_color=CHU, fg_color=BAC_HA, corner_radius=8,
                         width=RONG_COT[j], wraplength=int(RONG_COT[j] * ti_le(self)) - 4
                         ).grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
        self._hang = 1
        self.nhan_he_thong = {}   # ô 'Hệ thống' của từng tiêu chí lá
        self.nhan_ht_nhom = {}    # ô 'Hệ thống' của dòng nhóm / tổng

        # ----- Nhóm I -----
        nI = ch["nhom_I"]
        self._dong_nhom("I", nI["ma"], nI["ten"], nI["diem_toi_da"])
        for muc in nI["muc"]:
            toi_da_muc = sum(t["diem_toi_da"] for t in muc["tieu_chi"])
            self._dong_van_ban(muc["ma"], muc["ten"], toi_da_muc, dam=True)
            for tc in muc["tieu_chi"]:
                self._dong_cham(tc["ma"], tc["ma"], tc["ten"], tc["diem_toi_da"], khoa_tu_cham)

        # ----- Nhóm II -----
        nII = ch["nhom_II"]
        self._dong_nhom("II", nII["ma"], nII["ten"], nII["diem_toi_da"])
        mo_ta = nII["giai_thich"] + "\n(Tham khảo: " + "; ".join(nII.get("tieu_chi_tham_khao", [])) + ")"
        self._dong_cham("II", "", mo_ta, nII["diem_toi_da"], khoa_tu_cham)

        # ----- Nhóm III -----
        nIII = ch["nhom_III"]
        self._dong_nhom("III", nIII["ma"], nIII["ten"], nIII["diem_toi_da"])
        self._dong_cham("III", "", f"Điểm cộng (không quá {nIII['ty_le_toi_da_so_voi_nhom_II'] * 100:g}% "
                                   f"điểm Nhóm II, tối đa {nIII['diem_toi_da']:g} điểm)",
                        nIII["diem_toi_da"], khoa_tu_cham)

        # ----- Tổng -----
        self._dong_nhom("tong", "", "TỔNG ĐIỂM", ch["tong_diem_toi_da"], mau=HONG)

    def _dong_nhom(self, khoa, ma, ten, toi_da, mau=VANG):
        r = self._hang
        gia_tri = [ma, ten, f"{toi_da:g}", ""]
        for j, gt in enumerate(gia_tri):
            lbl = ctk.CTkLabel(self.bang, text=gt, font=F(12, True), text_color=CHU, fg_color=mau, corner_radius=6,
                               width=RONG_COT[j], anchor="w" if j == 1 else "center",
                               wraplength=int(RONG_COT[j] * ti_le(self)) - 8 if j == 1 else 0, justify="left")
            lbl.grid(row=r, column=j, sticky="nsew", padx=1, pady=1)
            if j == 3:
                self.nhan_ht_nhom[khoa] = lbl
        for j, c in enumerate(td.COT_DIEM, start=4):
            lbl = ctk.CTkLabel(self.bang, text="", font=F(12, True), text_color=CHU, fg_color=mau,
                               corner_radius=6, width=RONG_COT[j])
            lbl.grid(row=r, column=j, sticky="nsew", padx=1, pady=1)
            self.nhan_tong[(khoa, c)] = lbl
        self._hang += 1

    def _dong_van_ban(self, ma, ten, toi_da, dam=False):
        r = self._hang
        for j, gt in enumerate([ma, ten, f"{toi_da:g}"]):
            ctk.CTkLabel(self.bang, text=gt, font=F(12, dam), text_color=CHU, width=RONG_COT[j],
                         anchor="w" if j == 1 else "center", justify="left",
                         wraplength=int(RONG_COT[j] * ti_le(self)) - 8 if j == 1 else 0
                         ).grid(row=r, column=j, sticky="nsew", padx=1, pady=1)
        self._hang += 1

    def _dong_cham(self, khoa, ma, ten, toi_da, khoa_tu_cham):
        r = self._hang
        for j, gt in enumerate([ma, ten, f"{toi_da:g}"]):
            ctk.CTkLabel(self.bang, text=gt, font=F(11), text_color=CHU, width=RONG_COT[j],
                         anchor="w" if j == 1 else "center", justify="left",
                         wraplength=int(RONG_COT[j] * ti_le(self)) - 8 if j == 1 else 0
                         ).grid(row=r, column=j, sticky="nsew", padx=1, pady=3)
        lbl = ctk.CTkLabel(self.bang, text="", font=F(12), text_color=CHU_NHAT, width=RONG_COT[3])
        lbl.grid(row=r, column=3, padx=1, pady=3)
        self.nhan_he_thong[khoa] = lbl
        diem = self.phieu.get("diem", {}).get(khoa, {})
        for j, c in enumerate(td.COT_DIEM, start=4):
            e = ctk.CTkEntry(self.bang, width=RONG_COT[j] - 20, justify="center", placeholder_text="↩",
                             fg_color=VANG if c == "tu_cham" else THE, text_color=CHU, border_color="#EAD7CF")
            gt = diem.get(c)
            if gt not in (None, ""):
                e.insert(0, f"{td.so(gt):g}")
            if c == "tu_cham" and khoa_tu_cham:
                e.configure(state="disabled")
            e.grid(row=r, column=j, padx=1, pady=3)
            e.bind("<KeyRelease>", lambda _e: self._tinh_lai())
            e.bind("<FocusOut>", lambda _e: self._tinh_lai())
            e._toi_da = toi_da
            self.o[(khoa, c)] = e
        self._hang += 1

    # ---------------- tính toán & lưu ----------------
    def _doc_o(self, bao_loi=False):
        """Đọc các ô nhập vào dict điểm. Ô sai -> viền hồng đậm (và báo lỗi nếu bao_loi)."""
        diem, loi = {}, []
        for (khoa, c), e in self.o.items():
            gt = e.get().strip()
            ok = True
            if gt:
                try:
                    v = float(gt.replace(",", "."))
                    ok = 0 <= v <= e._toi_da
                except ValueError:
                    ok = False
                if ok:
                    diem.setdefault(khoa, {})[c] = v
                else:
                    loi.append(f"Tiêu chí {khoa} – {td.TEN_COT[c]}: «{gt}» (0 – {e._toi_da:g})")
            e.configure(border_color="#EAD7CF" if ok else HONG_DAM)
        if bao_loi and loi:
            raise ValueError("Điểm không hợp lệ:\n" + "\n".join(loi[:8]))
        return diem

    def _tinh_lai(self):
        if not self.phieu:
            return
        ch = self.app.kho.cau_hinh
        tam = dict(self.phieu, diem=self._doc_o())
        kq = td.ket_qua_phieu(tam, self.ky_id, self.app.kho.ds_muc_tieu, ch)
        ht = kq["he_thong"]
        for khoa, lbl in self.nhan_he_thong.items():
            if khoa in ht:
                lbl.configure(text=f"{ht[khoa]:g}")
        tong_ht = {"I": sum(v for k, v in ht.items() if k not in ("II", "III")), "II": ht["II"], "III": ht["III"]}
        tong_ht["tong"] = tong_ht["I"] + tong_ht["II"] + tong_ht["III"]
        for k in ("I", "II", "III", "tong"):
            if k in self.nhan_ht_nhom:
                self.nhan_ht_nhom[k].configure(text=f"{tong_ht[k]:.2f}")
        for c in td.COT_DIEM:
            co_du_lieu = c == "tu_cham" or td.cot_co_du_lieu(tam, c)
            for k in ("I", "II", "III", "tong"):
                self.nhan_tong[(k, c)].configure(text=f"{kq['cot'][c][k]:.2f}" if co_du_lieu else "–")
        xl = kq["xep_loai"]
        self.nhim.ve(xl.get("tam_trang", "binh_thuong"), kq["quy_doi"])
        self.lbl_diem.configure(text=f"{kq['diem_chot']:.2f} / {ch['tong_diem_toi_da']:g}")
        self.lbl_xl.configure(text=f"  {xl['ten']}  ", fg_color=xl.get("mau", HONG_DAM))
        self.lbl_nguon.configure(text=f"Điểm chốt theo: {td.TEN_COT[kq['nguon_chot']]}\n"
                                      f"Điểm KPI quy đổi: {kq['quy_doi'] * 100:.1f}%  ·  "
                                      f"Trần điểm cộng: {kq['cot'][kq['nguon_chot']]['tran_III']:g}")

    def _ghi(self, trang_thai, thong_bao):
        try:
            self.phieu["diem"] = self._doc_o(bao_loi=True)
        except ValueError as loi:
            messagebox.showwarning("Nhím nhắc nhẹ 🦔", str(loi))
            return False
        self.phieu["trang_thai"] = trang_thai
        self.app.kho.luu_phieu(self.phieu)
        self.app.lam_moi_tat_ca()
        if thong_bao:
            messagebox.showinfo("Đã lưu 🦔", thong_bao)
        return True

    def _luu_nhap(self):
        self._ghi(self.phieu["trang_thai"], "Đã lưu phiếu đánh giá.")

    def _gui(self):
        if messagebox.askyesno("Gửi đánh giá", "Chính thức gửi kết quả tự chấm lên cấp trên trực tiếp?\n"
                                               "Cột tự chấm sẽ được khoá lại."):
            self._ghi(PHIEU_DA_GUI, "Đã gửi đánh giá! Nhím chúc bạn đạt kết quả cao 🌟")

    def _mo_lai(self):
        if messagebox.askyesno("Mở lại phiếu", "Mở khoá cột tự chấm để chỉnh sửa lại?"):
            self._ghi(PHIEU_NHAP, None)

    def _ke_thua(self):
        """Điền điểm từ cột Hệ thống đánh giá vào cột Tự chấm."""
        kq = td.ket_qua_phieu(self.phieu, self.ky_id, self.app.kho.ds_muc_tieu, self.app.kho.cau_hinh)
        for (khoa, c), e in self.o.items():
            if c == "tu_cham" and khoa in kq["he_thong"]:
                e.delete(0, "end")
                e.insert(0, f"{kq['he_thong'][khoa]:g}")
        self._tinh_lai()

    def _gui_y_kien(self):
        nd = self.o_y_kien.get("1.0", "end").strip()
        if not nd:
            return
        self.phieu.setdefault("y_kien", []).append({"thoi_gian": bay_gio(), "noi_dung": nd})
        self._ghi(self.phieu["trang_thai"], None)
