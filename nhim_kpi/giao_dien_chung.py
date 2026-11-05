# -*- coding: utf-8 -*-
"""Bảng màu pastel, phông chữ và các widget dùng chung."""
import os
import subprocess
import sys
import tkinter as tk
from datetime import date

import customtkinter as ctk

from .nhim import ve_nhim

# ---------- Bảng màu pastel ngọt ngào ----------
NEN = "#FFF7F2"          # kem sữa
THE = "#FFFFFF"          # nền thẻ
VIEN = "#F3DCD4"
CHU = "#5B4A4A"
CHU_NHAT = "#9C8A8A"
HONG = "#F9C6D3"
HONG_DAM = "#F28AA8"
BAC_HA = "#C9EBDD"
BAC_HA_DAM = "#6CC4A1"
XANH = "#D4E4F8"
XANH_DAM = "#7FA8E0"
VANG = "#FCEFC2"
VANG_DAM = "#F2C45A"
TIM = "#E6DAF6"
TIM_DAM = "#A98BD9"
NAU = "#B98B6E"

if sys.platform == "win32":
    PHONG = "Segoe UI"
elif sys.platform == "darwin":
    PHONG = "Helvetica Neue"
else:
    PHONG = "DejaVu Sans"

_bo_nho_font = {}


def F(co=13, dam=False):
    """Phông chữ CTk (có bộ nhớ đệm)."""
    khoa = (co, dam)
    if khoa not in _bo_nho_font:
        _bo_nho_font[khoa] = ctk.CTkFont(family=PHONG, size=co, weight="bold" if dam else "normal")
    return _bo_nho_font[khoa]


def ti_le(widget):
    """Hệ số phóng to màn hình (để canvas/treeview không bị nhỏ trên màn hình HiDPI)."""
    try:
        return ctk.ScalingTracker.get_widget_scaling(widget)
    except Exception:
        return 1.0


# ---------- Ngày tháng ----------
def hien_ngay(iso):
    """'2026-01-31' -> '31/01/2026'."""
    if not iso:
        return ""
    try:
        return date.fromisoformat(iso).strftime("%d/%m/%Y")
    except ValueError:
        return iso


def doc_ngay_nhap(chuoi, ten_truong):
    """'31/01/2026' -> '2026-01-31'. Chuỗi rỗng -> ''. Sai định dạng -> ValueError."""
    chuoi = (chuoi or "").strip()
    if not chuoi:
        return ""
    for ky_tu in ("-", "."):
        chuoi = chuoi.replace(ky_tu, "/")
    try:
        d, m, y = (int(x) for x in chuoi.split("/"))
        return date(y, m, d).isoformat()
    except (ValueError, TypeError):
        raise ValueError(f"{ten_truong} không hợp lệ (định dạng dd/mm/yyyy).")


def thanh_tien_do_chu(ty_le_ht, do_dai=10):
    """Thanh tiến độ dạng ký tự cho Treeview."""
    ty_le_ht = max(0.0, min(1.0, ty_le_ht))
    day = round(ty_le_ht * do_dai)
    return "█" * day + "░" * (do_dai - day) + f"  {ty_le_ht * 100:.0f}%"


def mo_tep(duong_dan):
    """Mở tệp bằng ứng dụng mặc định của hệ điều hành."""
    if sys.platform == "win32":
        os.startfile(duong_dan)  # noqa
    elif sys.platform == "darwin":
        subprocess.Popen(["open", duong_dan])
    else:
        subprocess.Popen(["xdg-open", duong_dan])


# ---------- Widget dùng chung ----------
class The(ctk.CTkFrame):
    """Thẻ bo góc màu trắng, viền hồng nhạt."""

    def __init__(self, master, mau=THE, **kw):
        kw.setdefault("corner_radius", 18)
        super().__init__(master, fg_color=mau, border_width=2, border_color=VIEN, **kw)


def nut(master, text, command, mau=HONG_DAM, mau_hover=None, mau_chu="white", **kw):
    kw.setdefault("corner_radius", 14)
    kw.setdefault("height", 36)
    return ctk.CTkButton(master, text=text, command=command, fg_color=mau,
                         hover_color=mau_hover or mau, text_color=mau_chu, font=F(13, True), **kw)


class CanvasNhim(tk.Canvas):
    """Canvas vẽ một chú nhím, tự vẽ lại khi đổi tâm trạng/tiến độ."""

    def __init__(self, master, kich_thuoc=160, mau_nen=THE, tam_trang="binh_thuong", tien_do=None):
        k = int(kich_thuoc * ti_le(master))
        super().__init__(master, width=k, height=k, bg=mau_nen, highlightthickness=0, bd=0)
        self.k = k
        self.ve(tam_trang, tien_do)

    def ve(self, tam_trang="binh_thuong", tien_do=None):
        self.delete("all")
        ve_nhim(self, self.k / 2, self.k * 0.47, self.k * 0.36, tam_trang, tien_do)


