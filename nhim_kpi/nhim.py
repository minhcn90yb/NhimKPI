# -*- coding: utf-8 -*-
"""
CHÚ NHÍM CHIBI – vẽ hoàn toàn bằng tkinter.Canvas (không cần file ảnh)
-----------------------------------------------------------------------
Tâm trạng:
  "phan_khich"  – Hoàn thành xuất sắc (mắt cười, miệng mở, lấp lánh)
  "vui"         – Đạt KPI / hoàn thành tốt
  "binh_thuong" – Đang thực hiện (mắt tròn long lanh)
  "buon"        – Trễ hạn / không hoàn thành (mắt buồn, giọt nước mắt)
  "ngu"         – Chưa có dữ liệu
Tham số `tien_do` (0..1): nhím ôm quả thông, các tầng vảy được tô màu theo tiến độ.
"""
import math

MAU_GAI = "#B98B6E"
MAU_VIEN_GAI = "#9C6F55"
MAU_THAN = "#CFA285"
MAU_MAT_NHIM = "#FDEBDC"
MAU_MA_HONG = "#F7A8BC"
MAU_DEN = "#4A3A3A"
MAU_THONG_DAY = "#A0663F"
MAU_THONG_RONG = "#EADBCF"
MAU_LA = "#8CCB9E"

LOI_NHIM = {
    "phan_khich": "Tuyệt vời quá! Nhím tự hào về bạn lắm 🌟",
    "vui": "Giỏi quá! Cứ thế phát huy nha 💖",
    "binh_thuong": "Nhím đang ôm quả thông cố gắng cùng bạn 🌰",
    "buon": "Huhu... có việc trễ hạn rồi, mình cùng xử lý nhé 🥺",
    "ngu": "Chưa có dữ liệu... Nhím ngủ một chút đã 💤",
}


def ve_nhim(cv, cx, cy, s, tam_trang="binh_thuong", tien_do=None):
    """Vẽ một chú nhím tâm (cx, cy), bán kính ~ s lên canvas `cv`."""
    # --- Gai (vòng gai răng cưa quanh thân) ---
    n = 26
    diem = []
    for i in range(n * 2):
        goc = math.pi * 2 * i / (n * 2) - math.pi / 2
        r = s * (1.06 if i % 2 == 0 else 0.84)
        diem += [cx + r * math.cos(goc), cy + r * math.sin(goc) * 0.95]
    cv.create_polygon(diem, fill=MAU_GAI, outline=MAU_VIEN_GAI, width=2, joinstyle="round")

    # --- Tai ---
    for d in (-1, 1):
        tx = cx + d * s * 0.48
        cv.create_oval(tx - s * 0.17, cy - s * 0.72, tx + s * 0.17, cy - s * 0.40,
                       fill=MAU_MAT_NHIM, outline=MAU_VIEN_GAI, width=2)
        cv.create_oval(tx - s * 0.08, cy - s * 0.63, tx + s * 0.08, cy - s * 0.47,
                       fill=MAU_MA_HONG, outline="")

    # --- Thân & mặt ---
    cv.create_oval(cx - s * 0.84, cy - s * 0.74, cx + s * 0.84, cy + s * 0.80, fill=MAU_THAN, outline="")
    cv.create_oval(cx - s * 0.66, cy - s * 0.46, cx + s * 0.66, cy + s * 0.74, fill=MAU_MAT_NHIM, outline="")

    # --- Mắt ---
    my, mx, rm = cy + s * 0.04, s * 0.27, s * 0.10
    for d in (-1, 1):
        x = cx + d * mx
        if tam_trang in ("vui", "phan_khich"):
            # mắt cười ^ ^
            cv.create_arc(x - rm, my - rm * 0.6, x + rm, my + rm * 1.4, start=20, extent=140,
                          style="arc", outline=MAU_DEN, width=max(2, int(s * 0.05)))
        elif tam_trang == "ngu":
            cv.create_line(x - rm, my + rm * 0.3, x + rm, my + rm * 0.3, fill=MAU_DEN,
                           width=max(2, int(s * 0.04)), capstyle="round")
        else:
            cv.create_oval(x - rm, my - rm * 1.1, x + rm, my + rm * 1.1, fill=MAU_DEN, outline="")
            cv.create_oval(x - rm * 0.15, my - rm * 0.85, x + rm * 0.55, my - rm * 0.15,
                           fill="white", outline="")
            cv.create_oval(x - rm * 0.55, my + rm * 0.30, x - rm * 0.20, my + rm * 0.65,
                           fill="white", outline="")
            if tam_trang == "buon":   # lông mày cụp
                cv.create_line(x - d * rm * 1.2, my - rm * 1.9, x + d * rm * 0.9, my - rm * 1.4,
                               fill=MAU_DEN, width=max(2, int(s * 0.03)), capstyle="round")

    # --- Má hồng ---
    for d in (-1, 1):
        x = cx + d * s * 0.43
        cv.create_oval(x - s * 0.11, my + s * 0.13, x + s * 0.11, my + s * 0.24,
                       fill=MAU_MA_HONG, outline="")

    # --- Mũi & miệng ---
    ny = cy + s * 0.20
    cv.create_oval(cx - s * 0.06, ny - s * 0.04, cx + s * 0.06, ny + s * 0.04, fill=MAU_DEN, outline="")
    w = max(2, int(s * 0.035))
    if tam_trang == "phan_khich":
        cv.create_arc(cx - s * 0.13, ny - s * 0.02, cx + s * 0.13, ny + s * 0.24, start=180, extent=180,
                      style="pieslice", fill="#E86F8C", outline=MAU_DEN, width=w)
    elif tam_trang == "vui":
        cv.create_arc(cx - s * 0.12, ny - s * 0.06, cx + s * 0.12, ny + s * 0.16, start=200, extent=140,
                      style="arc", outline=MAU_DEN, width=w)
    elif tam_trang == "buon":
        cv.create_arc(cx - s * 0.10, ny + s * 0.08, cx + s * 0.10, ny + s * 0.24, start=20, extent=140,
                      style="arc", outline=MAU_DEN, width=w)
        # giọt nước mắt
        tx, ty = cx + mx + s * 0.04, my + s * 0.14
        cv.create_polygon(tx, ty, tx - s * 0.05, ty + s * 0.10, tx + s * 0.05, ty + s * 0.10,
                          fill="#9FD3F5", outline="")
        cv.create_oval(tx - s * 0.05, ty + s * 0.05, tx + s * 0.05, ty + s * 0.15, fill="#9FD3F5", outline="")
    elif tam_trang == "ngu":
        cv.create_oval(cx - s * 0.04, ny + s * 0.07, cx + s * 0.04, ny + s * 0.14, outline=MAU_DEN, width=w)
        cv.create_text(cx + s * 0.85, cy - s * 0.85, text="z Z", fill="#9C8AC9",
                       font=("Arial", max(8, int(s * 0.22)), "bold"))
    else:  # bình thường: miệng chữ "w"
        cv.create_line(cx - s * 0.10, ny + s * 0.08, cx - s * 0.05, ny + s * 0.13, cx, ny + s * 0.08,
                       cx + s * 0.05, ny + s * 0.13, cx + s * 0.10, ny + s * 0.08,
                       fill=MAU_DEN, width=w, smooth=True, capstyle="round")

    # --- Chân ---
    for d in (-1, 1):
        x = cx + d * s * 0.42
        cv.create_oval(x - s * 0.17, cy + s * 0.70, x + s * 0.17, cy + s * 0.90,
                       fill=MAU_GAI, outline=MAU_VIEN_GAI, width=2)

    # --- Quả thông tiến độ (nhím ôm trước bụng) ---
    if tien_do is not None:
        ve_qua_thong(cv, cx, cy + s * 0.80, s * 0.26, tien_do)
        for d in (-1, 1):   # hai bàn tay ôm quả thông
            x = cx + d * s * 0.24
            cv.create_oval(x - s * 0.10, cy + s * 0.60, x + s * 0.10, cy + s * 0.74,
                           fill=MAU_MAT_NHIM, outline=MAU_VIEN_GAI, width=2)

    # --- Lấp lánh khi phấn khích ---
    if tam_trang == "phan_khich":
        for (dx, dy, mau) in ((-1.05, -0.95, "#F2C45A"), (1.05, -0.80, "#F28AA8"), (1.15, 0.25, "#7FA8E0")):
            ve_ngoi_sao(cv, cx + dx * s, cy + dy * s, s * 0.13, mau)


