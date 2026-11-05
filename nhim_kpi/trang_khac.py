# -*- coding: utf-8 -*-
"""TRANG KỲ MỤC TIÊU và TRANG CÀI ĐẶT."""
import json
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from .giao_dien_chung import (F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, BAC_HA_DAM, XANH_DAM, VANG,
                              TIM, The, nut, CanvasNhim, mo_tep, ti_le)
from .hop_thoai import HopThoaiKy
from .luu_tru import ky_moi


class TrangKy(ctk.CTkFrame):
    """Danh sách kỳ mục tiêu: Thêm mới / Chỉnh sửa / Xoá."""
    COT = [("ten", "Tên kỳ", 300), ("loai", "Loại", 110), ("tieu_chi", "Tiêu chí", 200),
           ("don_vi", "Đơn vị sở hữu", 180), ("so_mt", "Số mục tiêu", 100), ("trang_thai", "Trạng thái", 130)]

    def __init__(self, master, app):
        super().__init__(master, fg_color=NEN)
        self.app = app
        thanh = ctk.CTkFrame(self, fg_color="transparent")
        thanh.pack(fill="x", padx=6, pady=(4, 8))
        nut(thanh, "＋ Thêm mới kỳ mục tiêu", self.them, mau=HONG_DAM).pack(side="left", padx=3)
        nut(thanh, "✏️ Chỉnh sửa", self.sua, mau=XANH_DAM).pack(side="left", padx=3)
        nut(thanh, "🗑️ Xoá", self.xoa, mau=HONG, mau_chu=CHU).pack(side="left", padx=3)
        nut(thanh, "📌 Đặt làm kỳ đang xem", self.chon_xem, mau=BAC_HA_DAM).pack(side="left", padx=3)

        t = The(self)
        t.pack(fill="both", expand=True, padx=6, pady=4)
        ctk.CTkLabel(t, text="📅  Danh sách kỳ mục tiêu", font=F(15, True), text_color=CHU).pack(anchor="w", padx=16, pady=(12, 6))
        self.bang = ttk.Treeview(t, columns=[c[0] for c in self.COT], show="headings", style="Nhim.Treeview")
        for k, nhan, rong in self.COT:
            self.bang.heading(k, text=nhan)
            self.bang.column(k, width=int(rong * ti_le(self)), anchor="w" if k == "ten" else "center")
        self.bang.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.bang.bind("<Double-1>", lambda e: self.sua())

    def lam_moi(self):
        self.bang.delete(*self.bang.get_children())
        for k in self.app.kho.ds_ky:
            so_mt = sum(1 for m in self.app.kho.ds_muc_tieu if m.get("ky_id") == k["id"])
            loai = k["loai"] + (f" {k.get('so_ky', 1)}" if k["loai"] != "Năm" else "") + f" / {k['nam']}"
            self.bang.insert("", "end", iid=k["id"], values=(k["ten"], loai, k["tieu_chi"], k["don_vi_so_huu"],
                                                             so_mt, k.get("trang_thai", "")))

    def _chon(self):
        sel = self.bang.selection()
        if not sel:
            messagebox.showinfo("Nhím nhắc nhẹ 🦔", "Hãy chọn một kỳ mục tiêu trong danh sách.")
            return None
        return self.app.kho.tim_ky(sel[0])

    def _mo(self, ky=None):
        hop = HopThoaiKy(self.app, ky)
        self.app.wait_window(hop)
        if hop.ket_qua:
            self.app.kho.luu_ky(hop.ket_qua)
            self.app.cap_nhat_ds_ky(chon_id=hop.ket_qua["id"])
            self.app.lam_moi_tat_ca()

    def them(self):
        self._mo()

    def sua(self):
        ky = self._chon()
        if ky:
            self._mo(ky)

    def chon_xem(self):
        ky = self._chon()
        if ky:
            self.app.cap_nhat_ds_ky(chon_id=ky["id"])
            self.app.lam_moi_tat_ca()

    def xoa(self):
        ky = self._chon()
        if not ky:
            return
        so_mt = sum(1 for m in self.app.kho.ds_muc_tieu if m.get("ky_id") == ky["id"])
        co_phieu = ky["id"] in self.app.kho.du_lieu["phieu_danh_gia"]
        canh_bao = f"Xoá kỳ mục tiêu «{ky['ten']}»?"
        if so_mt or co_phieu:
            canh_bao += (f"\n\n⚠️ Kỳ này đang gắn {so_mt} mục tiêu"
                         f"{' và 1 phiếu đánh giá' if co_phieu else ''} – tất cả sẽ bị xoá vĩnh viễn."
                         "\nChỉ nên xoá kỳ ở trạng thái Bản nháp hoặc chưa có dữ liệu đánh giá.")
        if messagebox.askyesno("Xác nhận xoá", canh_bao, icon="warning"):
            self.app.kho.xoa_ky(ky["id"])
            self.app.cap_nhat_ds_ky()
            self.app.lam_moi_tat_ca()


