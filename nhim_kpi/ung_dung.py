# -*- coding: utf-8 -*-
"""CỬA SỔ CHÍNH – thanh điều hướng bên trái + bộ chọn kỳ mục tiêu dùng chung."""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from .giao_dien_chung import F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, CanvasNhim
from .luu_tru import KhoDuLieu
from .trang_tong_quan import TrangTongQuan
from .trang_muc_tieu import TrangMucTieu
from .trang_phieu import TrangPhieu
from .trang_khac import TrangKy, TrangCaiDat


def duong_dan_tai_nguyen(ten):
    """Đường dẫn tới file trong thư mục assets (chạy được cả khi đã đóng gói PyInstaller)."""
    goc = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return goc / "assets" / ten


TAT_CA = "🌈 Tất cả các kỳ"

MENU = [("tong_quan", "🏠  Tổng quan", TrangTongQuan),
        ("muc_tieu", "🎯  Mục tiêu", TrangMucTieu),
        ("phieu", "📝  Phiếu đánh giá", TrangPhieu),
        ("ky", "📅  Kỳ mục tiêu", TrangKy),
        ("cai_dat", "⚙️  Cài đặt", TrangCaiDat)]


class UngDung(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        super().__init__()
        self.title("Nhím KPI 🦔 – Quản lý KPI cá nhân")
        self.geometry("1360x840")
        self.minsize(1100, 680)
        self.configure(fg_color=NEN)
        self.after(300, self._dat_icon)

        try:
            self.kho = KhoDuLieu()
        except Exception as loi:   # lỗi quyền ghi thư mục...
            messagebox.showerror("Không mở được dữ liệu", str(loi))
            raise

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._ve_thanh_ben()
        self._ve_dau_trang()

        self.trang = {}
        for khoa, _, lop in MENU:
            self.trang[khoa] = lop(self, self)
        self.trang_hien_tai = None
        self.chuyen_trang("tong_quan")

    def _dat_icon(self):
        """Gắn icon chú nhím cho cửa sổ (bỏ qua nếu thiếu file)."""
        try:
            if sys.platform == "win32" and duong_dan_tai_nguyen("nhim.ico").exists():
                self.iconbitmap(str(duong_dan_tai_nguyen("nhim.ico")))
            elif duong_dan_tai_nguyen("nhim.png").exists():
                self._anh_icon = tk.PhotoImage(file=str(duong_dan_tai_nguyen("nhim.png")))
                self.iconphoto(True, self._anh_icon)
        except tk.TclError:
            pass

    # ---------------- thanh điều hướng ----------------
    def _ve_thanh_ben(self):
        ben = ctk.CTkFrame(self, fg_color=HONG, corner_radius=0, width=220)
        ben.grid(row=0, column=0, rowspan=2, sticky="nsw")
        ben.grid_propagate(False)
        self.nhim_logo = CanvasNhim(ben, 120, HONG, "vui", 0.7)
        self.nhim_logo.pack(pady=(18, 0))
        ctk.CTkLabel(ben, text="Nhím KPI", font=F(24, True), text_color=CHU).pack()
        ctk.CTkLabel(ben, text="ôm quả thông · đạt mục tiêu", font=F(11), text_color=CHU_NHAT).pack(pady=(0, 18))
        self.nut_menu = {}
        for khoa, nhan, _ in MENU:
            b = ctk.CTkButton(ben, text=nhan, anchor="w", font=F(14, True), height=44, corner_radius=14,
                              fg_color="transparent", hover_color="#F7D6E0", text_color=CHU,
                              command=lambda k=khoa: self.chuyen_trang(k))
            b.pack(fill="x", padx=14, pady=3)
            self.nut_menu[khoa] = b

    def _ve_dau_trang(self):
        dau = ctk.CTkFrame(self, fg_color=NEN, height=64)
        dau.grid(row=0, column=1, sticky="ew", padx=16, pady=(12, 4))
        self.lbl_tieu_de = ctk.CTkLabel(dau, text="", font=F(22, True), text_color=CHU)
        self.lbl_tieu_de.pack(side="left")
        self.v_ky = tk.StringVar()
        self.cb_ky = ctk.CTkOptionMenu(dau, variable=self.v_ky, width=320, font=F(13), dropdown_font=F(13),
                                       fg_color=THE, button_color=HONG_DAM, button_hover_color=HONG_DAM,
                                       text_color=CHU, command=lambda _: self.lam_moi_tat_ca())
        self.cb_ky.pack(side="right")
        ctk.CTkLabel(dau, text="Kỳ mục tiêu:", font=F(13, True), text_color=CHU).pack(side="right", padx=8)
        self.cap_nhat_ds_ky()

    # ---------------- kỳ đang chọn ----------------
    def cap_nhat_ds_ky(self, chon_id=None):
        """Nạp lại danh sách kỳ vào bộ chọn (tên trùng nhau được gắn thêm mã)."""
        dem = {}
        for k in self.kho.ds_ky:
            dem[k["ten"]] = dem.get(k["ten"], 0) + 1
        self._nhan_ky = {}
        for k in self.kho.ds_ky:
            nhan = k["ten"] if dem[k["ten"]] == 1 else f"{k['ten']} [{k['id'][:4]}]"
            self._nhan_ky[nhan] = k["id"]
        gia_tri = list(self._nhan_ky) + [TAT_CA]
        self.cb_ky.configure(values=gia_tri)
        hien_tai = self.v_ky.get()
        if chon_id:
            hien_tai = next((n for n, i in self._nhan_ky.items() if i == chon_id), hien_tai)
        if hien_tai not in gia_tri:
            hien_tai = gia_tri[0]
        self.v_ky.set(hien_tai)

    def ky_id_dang_chon(self):
        return self._nhan_ky.get(self.v_ky.get())

    # ---------------- chuyển trang ----------------
    def chuyen_trang(self, khoa):
        if self.trang_hien_tai:
            self.trang[self.trang_hien_tai].grid_forget()
        self.trang_hien_tai = khoa
        for k, b in self.nut_menu.items():
            b.configure(fg_color=THE if k == khoa else "transparent")
        self.lbl_tieu_de.configure(text=next(n for k, n, _ in MENU if k == khoa).split("  ", 1)[1])
        tr = self.trang[khoa]
        tr.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 12))
        tr.lam_moi()

    def lam_moi_tat_ca(self):
        """Làm mới trang đang hiển thị (các trang khác tự làm mới khi được mở)."""
        if self.trang_hien_tai:
            self.trang[self.trang_hien_tai].lam_moi()


def chay():
    app = UngDung()
    app.mainloop()