class BangDong(ctk.CTkFrame):
    """Bảng nhập nhiều dòng (chỉ tiêu, kết quả then chốt, công việc...).
    cot = [(khoá, nhãn, độ rộng, kiểu)] với kiểu ∈ {"chu", "so", "check", "chon:<a|b|c>"}"""

    def __init__(self, master, cot, tieu_de, nhan_them="+ Tạo mới", **kw):
        super().__init__(master, fg_color=NEN, corner_radius=14, **kw)
        self.cot = cot
        self.dong = []   # mỗi dòng: (frame, {khoá: widget/biến})
        dau = ctk.CTkFrame(self, fg_color="transparent")
        dau.pack(fill="x", padx=10, pady=(8, 2))
        ctk.CTkLabel(dau, text=tieu_de, font=F(13, True), text_color=CHU).pack(side="left")
        nut(dau, nhan_them, self.them_dong, mau=BAC_HA_DAM, width=90, height=28).pack(side="right")
        tieu_de_cot = ctk.CTkFrame(self, fg_color="transparent")
        tieu_de_cot.pack(fill="x", padx=10)
        for _, nhan, rong, _ in cot:
            ctk.CTkLabel(tieu_de_cot, text=nhan, width=rong, anchor="w", font=F(11, True),
                         text_color=CHU_NHAT).pack(side="left", padx=3)
        self.than = ctk.CTkFrame(self, fg_color="transparent")
        self.than.pack(fill="x", padx=10, pady=(0, 8))

    def them_dong(self, du_lieu=None):
        du_lieu = du_lieu or {}
        khung = ctk.CTkFrame(self.than, fg_color="transparent")
        khung.pack(fill="x", pady=2)
        o = {}
        for khoa, _, rong, kieu in self.cot:
            if kieu == "check":
                bien = tk.BooleanVar(value=bool(du_lieu.get(khoa)))
                ctk.CTkCheckBox(khung, text="", variable=bien, width=rong, fg_color=BAC_HA_DAM,
                                hover_color=BAC_HA_DAM).pack(side="left", padx=3)
                o[khoa] = bien
            elif kieu.startswith("chon:"):
                gia_tri = kieu[5:].split("|")
                bien = tk.StringVar(value=str(du_lieu.get(khoa) or gia_tri[0]))
                ctk.CTkComboBox(khung, values=gia_tri, variable=bien, width=rong).pack(side="left", padx=3)
                o[khoa] = bien
            else:
                e = ctk.CTkEntry(khung, width=rong)
                gt = du_lieu.get(khoa)
                if gt not in (None, ""):
                    e.insert(0, f"{gt:g}" if isinstance(gt, (int, float)) else str(gt))
                e.pack(side="left", padx=3)
                o[khoa] = e
        ctk.CTkButton(khung, text="✕", width=28, height=28, fg_color=HONG, hover_color=HONG_DAM,
                      text_color=CHU, command=lambda: self._xoa(khung)).pack(side="left", padx=3)
        self.dong.append((khung, o))

    def _xoa(self, khung):
        self.dong = [(k, o) for k, o in self.dong if k is not khung]
        khung.destroy()

    def dat_du_lieu(self, ds):
        for k, _ in self.dong:
            k.destroy()
        self.dong = []
        for d in ds:
            self.them_dong(d)

    def lay_du_lieu(self):
        """Đọc dữ liệu; số không hợp lệ -> ValueError."""
        kq = []
        for _, o in self.dong:
            ban_ghi, rong_het = {}, True
            for khoa, nhan, _, kieu in self.cot:
                w = o[khoa]
                if kieu == "check":
                    ban_ghi[khoa] = bool(w.get())
                    continue
                gt = w.get().strip()
                if gt:
                    rong_het = False
                if kieu == "so":
                    if gt == "":
                        ban_ghi[khoa] = 0
                    else:
                        try:
                            ban_ghi[khoa] = float(gt.replace(",", "."))
                        except ValueError:
                            raise ValueError(f"«{nhan}» phải là số (đang nhập: {gt}).")
                        if ban_ghi[khoa] < 0:
                            raise ValueError(f"«{nhan}» không được âm.")
                else:
                    ban_ghi[khoa] = gt
            if not rong_het:
                kq.append(ban_ghi)
        return kq