def ve_qua_thong(cv, cx, cy, r, tien_do):
    """Quả thông 6 tầng vảy; số tầng tô đậm (từ dưới lên) = tiến độ."""
    tien_do = max(0.0, min(1.0, tien_do or 0.0))
    so_tang = 6
    da_to = round(tien_do * so_tang)
    for i in range(so_tang):                      # i = 0 là tầng dưới cùng
        y = cy + r * 0.9 - i * r * 0.32
        do_rong = r * (0.55 + 0.45 * math.sin(math.pi * (i + 0.8) / (so_tang + 0.6)))
        mau = MAU_THONG_DAY if i < da_to else MAU_THONG_RONG
        cv.create_oval(cx - do_rong, y - r * 0.24, cx + do_rong, y + r * 0.24,
                       fill=mau, outline="#7A4E33", width=1)
    # lá trên đỉnh
    dinh = cy + r * 0.9 - (so_tang - 1) * r * 0.32 - r * 0.25
    cv.create_oval(cx - r * 0.35, dinh - r * 0.25, cx, dinh + r * 0.05, fill=MAU_LA, outline="")
    cv.create_oval(cx, dinh - r * 0.25, cx + r * 0.35, dinh + r * 0.05, fill=MAU_LA, outline="")


def ve_ngoi_sao(cv, cx, cy, r, mau):
    diem = []
    for i in range(8):
        goc = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.35
        diem += [cx + rr * math.cos(goc), cy + rr * math.sin(goc)]
    cv.create_polygon(diem, fill=mau, outline="")


def ve_bieu_do_tron(cv, cx, cy, r, du_lieu, mau_nen="#FFFFFF"):
    """Biểu đồ tròn (donut) – du_lieu: [(nhãn, giá trị, màu)]."""
    tong = sum(v for _, v, _ in du_lieu)
    if tong <= 0:
        cv.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#EEE6E6", outline="")
    else:
        bat_dau = 90.0
        for _, v, mau in du_lieu:
            if v <= 0:
                continue
            goc = 359.999 * v / tong
            cv.create_arc(cx - r, cy - r, cx + r, cy + r, start=bat_dau, extent=-goc,
                          fill=mau, outline=mau_nen, width=2, style="pieslice")
            bat_dau -= goc
    cv.create_oval(cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55, fill=mau_nen, outline="")
    cv.create_text(cx, cy - 6, text=str(int(tong)), font=("Arial", int(r * 0.28), "bold"), fill="#5B4A4A")
    cv.create_text(cx, cy + r * 0.22, text="mục tiêu", font=("Arial", max(8, int(r * 0.12))), fill="#9C8A8A")
