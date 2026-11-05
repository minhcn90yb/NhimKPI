# -*- coding: utf-8 -*-
"""
CẤU HÌNH NGHIỆP VỤ (bám sát tài liệu HDSD eKPI)
------------------------------------------------
Toàn bộ thang điểm, tiêu chí và ngưỡng xếp loại được để ở đây và được ghi ra
file `cau_hinh.json` trong thư mục dữ liệu. Khi đơn vị thay đổi quy định,
chỉ cần sửa file JSON đó, KHÔNG cần sửa mã nguồn.
"""

# ---- Hằng số danh mục (lấy từ các trường thông tin trong tài liệu) ----
LOAI_MUC_TIEU = ["KPI", "OKR"]

PT_CHI_TIEU = "Theo chỉ tiêu / kết quả then chốt"
PT_TONG_HOP_CON = "Tự động tổng hợp từ mục tiêu con"
PT_CONG_VIEC = "Tổng hợp từ dự án hoặc danh sách công việc"
PHUONG_THUC_DANH_GIA = [PT_CHI_TIEU, PT_TONG_HOP_CON, PT_CONG_VIEC]

LOAI_NGUON = ["Dự án", "Danh sách công việc"]
DOI_TUONG_MUC_TIEU = ["Cá nhân", "Phòng ban", "Đơn vị", "Bộ/Ngành"]
LOAI_KY = ["Năm", "Quý", "Tháng"]
TIEU_CHI_KY = ["Tiêu chí kết quả công việc", "Tiêu chí chung"]
TRANG_THAI_KY = ["Bản nháp", "Đang thực hiện", "Đã kết thúc"]

# Trạng thái mục tiêu (4 thẻ chỉ số trên màn hình Kết quả thực hiện)
TT_HOAN_THANH = "Hoàn thành"
TT_DANG_THUC_HIEN = "Đang thực hiện"
TT_QUA_HAN = "Quá hạn"
TT_CHUA_BAT_DAU = "Chưa bắt đầu"

# Trạng thái phiếu đánh giá (luồng: Tự đánh giá → Cấp trên → Cấp thẩm quyền)
PHIEU_NHAP = "Lưu nháp"
PHIEU_DA_GUI = "Đã gửi đánh giá"

