# -*- coding: utf-8 -*-
"""DASHBOARD – Kết quả thực hiện mục tiêu & điểm hiệu suất (tính tự động)."""
import tkinter as tk

import customtkinter as ctk

from . import tinh_diem as td
from .cau_hinh import TT_HOAN_THANH, TT_DANG_THUC_HIEN, TT_QUA_HAN, TT_CHUA_BAT_DAU
from .giao_dien_chung import (F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, BAC_HA, BAC_HA_DAM, XANH,
                              XANH_DAM, VANG, VANG_DAM, TIM, TIM_DAM, The, CanvasNhim, hien_ngay, ti_le)
from .nhim import LOI_NHIM, ve_bieu_do_tron

MAU_TT = {TT_HOAN_THANH: BAC_HA_DAM, TT_DANG_THUC_HIEN: XANH_DAM, TT_QUA_HAN: HONG_DAM, TT_CHUA_BAT_DAU: TIM_DAM}
NHIM_TT = {TT_HOAN_THANH: "vui", TT_DANG_THUC_HIEN: "binh_thuong", TT_QUA_HAN: "buon", TT_CHUA_BAT_DAU: "ngu"}


class TrangTongQuan(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=NEN)
        self.app = app
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="c")

    def lam_moi(self):
        for w in self.winfo_children():
            w.destroy()
        kho, ch = self.app.kho, self.app.kho.cau_hinh
        ky_id = self.app.ky_id_dang_chon()
        ds = kho.ds_muc_tieu
        tk_ = td.thong_ke(ky_id, ds, ch)
        dem = tk_["theo_trang_thai"]

        # ---------- Hàng 1: 4 thẻ chỉ số ----------
        the_so = [("🎯", "Tổng mục tiêu", tk_["tong"], TIM, f"KPI {tk_['kpi']} · OKR {tk_['okr']}"),
                  ("🌟", "Hoàn thành", dem[TT_HOAN_THANH], BAC_HA, "Nhím vui lắm!"),
                  ("🌰", "Đang thực hiện", dem[TT_DANG_THUC_HIEN] + dem[TT_CHUA_BAT_DAU], XANH,
                   f"Chưa bắt đầu: {dem[TT_CHUA_BAT_DAU]}"),
                  ("⏰", "Quá hạn", dem[TT_QUA_HAN], HONG, "Cần xử lý ngay" if dem[TT_QUA_HAN] else "Không có 💖")]
        for i, (bt, nhan, so_luong, mau, phu) in enumerate(the_so):
            t = The(self, mau=mau)
            t.grid(row=0, column=i, sticky="nsew", padx=6, pady=(4, 8))
            ctk.CTkLabel(t, text=f"{bt}  {nhan}", font=F(14, True), text_color=CHU).pack(anchor="w", padx=16, pady=(12, 0))
            ctk.CTkLabel(t, text=str(so_luong), font=F(34, True), text_color=CHU).pack(anchor="w", padx=16)
            ctk.CTkLabel(t, text=phu, font=F(12), text_color=CHU_NHAT).pack(anchor="w", padx=16, pady=(0, 12))

        # ---------- Hàng 2: nhím + biểu đồ tròn + điểm hiệu suất ----------
        if ky_id:
            phieu = kho.lay_phieu(ky_id)
            kq = td.ket_qua_phieu(phieu, ky_id, ds, ch)
        else:
            kq = None
        quy_doi = td.diem_kpi_quy_doi(ky_id, ds, ch) if tk_["tong"] else 0.0

        if tk_["tong"] == 0:
            tam_trang = "ngu"
        elif dem[TT_QUA_HAN]:
            tam_trang = "buon"
        elif kq:
            tam_trang = kq["xep_loai"].get("tam_trang", "binh_thuong")
        else:
            tam_trang = "binh_thuong"

        t_nhim = The(self)
        t_nhim.grid(row=1, column=0, sticky="nsew", padx=6, pady=8)
        CanvasNhim(t_nhim, 190, THE, tam_trang, quy_doi if tam_trang != "ngu" else None).pack(pady=(14, 4))
        ctk.CTkLabel(t_nhim, text=LOI_NHIM[tam_trang], font=F(13, True), text_color=CHU,
                     wraplength=int(200 * ti_le(self)), justify="center").pack(padx=10, pady=(0, 14))

        t_tron = The(self)
        t_tron.grid(row=1, column=1, sticky="nsew", padx=6, pady=8)
        ctk.CTkLabel(t_tron, text="Phân bổ theo trạng thái", font=F(14, True), text_color=CHU).pack(pady=(12, 0))
        k = int(170 * ti_le(self))
        cv = tk.Canvas(t_tron, width=k, height=k, bg=THE, highlightthickness=0)
        cv.pack(pady=4)
        du_lieu = [(tt, dem[tt], MAU_TT[tt]) for tt in MAU_TT]
        ve_bieu_do_tron(cv, k / 2, k / 2, k * 0.45, du_lieu, THE)
        chu_giai = ctk.CTkFrame(t_tron, fg_color="transparent")
        chu_giai.pack(pady=(0, 12))
        for i, (tt, v, mau) in enumerate(du_lieu):
            pct = v / tk_["tong"] * 100 if tk_["tong"] else 0
            ctk.CTkLabel(chu_giai, text=f"● {tt}: {v} ({pct:.0f}%)", text_color=mau, font=F(12, True)
                         ).grid(row=i // 2, column=i % 2, sticky="w", padx=6)

        t_diem = The(self)
        t_diem.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=6, pady=8)
        ctk.CTkLabel(t_diem, text="🏆  Điểm hiệu suất (tự động tính)", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=18, pady=(14, 6))
        nII = ch["nhom_II"]
        dong_diem = [("Điểm KPI quy đổi", f"{quy_doi * 100:.1f}%"),
                     (f"Điểm nhóm II = quy đổi × {nII['he_so_quy_doi']:g}",
                      f"{min(quy_doi * nII['he_so_quy_doi'], nII['diem_toi_da']):.2f} / {nII['diem_toi_da']:g}")]
        if kq:
            dong_diem.append((f"Tổng điểm phiếu ({td.TEN_COT[kq['nguon_chot']].replace('Điểm ', '')})",
                              f"{kq['diem_chot']:.2f} / {ch['tong_diem_toi_da']:g}"))
        for nhan, gt in dong_diem:
            h = ctk.CTkFrame(t_diem, fg_color=NEN, corner_radius=12)
            h.pack(fill="x", padx=18, pady=3)
            ctk.CTkLabel(h, text=nhan, font=F(13), text_color=CHU).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(h, text=gt, font=F(15, True), text_color=CHU).pack(side="right", padx=12)
        if kq:
            xl = kq["xep_loai"]
            ctk.CTkLabel(t_diem, text=f"  {xl['ten']}  ", font=F(15, True), text_color="white",
                         fg_color=xl.get("mau", HONG_DAM), corner_radius=14, height=36).pack(pady=(10, 4))
        else:
            ctk.CTkLabel(t_diem, text="Chọn một kỳ cụ thể để xem điểm phiếu & xếp loại.",
                         font=F(12), text_color=CHU_NHAT).pack(pady=8)
        canh_bao = td.kiem_tra_trong_so(ds, ky_id) if ky_id else []
        for c in canh_bao[:3]:
            ctk.CTkLabel(t_diem, text="⚠️ " + c, font=F(12), text_color=HONG_DAM).pack(anchor="w", padx=18)
        ctk.CTkFrame(t_diem, fg_color="transparent", height=10).pack()

        # ---------- Hàng 3: tiến độ từng mục tiêu ----------
        t_ds = The(self)
        t_ds.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=6, pady=8)
        ctk.CTkLabel(t_ds, text="🌰  Tiến độ từng mục tiêu", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=18, pady=(14, 6))
        ds_ky = td.muc_tieu_trong_ky(ky_id, ds)
        if not ds_ky:
            ctk.CTkLabel(t_ds, text="Chưa có mục tiêu nào. Vào mục 🎯 Mục tiêu để thêm mới nhé!",
                         font=F(13), text_color=CHU_NHAT).pack(pady=(0, 16))
        mau_tt = {TT_HOAN_THANH: BAC_HA, TT_DANG_THUC_HIEN: XANH, TT_QUA_HAN: HONG, TT_CHUA_BAT_DAU: TIM}
        for m in ds_ky:
            p = td.tien_do(m, ds, ch)
            tt = td.trang_thai(m, p)
            h = ctk.CTkFrame(t_ds, fg_color=NEN, corner_radius=14)
            h.pack(fill="x", padx=18, pady=3)
            CanvasNhim(h, 44, NEN, NHIM_TT[tt]).pack(side="left", padx=(8, 4), pady=2)
            ten = ("↳ " if m.get("parent_id") else "") + m["ten"]
            ctk.CTkLabel(h, text=f"{ten}\n{m['loai']} · trọng số {m['trong_so']:g}% · hạn {hien_ngay(m['ngay_ket_thuc'])}",
                         font=F(12), text_color=CHU, justify="left", anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(h, text=f" {tt} ", font=F(12, True), text_color=CHU, fg_color=mau_tt[tt],
                         corner_radius=10).pack(side="right", padx=10)
            ctk.CTkLabel(h, text=f"{p * 100:.0f}%", font=F(13, True), text_color=CHU, width=48).pack(side="right")
            pb = ctk.CTkProgressBar(h, width=int(200), height=12, progress_color=MAU_TT[tt], fg_color="#EFE3DE")
            pb.set(min(p, 1.0))
            pb.pack(side="right", padx=6)
        ctk.CTkFrame(t_ds, fg_color="transparent", height=10).pack()

        # ---------- Hàng 4: kết quả đánh giá, xếp loại các kỳ ----------
        t_kq = The(self)
        t_kq.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=6, pady=(8, 16))
        ctk.CTkLabel(t_kq, text="📋  Kết quả đánh giá, xếp loại theo kỳ", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=18, pady=(14, 6))
        bang = ctk.CTkFrame(t_kq, fg_color="transparent")
        bang.pack(fill="x", padx=18, pady=(0, 16))
        tieu_de = ["Kỳ mục tiêu", "Trạng thái phiếu", "Điểm tự ĐG", "Điểm cấp trên ĐG", "Điểm phê duyệt", "Xếp loại"]
        for j, td_ in enumerate(tieu_de):
            bang.grid_columnconfigure(j, weight=3 if j == 0 else 2)
            ctk.CTkLabel(bang, text=td_, font=F(12, True), text_color=CHU, fg_color=HONG,
                         corner_radius=8).grid(row=0, column=j, sticky="ew", padx=2, pady=2)
        for i, ky in enumerate(kho.ds_ky, start=1):
            phieu = kho.du_lieu["phieu_danh_gia"].get(ky["id"])
            r = td.ket_qua_phieu(phieu or kho.lay_phieu(ky["id"]), ky["id"], ds, ch)
            c = r["cot"]
            gia_tri = [ky["ten"], phieu["trang_thai"] if phieu else "Chưa lập phiếu",
                       f"{c['tu_cham']['tong']:.2f}",
                       f"{c['cap_tren']['tong']:.2f}" if td.cot_co_du_lieu(phieu or {}, "cap_tren") else "–",
                       f"{c['tham_quyen']['tong']:.2f}" if td.cot_co_du_lieu(phieu or {}, "tham_quyen") else "–",
                       r["xep_loai"]["ten"]]
            for j, gt in enumerate(gia_tri):
                ctk.CTkLabel(bang, text=gt, font=F(12, j == 5),
                             text_color="white" if j == 5 else CHU,
                             fg_color=r["xep_loai"].get("mau") if j == 5 else NEN, corner_radius=8,
                             wraplength=int(260 * ti_le(self)) if j == 0 else 0
                             ).grid(row=i, column=j, sticky="ew", padx=2, pady=2)
