# -*- coding: utf-8 -*-
"""Các hộp thoại Thêm mới / Chỉnh sửa: Kỳ mục tiêu và Mục tiêu (KPI/OKR)."""
import copy
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from .cau_hinh import (LOAI_MUC_TIEU, PHUONG_THUC_DANH_GIA, PT_CHI_TIEU, PT_TONG_HOP_CON,
                       PT_CONG_VIEC, LOAI_NGUON, DOI_TUONG_MUC_TIEU, LOAI_KY, TIEU_CHI_KY,
                       TRANG_THAI_KY)
from .giao_dien_chung import (F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, BAC_HA_DAM, XANH_DAM,
                              TIM, nut, BangDong, hien_ngay, doc_ngay_nhap, mo_tep, CanvasNhim)
from .luu_tru import ky_moi, muc_tieu_moi


class HopThoaiCoBan(ctk.CTkToplevel):
    """Cửa sổ con dạng modal, có vùng cuộn và thanh nút Lưu/Huỷ."""

    def __init__(self, master, tieu_de, rong=760, cao=680):
        super().__init__(master)
        self.title(tieu_de)
        self.geometry(f"{rong}x{cao}")
        self.minsize(560, 420)
        self.configure(fg_color=NEN)
        self.transient(master)
        self.ket_qua = None

        dau = ctk.CTkFrame(self, fg_color=HONG, corner_radius=0, height=64)
        dau.pack(fill="x")
        CanvasNhim(dau, kich_thuoc=58, mau_nen=HONG, tam_trang="vui").pack(side="left", padx=(14, 6), pady=3)
        ctk.CTkLabel(dau, text=tieu_de, font=F(18, True), text_color=CHU).pack(side="left")

        self.vung = ctk.CTkScrollableFrame(self, fg_color=NEN)
        self.vung.pack(fill="both", expand=True, padx=12, pady=8)
        self.vung.grid_columnconfigure(1, weight=1)
        self._dong = 0

        chan = ctk.CTkFrame(self, fg_color=NEN)
        chan.pack(fill="x", padx=16, pady=(0, 14))
        nut(chan, "💾  Lưu", self._bam_luu, mau=BAC_HA_DAM, width=120).pack(side="right")
        nut(chan, "Huỷ", self.destroy, mau=HONG, mau_chu=CHU, width=90).pack(side="right", padx=8)

        self.after(120, self._hien)

    def _hien(self):
        self.lift()
        self.focus_force()
        try:
            self.grab_set()
        except tk.TclError:
            pass

    # --- tiện ích bố cục: nhãn trái / widget phải ---
    def hang(self, nhan, widget_tao, bat_buoc=False):
        ctk.CTkLabel(self.vung, text=nhan + (" *" if bat_buoc else ""), font=F(13, True),
                     text_color=CHU, anchor="w").grid(row=self._dong, column=0, sticky="nw", padx=(4, 12), pady=6)
        w = widget_tao(self.vung)
        w.grid(row=self._dong, column=1, sticky="ew", pady=6)
        self._dong += 1
        return w

    def khoi(self, widget):
        widget.grid(row=self._dong, column=0, columnspan=2, sticky="ew", pady=6)
        self._dong += 1
        return widget

    def o_nhap(self, gia_tri="", goi_y=""):
        def tao(m):
            e = ctk.CTkEntry(m, placeholder_text=goi_y)
            if gia_tri not in (None, ""):
                e.insert(0, str(gia_tri))
            return e
        return tao

    def _bam_luu(self):
        try:
            self.ket_qua = self.thu_thap()
        except ValueError as loi:
            messagebox.showwarning("Nhím nhắc nhẹ 🦔", str(loi), parent=self)
            return
        self.destroy()

    def thu_thap(self):
        raise NotImplementedError