# ---- Cấu hình mặc định ----
CAU_HINH_MAC_DINH = {
    "phien_ban": 1,
    "ghi_chu": (
        "Thang 120 điểm theo phiếu đánh giá trong HDSD eKPI: Nhóm I (30) + "
        "Nhóm II (70 = Điểm KPI quy đổi x 70) + Nhóm III điểm cộng (tối đa 20, "
        "không quá 30% điểm Nhóm II). Ngưỡng xếp loại suy ra từ ví dụ trong "
        "tài liệu, hãy đối chiếu quy định của đơn vị và sửa nếu cần."
    ),
    "tong_diem_toi_da": 120,
    # Trần tỷ lệ hoàn thành của một chỉ tiêu (1.0 = tối đa 100%)
    "tran_ty_le_hoan_thanh": 1.0,
    "don_vi_tinh_mac_dinh": ["Văn bản", "Báo cáo", "Hồ sơ", "Bản / Tờ"],

    # NHÓM I – TIÊU CHÍ CHUNG (30 điểm)
    "nhom_I": {
        "ma": "I",
        "ten": "NHÓM TIÊU CHÍ CHUNG",
        "diem_toi_da": 30,
        "muc": [
            {
                "ma": "1",
                "ten": "Về chính trị, phẩm chất đạo đức và ý thức tổ chức kỷ luật",
                "tieu_chi": [
                    {"ma": "1.1", "diem_toi_da": 2,
                     "ten": "Có quan điểm, bản lĩnh chính trị vững vàng; kiên định lập trường; "
                            "nghiên cứu, học tập, vận dụng chủ nghĩa Mác - Lênin, tư tưởng Hồ Chí Minh, "
                            "nghị quyết, chỉ thị, quyết định của Đảng, Nhà nước, Tòa án nhân dân."},
                    {"ma": "1.2", "diem_toi_da": 2,
                     "ten": "Thực hiện nghiêm nguyên tắc tổ chức và hoạt động của Đảng, nhất là tập trung "
                            "dân chủ, tự phê bình và phê bình; chấp hành đường lối, chính sách, pháp luật, "
                            "quy chế, quy định của TAND và cơ quan, đơn vị."},
                    {"ma": "1.3", "diem_toi_da": 2,
                     "ten": "Giữ gìn phẩm chất đạo đức, lối sống trong sáng, trung thực, khiêm tốn; tích cực "
                            "đấu tranh phòng, chống tham nhũng, lãng phí, tiêu cực; không vi phạm những điều "
                            "đảng viên, công chức TAND không được làm."},
                    {"ma": "1.4", "diem_toi_da": 9,
                     "ten": "[...] Các tiêu chí còn lại của mục 1 – bổ sung theo mẫu phiếu của đơn vị."},
                ],
            },
            {
                "ma": "2",
                "ten": "[...] Mục 2 – bổ sung tên và tiêu chí theo mẫu phiếu của đơn vị",
                "tieu_chi": [
                    {"ma": "2.1", "diem_toi_da": 10,
                     "ten": "[...] Tiêu chí mục 2 – bổ sung theo mẫu phiếu của đơn vị."},
                ],
            },
            {
                "ma": "3",
                "ten": "Tinh thần tự phê bình, tự soi, tự sửa",
                "tieu_chi": [
                    {"ma": "3.1", "diem_toi_da": 5,
                     "ten": "Tinh thần tự phê bình, tự soi, tự sửa của cá nhân; mức độ tự giác nhận diện "
                            "hạn chế, khuyết điểm của bản thân và kết quả khắc phục hạn chế, khuyết điểm "
                            "đã được chỉ ra (nếu có)."},
                ],
            },
        ],
    },

    # NHÓM II – KẾT QUẢ THỰC HIỆN CHỨC TRÁCH, NHIỆM VỤ (70 điểm)
    "nhom_II": {
        "ma": "II",
        "ten": "NHÓM TIÊU CHÍ VỀ KẾT QUẢ THỰC HIỆN CHỨC TRÁCH, NHIỆM VỤ ĐƯỢC GIAO",
        "diem_toi_da": 70,
        "he_so_quy_doi": 70,
        "giai_thich": "Điểm = Điểm KPI quy đổi (x) 70. Điểm KPI quy đổi = bình quân gia quyền "
                      "tiến độ các mục tiêu gốc trong kỳ theo trọng số (%).",
        "tieu_chi_tham_khao": [
            "Số lượng kết quả thực hiện nhiệm vụ",
            "Chất lượng kết quả thực hiện nhiệm vụ",
            "Tiến độ kết quả thực hiện nhiệm vụ",
        ],
    },

    # NHÓM III – ĐIỂM CỘNG DO CẤP CÓ THẨM QUYỀN QUYẾT ĐỊNH (20 điểm)
    "nhom_III": {
        "ma": "III",
        "ten": "ĐIỂM CỘNG DO CẤP CÓ THẨM QUYỀN THEO DÕI, ĐÁNH GIÁ QUYẾT ĐỊNH",
        "diem_toi_da": 20,
        "ty_le_toi_da_so_voi_nhom_II": 0.30,
    },

    # 4 NHÓM XẾP LOẠI (sắp xếp từ cao xuống thấp; "diem_tu" là ngưỡng dưới, đơn vị: điểm/120)
    "xep_loai": [
        {"ten": "Hoàn thành xuất sắc nhiệm vụ", "diem_tu": 90, "mau": "#6CC4A1",
         "tam_trang": "phan_khich", "ty_le_toi_da": 0.20},
        {"ten": "Hoàn thành tốt nhiệm vụ", "diem_tu": 70, "mau": "#7FA8E0",
         "tam_trang": "vui", "ty_le_toi_da": None},
        {"ten": "Hoàn thành nhiệm vụ", "diem_tu": 50, "mau": "#F2C45A",
         "tam_trang": "binh_thuong", "ty_le_toi_da": None},
        {"ten": "Không hoàn thành nhiệm vụ", "diem_tu": 0, "mau": "#F28AA8",
         "tam_trang": "buon", "ty_le_toi_da": None},
    ],
}


def cac_tieu_chi_nhom_I(cau_hinh):
    """Trả về danh sách phẳng các tiêu chí lá của Nhóm I."""
    ds = []
    for muc in cau_hinh["nhom_I"]["muc"]:
        ds.extend(muc["tieu_chi"])
    return ds


def hop_nhat_cau_hinh(mac_dinh, nguoi_dung):
    """Bổ sung các khoá còn thiếu từ cấu hình mặc định (giữ nguyên giá trị người dùng đã sửa)."""
    if not isinstance(nguoi_dung, dict):
        return mac_dinh
    kq = dict(mac_dinh)
    for k, v in nguoi_dung.items():
        if k in mac_dinh and isinstance(mac_dinh[k], dict) and isinstance(v, dict):
            kq[k] = hop_nhat_cau_hinh(mac_dinh[k], v)
        else:
            kq[k] = v
    return kq