class TrangCaiDat(ctk.CTkScrollableFrame):
    """Thông tin cá nhân, sao lưu/khôi phục dữ liệu JSON, xem thang xếp loại."""

    def __init__(self, master, app):
        super().__init__(master, fg_color=NEN)
        self.app = app

    def lam_moi(self):
        for w in self.winfo_children():
            w.destroy()
        kho = self.app.kho
        nd = kho.du_lieu["nguoi_dung"]

        t = The(self)
        t.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(t, text="👤  Thông tin cán bộ (in trên phiếu đánh giá)", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=16, pady=(12, 6))
        self.o = {}
        for khoa, nhan in (("ho_ten", "Họ và tên"), ("chuc_vu", "Chức vụ / chức danh"), ("don_vi", "Đơn vị công tác")):
            h = ctk.CTkFrame(t, fg_color="transparent")
            h.pack(fill="x", padx=16, pady=3)
            ctk.CTkLabel(h, text=nhan, width=170, anchor="w", font=F(13), text_color=CHU).pack(side="left")
            e = ctk.CTkEntry(h)
            e.insert(0, nd.get(khoa, ""))
            e.pack(side="left", fill="x", expand=True)
            self.o[khoa] = e
        nut(t, "💾 Lưu thông tin", self._luu_nd, mau=BAC_HA_DAM).pack(anchor="e", padx=16, pady=(6, 14))

        t = The(self)
        t.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(t, text="💾  Dữ liệu cục bộ (JSON)", font=F(15, True), text_color=CHU).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(t, text=f"File dữ liệu: {kho.file_du_lieu}\nFile cấu hình: {kho.file_cau_hinh}\n"
                             "Mỗi lần lưu, phần mềm tự giữ 1 bản sao lưu .bak bên cạnh.",
                     font=F(12), text_color=CHU_NHAT, justify="left").pack(anchor="w", padx=16)
        h = ctk.CTkFrame(t, fg_color="transparent")
        h.pack(fill="x", padx=16, pady=(8, 14))
        nut(h, "📂 Mở thư mục dữ liệu", lambda: mo_tep(str(kho.file_du_lieu.parent)), mau=XANH_DAM).pack(side="left", padx=3)
        nut(h, "📤 Xuất bản sao lưu", self._xuat, mau=BAC_HA_DAM).pack(side="left", padx=3)
        nut(h, "📥 Khôi phục từ file", self._nhap, mau=VANG, mau_chu=CHU).pack(side="left", padx=3)
        nut(h, "⚙️ Mở file cấu hình", lambda: mo_tep(str(kho.file_cau_hinh)), mau=TIM, mau_chu=CHU).pack(side="left", padx=3)

        t = The(self)
        t.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(t, text="🏅  Thang xếp loại & công thức đang áp dụng", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=16, pady=(12, 6))
        hang = ctk.CTkFrame(t, fg_color="transparent")
        hang.pack(fill="x", padx=16)
        ds_xl = sorted(kho.cau_hinh["xep_loai"], key=lambda x: x["diem_tu"], reverse=True)
        tren = kho.cau_hinh["tong_diem_toi_da"]
        for xl in ds_xl:
            o = ctk.CTkFrame(hang, fg_color=NEN, corner_radius=14)
            o.pack(side="left", padx=4, fill="x", expand=True)
            CanvasNhim(o, 80, NEN, xl.get("tam_trang", "binh_thuong")).pack(pady=(6, 0))
            ctk.CTkLabel(o, text=xl["ten"], font=F(12, True), text_color="white", fg_color=xl.get("mau", HONG_DAM),
                         corner_radius=10).pack(padx=6)
            ctk.CTkLabel(o, text=f"{xl['diem_tu']:g} – {tren:g} điểm" if xl is ds_xl[0]
                         else f"từ {xl['diem_tu']:g} điểm", font=F(12), text_color=CHU).pack(pady=(2, 8))
            tren = xl["diem_tu"]
        ctk.CTkLabel(t, text=kho.cau_hinh.get("ghi_chu", ""), font=F(12), text_color=CHU_NHAT,
                     wraplength=int(900 * ti_le(self)), justify="left").pack(anchor="w", padx=16, pady=(8, 14))
        ctk.CTkLabel(self, text="🦔 Nhím KPI v1.0 – dữ liệu chỉ lưu trên máy của bạn.", font=F(11),
                     text_color=CHU_NHAT).pack(pady=8)

    def _luu_nd(self):
        self.app.kho.du_lieu["nguoi_dung"] = {k: e.get().strip() for k, e in self.o.items()}
        self.app.kho.luu()
        messagebox.showinfo("Đã lưu 🦔", "Đã cập nhật thông tin cán bộ.")
        self.app.lam_moi_tat_ca()

    def _xuat(self):
        p = filedialog.asksaveasfilename(defaultextension=".json", initialfile="NhimKPI_saoluu.json",
                                         filetypes=[("JSON", "*.json")])
        if p:
            self.app.kho.xuat(p)
            messagebox.showinfo("Xuất dữ liệu", f"Đã sao lưu tới:\n{p}")

    def _nhap(self):
        p = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not p:
            return
        if not messagebox.askyesno("Khôi phục dữ liệu", "Dữ liệu hiện tại sẽ được thay bằng dữ liệu trong file. Tiếp tục?"):
            return
        try:
            self.app.kho.nhap(p)
        except (ValueError, json.JSONDecodeError) as loi:
            messagebox.showerror("Lỗi", str(loi))
            return
        self.app.cap_nhat_ds_ky()
        self.app.lam_moi_tat_ca()
        messagebox.showinfo("Khôi phục", "Đã khôi phục dữ liệu thành công 🦔")