# ======================================================================
class HopThoaiKy(HopThoaiCoBan):
    """Thêm mới / chỉnh sửa Kỳ mục tiêu."""

    def __init__(self, master, ky=None):
        self.ky = copy.deepcopy(ky) if ky else ky_moi()
        super().__init__(master, "Chỉnh sửa kỳ mục tiêu" if ky else "Thêm mới kỳ mục tiêu", 680, 600)
        k = self.ky
        self.e_ten = self.hang("Tên kỳ", self.o_nhap(k["ten"], "VD: Nhiệm vụ công tác năm 2026"), True)
        self.v_tieu_chi = tk.StringVar(value=k["tieu_chi"])
        self.hang("Tiêu chí", lambda m: ctk.CTkComboBox(m, values=TIEU_CHI_KY, variable=self.v_tieu_chi))
        self.e_dv = self.hang("Đơn vị sở hữu", self.o_nhap(k["don_vi_so_huu"], "Phòng ban / đơn vị phụ trách"))
        self.v_loai = tk.StringVar(value=k["loai"])
        self.hang("Loại kỳ", lambda m: ctk.CTkSegmentedButton(
            m, values=LOAI_KY, variable=self.v_loai, selected_color=HONG_DAM, selected_hover_color=HONG_DAM))
        self.e_nam = self.hang("Năm", self.o_nhap(k["nam"]), True)
        self.e_so_ky = self.hang("Quý/Tháng số", self.o_nhap(k.get("so_ky", 1), "Chỉ dùng khi loại là Quý hoặc Tháng"))
        self.e_dvt = self.hang("Đơn vị tính mục tiêu", self.o_nhap(", ".join(k["don_vi_tinh"]),
                                                                   "Cách nhau bằng dấu phẩy"))
        self.v_tt = tk.StringVar(value=k.get("trang_thai", "Đang thực hiện"))
        self.hang("Trạng thái", lambda m: ctk.CTkComboBox(m, values=TRANG_THAI_KY, variable=self.v_tt))
        self.t_mo_ta = self.hang("Mô tả kỳ mục tiêu", lambda m: ctk.CTkTextbox(m, height=110))
        self.t_mo_ta.insert("1.0", k.get("mo_ta", ""))

    def thu_thap(self):
        ten = self.e_ten.get().strip()
        if not ten:
            raise ValueError("Vui lòng nhập Tên kỳ mục tiêu.")
        try:
            nam = int(self.e_nam.get().strip())
            assert 2000 <= nam <= 2100
        except (ValueError, AssertionError):
            raise ValueError("Năm không hợp lệ.")
        so_ky = 1
        if self.v_loai.get() != "Năm":
            gioi_han = 4 if self.v_loai.get() == "Quý" else 12
            try:
                so_ky = int(self.e_so_ky.get().strip())
                assert 1 <= so_ky <= gioi_han
            except (ValueError, AssertionError):
                raise ValueError(f"{self.v_loai.get()} số phải từ 1 đến {gioi_han}.")
        dvt = [x.strip() for x in self.e_dvt.get().split(",") if x.strip()]
        self.ky.update(ten=ten, tieu_chi=self.v_tieu_chi.get(), don_vi_so_huu=self.e_dv.get().strip(),
                       loai=self.v_loai.get(), nam=nam, so_ky=so_ky, don_vi_tinh=dvt or ["Văn bản"],
                       trang_thai=self.v_tt.get(), mo_ta=self.t_mo_ta.get("1.0", "end").strip())
        return self.ky


