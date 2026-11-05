# -*- coding: utf-8 -*-
"""TRANG MỤC TIÊU – Cây mục tiêu cha/con: Thêm / Sửa / Xoá / Lịch sử cập nhật."""
import os
import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from . import tinh_diem as td
from .cau_hinh import TT_HOAN_THANH, TT_QUA_HAN, TT_CHUA_BAT_DAU
from .giao_dien_chung import (F, NEN, THE, CHU, CHU_NHAT, HONG, HONG_DAM, BAC_HA, BAC_HA_DAM, XANH,
                              XANH_DAM, VANG, TIM, TIM_DAM, The, nut, CanvasNhim, hien_ngay,
                              thanh_tien_do_chu, mo_tep, ti_le)
from .hop_thoai import HopThoaiMucTieu

BIEU_TUONG_TT = {TT_HOAN_THANH: "🌟", TT_QUA_HAN: "⏰", TT_CHUA_BAT_DAU: "💤"}


class TrangMucTieu(ctk.CTkFrame):
    COT = [("loai", "Loại", 60), ("nguoi", "Người thực hiện", 140), ("thoi_gian", "Thời gian thực hiện", 180),
           ("trong_so", "Trọng số", 75), ("tien_do", "Tiến độ", 170), ("trang_thai", "Trạng thái", 130)]

    def __init__(self, master, app):
        super().__init__(master, fg_color=NEN)
        self.app = app

        # ---- Thanh công cụ ----
        thanh = ctk.CTkFrame(self, fg_color="transparent")
        thanh.pack(fill="x", padx=6, pady=(4, 8))
        nut(thanh, "＋ Thêm mới", self.them, mau=HONG_DAM).pack(side="left", padx=3)
        nut(thanh, "＋ Mục tiêu con", self.them_con, mau=TIM_DAM).pack(side="left", padx=3)
        nut(thanh, "✏️ Sửa", self.sua, mau=XANH_DAM).pack(side="left", padx=3)
        nut(thanh, "🗑️ Xoá", self.xoa, mau=HONG, mau_chu=CHU).pack(side="left", padx=3)
        nut(thanh, "🕘 Lịch sử cập nhật", self.lich_su, mau=BAC_HA_DAM).pack(side="left", padx=3)
        nut(thanh, "📎 Tệp minh chứng", self.mo_tep_dinh_kem, mau=VANG, mau_chu=CHU).pack(side="left", padx=3)
        nut(thanh, "⟳ Làm mới", self.lam_moi, mau=THE, mau_chu=CHU).pack(side="right", padx=3)

        than = ctk.CTkFrame(self, fg_color="transparent")
        than.pack(fill="both", expand=True)

        # ---- Khung trái: số lượng mục tiêu ----
        self.trai = The(than, width=250)
        self.trai.pack(side="left", fill="y", padx=6, pady=4)
        self.trai.pack_propagate(False)

        # ---- Khung giữa: cây mục tiêu ----
        giua = The(than)
        giua.pack(side="left", fill="both", expand=True, padx=6, pady=4)
        ctk.CTkLabel(giua, text="🌳  Cây mục tiêu  (nhấp đúp để chỉnh sửa)", font=F(15, True),
                     text_color=CHU).pack(anchor="w", padx=16, pady=(12, 6))
        khung_cay = tk.Frame(giua, bg=THE)
        khung_cay.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self._kieu_cay()
        self.cay = ttk.Treeview(khung_cay, columns=[c[0] for c in self.COT], style="Nhim.Treeview")
        self.cay.heading("#0", text="Mục tiêu")
        self.cay.column("#0", width=int(320 * ti_le(self)), minwidth=200)
        for khoa, nhan, rong in self.COT:
            self.cay.heading(khoa, text=nhan)
            self.cay.column(khoa, width=int(rong * ti_le(self)), anchor="center")
        cuon = ctk.CTkScrollbar(khung_cay, command=self.cay.yview)
        self.cay.configure(yscrollcommand=cuon.set)
        self.cay.pack(side="left", fill="both", expand=True)
        cuon.pack(side="right", fill="y")
        self.cay.bind("<Double-1>", lambda e: self.sua())
        for tt, mau in ((TT_HOAN_THANH, "#E9F7F0"), (TT_QUA_HAN, "#FDEBEF"), (TT_CHUA_BAT_DAU, "#F3EEFB")):
            self.cay.tag_configure(tt, background=mau)

    def _kieu_cay(self):
        k = ti_le(self)
        st = ttk.Style()
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("Nhim.Treeview", background=THE, fieldbackground=THE, foreground=CHU,
                     rowheight=int(32 * k), font=(F().cget("family"), 11), borderwidth=0)
        st.configure("Nhim.Treeview.Heading", background=HONG, foreground=CHU, relief="flat",
                     font=(F().cget("family"), 11, "bold"), padding=6)
        st.map("Nhim.Treeview", background=[("selected", "#F7D6E0")], foreground=[("selected", CHU)])
        st.map("Nhim.Treeview.Heading", background=[("active", HONG_DAM)])

    # ------------------------------------------------------------------
    def lam_moi(self):
        kho, ch = self.app.kho, self.app.kho.cau_hinh
        ky_id = self.app.ky_id_dang_chon()
        ds = kho.ds_muc_tieu
        self.cay.delete(*self.cay.get_children())
        ds_ky = td.muc_tieu_trong_ky(ky_id, ds)
        ids = {m["id"] for m in ds_ky}

        def chen(cha_tree, cha_id):
            for m in ds_ky:
                pid = m.get("parent_id") if m.get("parent_id") in ids else None
                if pid != cha_id:
                    continue
                p = td.tien_do(m, ds, ch)
                tt = td.trang_thai(m, p)
                self.cay.insert(cha_tree, "end", iid=m["id"], open=True, tags=(tt,),
                                text=f"{BIEU_TUONG_TT.get(tt, '🌰')} {m['ten']}",
                                values=(m["loai"], m.get("nguoi_thuc_hien") or "–",
                                        f"{hien_ngay(m['ngay_bat_dau'])} – {hien_ngay(m['ngay_ket_thuc'])}",
                                        f"{m['trong_so']:g}%", thanh_tien_do_chu(p), tt))
                chen(m["id"], m["id"])
        chen("", None)
        self._ve_khung_trai(ky_id, ds_ky)

    def _ve_khung_trai(self, ky_id, ds_ky):
        for w in self.trai.winfo_children():
            w.destroy()
        kho, ch = self.app.kho, self.app.kho.cau_hinh
        tk_ = td.thong_ke(ky_id, kho.ds_muc_tieu, ch)
        tam = "ngu" if not tk_["tong"] else ("buon" if tk_["theo_trang_thai"][TT_QUA_HAN] else "vui")
        CanvasNhim(self.trai, 120, THE, tam).pack(pady=(12, 0))
        ctk.CTkLabel(self.trai, text="Số lượng mục tiêu", font=F(14, True), text_color=CHU).pack()
        ctk.CTkLabel(self.trai, text=str(tk_["tong"]), font=F(30, True), text_color=HONG_DAM).pack()
        for nhan, so_luong, mau in (("KPI", tk_["kpi"], XANH), ("OKR", tk_["okr"], TIM)):
            ctk.CTkLabel(self.trai, text=f"{nhan}: {so_luong}", font=F(13, True), text_color=CHU,
                         fg_color=mau, corner_radius=10, width=150).pack(pady=3)
        ctk.CTkLabel(self.trai, text="Mục tiêu được giao", font=F(13, True), text_color=CHU).pack(pady=(12, 4))
        for m in ds_ky[:8]:
            p = td.tien_do(m, kho.ds_muc_tieu, ch)
            ctk.CTkLabel(self.trai, text=m["ten"][:30] + ("…" if len(m["ten"]) > 30 else ""), font=F(11),
                         text_color=CHU_NHAT, anchor="w").pack(fill="x", padx=14)
            pb = ctk.CTkProgressBar(self.trai, height=8, progress_color=BAC_HA_DAM, fg_color="#EFE3DE")
            pb.set(min(p, 1.0))
            pb.pack(fill="x", padx=14, pady=(0, 4))
        for c in td.kiem_tra_trong_so(kho.ds_muc_tieu, ky_id)[:3] if ky_id else []:
            ctk.CTkLabel(self.trai, text="⚠️ " + c, font=F(11), text_color=HONG_DAM, wraplength=int(210 * ti_le(self)),
                         justify="left").pack(padx=10, pady=2)

    # ------------------------------------------------------------------
    def _chon(self, bao=True):
        sel = self.cay.selection()
        if not sel:
            if bao:
                messagebox.showinfo("Nhím nhắc nhẹ 🦔", "Hãy chọn một mục tiêu trong cây trước nhé.")
            return None
        return self.app.kho.tim_muc_tieu(sel[0])

    def _can_ky(self):
        ky_id = self.app.ky_id_dang_chon()
        if not ky_id:
            messagebox.showinfo("Chọn kỳ mục tiêu", "Hãy chọn một kỳ mục tiêu cụ thể ở thanh trên cùng "
                                                     "(hoặc tạo kỳ mới ở mục 📅 Kỳ mục tiêu).")
        return ky_id

    def _mo_hop_thoai(self, ky_id, mt=None, parent_id=None):
        hop = HopThoaiMucTieu(self.app, self.app.kho, ky_id, mt, parent_id)
        self.app.wait_window(hop)
        if hop.ket_qua:
            self.app.kho.luu_muc_tieu(hop.ket_qua, "Tạo mới mục tiêu" if mt is None else "Chỉnh sửa mục tiêu")
            self.app.lam_moi_tat_ca()

    def them(self):
        ky_id = self._can_ky()
        if ky_id:
            self._mo_hop_thoai(ky_id)

    def them_con(self):
        cha = self._chon()
        if cha:
            self._mo_hop_thoai(cha["ky_id"], parent_id=cha["id"])

    def sua(self):
        mt = self._chon()
        if mt:
            self._mo_hop_thoai(mt["ky_id"], mt)

    def xoa(self):
        mt = self._chon()
        if not mt:
            return
        so_con = len(self.app.kho.hau_due(mt["id"]))
        thong_bao = f"Xoá mục tiêu «{mt['ten']}»?"
        if so_con:
            thong_bao += f"\n\n⚠️ {so_con} mục tiêu con bên trong cũng sẽ bị xoá."
        if messagebox.askyesno("Xác nhận xoá", thong_bao, icon="warning"):
            self.app.kho.xoa_muc_tieu(mt["id"])
            self.app.lam_moi_tat_ca()

    def lich_su(self):
        mt = self._chon()
        if not mt:
            return
        dong = [f"• {x['thoi_gian']} — {x['noi_dung']}" for x in reversed(mt.get("lich_su", []))]
        messagebox.showinfo(f"Lịch sử cập nhật – {mt['ten']}", "\n".join(dong) or "Chưa có lịch sử.")

    def mo_tep_dinh_kem(self):
        mt = self._chon()
        if not mt:
            return
        tep = [p for p in mt.get("tep_dinh_kem", []) if os.path.exists(p)]
        if not tep:
            messagebox.showinfo("Tệp minh chứng", "Mục tiêu này chưa có tệp minh chứng (hoặc tệp đã bị di chuyển).")
            return
        for p in tep:
            mo_tep(p)