# ======================================================================
class HopThoaiMucTieu(HopThoaiCoBan):
    """Thêm mới / chỉnh sửa Mục tiêu loại KPI hoặc OKR (đủ các trường như tài liệu)."""

    def __init__(self, master, kho, ky_id, muc_tieu=None, parent_id=None):
        self.kho = kho
        self.ky = kho.tim_ky(ky_id)
        self.mt = copy.deepcopy(muc_tieu) if muc_tieu else muc_tieu_moi(ky_id=ky_id, parent_id=parent_id)
        self.la_moi = muc_tieu is None
        super().__init__(master, "Chỉnh sửa mục tiêu" if muc_tieu else "Thêm mới mục tiêu", 860, 760)
        m = self.mt

        # --- Bước 1: loại mục tiêu & kỳ liên kết ---
        ctk.CTkLabel(self.vung, text=f"📅  Kỳ mục tiêu liên kết: {self.ky['ten']}", font=F(13),
                     text_color=CHU_NHAT, anchor="w").grid(row=self._dong, column=0, columnspan=2, sticky="w")
        self._dong += 1
        self.v_loai = tk.StringVar(value=m["loai"])
        self.hang("Loại mục tiêu", lambda w: ctk.CTkSegmentedButton(
            w, values=LOAI_MUC_TIEU, variable=self.v_loai, command=lambda _: self._cap_nhat_vung_do(),
            selected_color=HONG_DAM, selected_hover_color=HONG_DAM), True)

        # mục tiêu cha (loại trừ chính nó và con cháu để tránh vòng lặp)
        cam = self.kho.hau_due(m["id"]) | {m["id"]}
        self.ds_cha = [x for x in self.kho.ds_muc_tieu if x.get("ky_id") == ky_id and x["id"] not in cam]
        nhan_cha = ["(Không – mục tiêu gốc)"] + [self._nhan(x) for x in self.ds_cha]
        cha_hien_tai = next((self._nhan(x) for x in self.ds_cha if x["id"] == m.get("parent_id")), nhan_cha[0])
        self.v_cha = tk.StringVar(value=cha_hien_tai)
        self.hang("Mục tiêu cha", lambda w: ctk.CTkComboBox(w, values=nhan_cha, variable=self.v_cha))

        self.v_pt = tk.StringVar(value=m["phuong_thuc"])
        self.hang("Phương thức đánh giá", lambda w: ctk.CTkComboBox(
            w, values=PHUONG_THUC_DANH_GIA, variable=self.v_pt, command=lambda _: self._cap_nhat_vung_do()), True)

        # --- Bước 2/3: thông tin cốt lõi ---
        self.e_ten = self.hang("Tên mục tiêu", self.o_nhap(m["ten"], "VD: Ban hành văn bản quy phạm pháp luật 2026"), True)
        self.e_ts = self.hang("Trọng số (%)", self.o_nhap(f"{m['trong_so']:g}" if m["trong_so"] else "",
                                                          "Mức độ quan trọng, các mục tiêu cùng cấp cộng lại = 100"), True)
        self.v_dt = tk.StringVar(value=m["doi_tuong"])
        self.hang("Đối tượng mục tiêu", lambda w: ctk.CTkComboBox(w, values=DOI_TUONG_MUC_TIEU, variable=self.v_dt))
        self.e_dv = self.hang("Đơn vị / phòng ban", self.o_nhap(m["don_vi"]))
        self.e_ntt = self.hang("Người thực hiện chính", self.o_nhap(m["nguoi_thuc_hien"]))
        self.e_ntd = self.hang("Người theo dõi", self.o_nhap(m["nguoi_theo_doi"], "Nhiều người cách nhau bằng dấu phẩy"))
        self.e_bd = self.hang("Ngày bắt đầu", self.o_nhap(hien_ngay(m["ngay_bat_dau"]), "dd/mm/yyyy"), True)
        self.e_kt = self.hang("Ngày kết thúc", self.o_nhap(hien_ngay(m["ngay_ket_thuc"]), "dd/mm/yyyy"), True)

        tuy_chon = ctk.CTkFrame(self.vung, fg_color="transparent")
        self.v_ket_noi = tk.BooleanVar(value=m.get("ket_noi_cha", False))
        self.v_cong_khai = tk.BooleanVar(value=m.get("cong_khai", False))
        ctk.CTkCheckBox(tuy_chon, text="Kết nối mục tiêu cha", variable=self.v_ket_noi,
                        fg_color=HONG_DAM).pack(side="left", padx=(0, 18))
        ctk.CTkCheckBox(tuy_chon, text="Công khai kỳ mục tiêu", variable=self.v_cong_khai,
                        fg_color=HONG_DAM).pack(side="left")
        self.hang("Liên kết & công khai", lambda w: tuy_chon)

        # --- Vùng thiết lập đo lường (đổi theo loại/phương thức) ---
        self.vung_do = self.khoi(ctk.CTkFrame(self.vung, fg_color="transparent"))
        dvt = "|".join(self.ky.get("don_vi_tinh") or ["Văn bản"])
        self.bang_chi_tieu = BangDong(self.vung_do, [
            ("don_vi_tinh", "Đơn vị tính", 150, "chon:" + dvt),
            ("gia_tri_muc_tieu", "Giá trị mục tiêu", 120, "so"),
            ("gia_tri_dat", "Giá trị đã đạt", 120, "so"),
            ("ty_trong", "Tỷ trọng (%)", 100, "so")], "📏 Chỉ tiêu theo đơn vị tính (KPI)", "+ Thêm chỉ tiêu")
        self.bang_chi_tieu.dat_du_lieu(m["chi_tieu"])
        self.bang_kr = BangDong(self.vung_do, [
            ("ten", "Kết quả then chốt", 260, "chu"),
            ("gia_tri_muc_tieu", "Mục tiêu", 90, "so"),
            ("gia_tri_dat", "Đã đạt", 90, "so"),
            ("ty_trong", "Tỷ trọng (%)", 90, "so")], "🔑 Kết quả then chốt (OKR)", "+ Tạo mới")
        self.bang_kr.dat_du_lieu(m["ket_qua_then_chot"])
        self.khung_cv = ctk.CTkFrame(self.vung_do, fg_color="transparent")
        self.v_nguon = tk.StringVar(value=m.get("loai_nguon", LOAI_NGUON[1]))
        hang_nguon = ctk.CTkFrame(self.khung_cv, fg_color="transparent")
        hang_nguon.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(hang_nguon, text="Loại nguồn:", font=F(13, True), text_color=CHU).pack(side="left", padx=(4, 10))
        for g in LOAI_NGUON:
            ctk.CTkRadioButton(hang_nguon, text=g, variable=self.v_nguon, value=g,
                               fg_color=HONG_DAM).pack(side="left", padx=6)
        self.bang_cv = BangDong(self.khung_cv, [
            ("ten", "Tên công việc / hạng mục dự án", 420, "chu"),
            ("hoan_thanh", "Hoàn thành", 90, "check")], "✅ Danh sách công việc liên kết", "+ Thêm việc")
        self.bang_cv.pack(fill="x")
        self.bang_cv.dat_du_lieu(m["cong_viec"])
        self.nhan_tong_hop = ctk.CTkLabel(
            self.vung_do, text="🌰 Tiến độ được TỰ ĐỘNG TỔNG HỢP từ các mục tiêu con theo trọng số (%). "
                               "Hãy thêm mục tiêu con sau khi lưu.",
            font=F(13), text_color=CHU, fg_color=TIM, corner_radius=12, wraplength=700, justify="left")
        self._cap_nhat_vung_do()

        # --- Mô tả & tệp minh chứng ---
        self.t_mo_ta = self.hang("Mô tả mục tiêu", lambda w: ctk.CTkTextbox(w, height=90))
        self.t_mo_ta.insert("1.0", m.get("mo_ta", ""))
        self.tep = list(m.get("tep_dinh_kem", []))
        khung_tep = ctk.CTkFrame(self.vung, fg_color="transparent")
        nut(khung_tep, "📎 Chọn tệp", self._chon_tep, mau=XANH_DAM, width=110, height=30).pack(anchor="w")
        self.ds_tep = ctk.CTkFrame(khung_tep, fg_color="transparent")
        self.ds_tep.pack(fill="x", pady=4)
        self.hang("Tệp đính kèm minh chứng", lambda w: khung_tep)
        self._ve_tep()

    @staticmethod
    def _nhan(x):
        return f"{x['ten']}  [{x['id'][:4]}]"

    def _cap_nhat_vung_do(self):
        for w in (self.bang_chi_tieu, self.bang_kr, self.khung_cv, self.nhan_tong_hop):
            w.pack_forget()
        pt = self.v_pt.get()
        if pt == PT_TONG_HOP_CON:
            self.nhan_tong_hop.pack(fill="x", pady=4, ipady=8)
        elif pt == PT_CONG_VIEC:
            self.khung_cv.pack(fill="x", pady=4)
        elif self.v_loai.get() == "KPI":
            self.bang_chi_tieu.pack(fill="x", pady=4)
        else:
            self.bang_kr.pack(fill="x", pady=4)

    def _chon_tep(self):
        ds = filedialog.askopenfilenames(parent=self, title="Chọn tệp minh chứng", filetypes=[
            ("Tài liệu", "*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.png *.jpg"), ("Tất cả", "*.*")])
        for p in ds:
            if p not in self.tep:
                self.tep.append(p)
        self._ve_tep()

    def _ve_tep(self):
        for w in self.ds_tep.winfo_children():
            w.destroy()
        for p in self.tep:
            h = ctk.CTkFrame(self.ds_tep, fg_color=THE, corner_radius=10)
            h.pack(fill="x", pady=2)
            ctk.CTkLabel(h, text="📄 " + os.path.basename(p), font=F(12), text_color=CHU,
                         anchor="w").pack(side="left", padx=8)
            ctk.CTkButton(h, text="✕", width=26, height=24, fg_color=HONG, hover_color=HONG_DAM, text_color=CHU,
                          command=lambda p=p: (self.tep.remove(p), self._ve_tep())).pack(side="right", padx=4, pady=3)
            ctk.CTkButton(h, text="Xem", width=44, height=24, fg_color=XANH_DAM,
                          command=lambda p=p: self._xem(p)).pack(side="right", padx=2, pady=3)

    def _xem(self, p):
        if os.path.exists(p):
            mo_tep(p)
        else:
            messagebox.showwarning("Không tìm thấy tệp", f"Tệp đã bị di chuyển hoặc xoá:\n{p}", parent=self)

    def thu_thap(self):
        ten = self.e_ten.get().strip()
        if not ten:
            raise ValueError("Vui lòng nhập Tên mục tiêu.")
        try:
            ts = float(self.e_ts.get().strip().replace(",", "."))
            assert 0 <= ts <= 100
        except (ValueError, AssertionError):
            raise ValueError("Trọng số (%) phải là số từ 0 đến 100.")
        bd = doc_ngay_nhap(self.e_bd.get(), "Ngày bắt đầu")
        kt = doc_ngay_nhap(self.e_kt.get(), "Ngày kết thúc")
        if not bd or not kt:
            raise ValueError("Vui lòng nhập đủ Ngày bắt đầu và Ngày kết thúc.")
        if kt < bd:
            raise ValueError("Ngày kết thúc phải sau hoặc bằng Ngày bắt đầu.")

        pt, loai = self.v_pt.get(), self.v_loai.get()
        chi_tieu = self.bang_chi_tieu.lay_du_lieu()
        kr = self.bang_kr.lay_du_lieu()
        cv = self.bang_cv.lay_du_lieu()
        if pt == PT_CHI_TIEU:
            dong = chi_tieu if loai == "KPI" else kr
            if not dong:
                raise ValueError("Vui lòng thêm ít nhất một " +
                                 ("chỉ tiêu theo đơn vị tính." if loai == "KPI" else "kết quả then chốt."))
            if any(d.get("gia_tri_muc_tieu", 0) <= 0 for d in dong):
                raise ValueError("Giá trị mục tiêu của mỗi dòng phải lớn hơn 0.")
            if loai == "OKR" and any(not d.get("ten") for d in kr):
                raise ValueError("Vui lòng nhập tên cho mọi kết quả then chốt.")
        if pt == PT_CONG_VIEC and not cv:
            raise ValueError("Vui lòng thêm ít nhất một công việc liên kết.")

        nhan_cha = self.v_cha.get()
        cha = next((x["id"] for x in self.ds_cha if self._nhan(x) == nhan_cha), None)
        self.mt.update(
            loai=loai, phuong_thuc=pt, parent_id=cha, ten=ten, trong_so=ts,
            doi_tuong=self.v_dt.get(), don_vi=self.e_dv.get().strip(),
            nguoi_thuc_hien=self.e_ntt.get().strip(), nguoi_theo_doi=self.e_ntd.get().strip(),
            ngay_bat_dau=bd, ngay_ket_thuc=kt, ket_noi_cha=self.v_ket_noi.get(),
            cong_khai=self.v_cong_khai.get(), chi_tieu=chi_tieu, ket_qua_then_chot=kr,
            loai_nguon=self.v_nguon.get(), cong_viec=cv, tep_dinh_kem=self.tep,
            mo_ta=self.t_mo_ta.get("1.0", "end").strip())
        return self.mt
