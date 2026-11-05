# -*- coding: utf-8 -*-
"""
LƯU TRỮ CỤC BỘ BẰNG JSON
------------------------
- Dữ liệu:   <thư mục người dùng>/NhimKPI/du_lieu_kpi.json
- Cấu hình:  <thư mục người dùng>/NhimKPI/cau_hinh.json
- Ghi an toàn: ghi ra file tạm rồi thay thế (os.replace) + giữ 1 bản .bak,
  nên dù mất điện giữa chừng cũng không hỏng dữ liệu.
"""
import json
import os
import shutil
import uuid
from datetime import date, datetime
from pathlib import Path

from .cau_hinh import (CAU_HINH_MAC_DINH, hop_nhat_cau_hinh, PT_CHI_TIEU,
                       PT_TONG_HOP_CON, PT_CONG_VIEC, PHIEU_NHAP)

THU_MUC_DU_LIEU = Path(os.environ.get("NHIM_KPI_HOME", Path.home() / "NhimKPI"))
FILE_DU_LIEU = THU_MUC_DU_LIEU / "du_lieu_kpi.json"
FILE_CAU_HINH = THU_MUC_DU_LIEU / "cau_hinh.json"


def tao_id():
    return uuid.uuid4().hex[:10]


def bay_gio():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def _ghi_json_an_toan(duong_dan: Path, du_lieu):
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    tam = duong_dan.with_suffix(".tmp")
    with open(tam, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, indent=2)
    if duong_dan.exists():
        shutil.copy2(duong_dan, duong_dan.with_suffix(".bak"))
    os.replace(tam, duong_dan)


def _doc_json(duong_dan: Path):
    """Đọc JSON; nếu file chính lỗi thì thử khôi phục từ bản .bak."""
    for p in (duong_dan, duong_dan.with_suffix(".bak")):
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
    return None


# ===================== Mẫu bản ghi =====================
def ky_moi(**kw):
    """Kỳ mục tiêu (theo màn hình 'Thêm mới kỳ mục tiêu')."""
    nam = date.today().year
    ban_ghi = {
        "id": tao_id(), "ten": "", "tieu_chi": "Tiêu chí kết quả công việc",
        "don_vi_so_huu": "", "loai": "Năm", "nam": nam, "so_ky": 1,
        "don_vi_tinh": list(CAU_HINH_MAC_DINH["don_vi_tinh_mac_dinh"]),
        "mo_ta": "", "trang_thai": "Đang thực hiện", "ngay_tao": bay_gio(),
    }
    ban_ghi.update(kw)
    return ban_ghi


def muc_tieu_moi(**kw):
    """Mục tiêu (theo màn hình 'Thêm mới mục tiêu' – loại KPI/OKR)."""
    ban_ghi = {
        "id": tao_id(), "ky_id": None, "parent_id": None,
        "loai": "KPI", "phuong_thuc": PT_CHI_TIEU,
        "ten": "", "trong_so": 0,
        "doi_tuong": "Cá nhân", "don_vi": "", "nguoi_thuc_hien": "", "nguoi_theo_doi": "",
        "ngay_bat_dau": "", "ngay_ket_thuc": "", "mo_ta": "",
        "ket_noi_cha": False, "cong_khai": False,
        # KPI: chỉ tiêu theo đơn vị tính
        "chi_tieu": [],            # [{don_vi_tinh, gia_tri_muc_tieu, gia_tri_dat, ty_trong}]
        # OKR: kết quả then chốt
        "ket_qua_then_chot": [],   # [{ten, gia_tri_muc_tieu, gia_tri_dat, ty_trong}]
        # Liên kết eTask
        "loai_nguon": "Danh sách công việc",
        "cong_viec": [],           # [{ten, hoan_thanh}]
        "tep_dinh_kem": [],        # [đường dẫn tệp minh chứng]
        "lich_su": [],             # [{thoi_gian, noi_dung}]
    }
    ban_ghi.update(kw)
    return ban_ghi


def phieu_moi(ky_id):
    """Phiếu đánh giá của một kỳ: điểm theo từng tiêu chí ở 3 cột."""
    return {"ky_id": ky_id, "trang_thai": PHIEU_NHAP, "diem": {},
            "y_kien": [], "ngay_cap_nhat": bay_gio()}


def du_lieu_mau():
    """Dữ liệu minh họa dựa trên các ví dụ trong tài liệu HDSD."""
    nam = date.today().year
    ky = ky_moi(ten=f"Nhiệm vụ công tác năm {nam}", don_vi_so_huu="Văn phòng",
                mo_ta="Kỳ mục tiêu minh họa – có thể sửa hoặc xoá.")
    cha = muc_tieu_moi(ky_id=ky["id"], ten=f"Công tác trọng tâm năm {nam}",
                       phuong_thuc=PT_TONG_HOP_CON, trong_so=100,
                       ngay_bat_dau=f"{nam}-01-01", ngay_ket_thuc=f"{nam}-12-31")
    mt1 = muc_tieu_moi(ky_id=ky["id"], parent_id=cha["id"], loai="KPI", trong_so=40,
                       ten=f"Ban hành văn bản quy phạm pháp luật {nam}",
                       ngay_bat_dau=f"{nam}-01-01", ngay_ket_thuc=f"{nam}-12-31",
                       chi_tieu=[{"don_vi_tinh": "Văn bản", "gia_tri_muc_tieu": 20,
                                  "gia_tri_dat": 12, "ty_trong": 100}])
    mt2 = muc_tieu_moi(ky_id=ky["id"], parent_id=cha["id"], loai="OKR", trong_so=30,
                       ten="Chuẩn hóa quy trình xử lý văn bản",
                       ngay_bat_dau=f"{nam}-01-01", ngay_ket_thuc=f"{nam}-06-30",
                       ket_qua_then_chot=[
                           {"ten": "Hoàn thiện quy trình", "gia_tri_muc_tieu": 1, "gia_tri_dat": 1, "ty_trong": 50},
                           {"ten": "Biên bản họp thống nhất quy trình", "gia_tri_muc_tieu": 2,
                            "gia_tri_dat": 1, "ty_trong": 50}])
    mt3 = muc_tieu_moi(ky_id=ky["id"], parent_id=cha["id"], loai="KPI", trong_so=30,
                       phuong_thuc=PT_CONG_VIEC, ten="Triển khai công tác Quy hoạch",
                       ngay_bat_dau=f"{nam}-03-01", ngay_ket_thuc=f"{nam}-12-15",
                       cong_viec=[{"ten": "Rà soát hồ sơ", "hoan_thanh": True},
                                  {"ten": "Tổng hợp báo cáo", "hoan_thanh": True},
                                  {"ten": "Trình phê duyệt", "hoan_thanh": False}])
    return {"phien_ban": 1, "nguoi_dung": {"ho_ten": "", "chuc_vu": "Chuyên viên", "don_vi": ""},
            "ky_muc_tieu": [ky], "muc_tieu": [cha, mt1, mt2, mt3], "phieu_danh_gia": {}}


# ===================== Kho dữ liệu =====================
class KhoDuLieu:
    """Đọc/ghi toàn bộ dữ liệu ứng dụng."""

    def __init__(self, file_du_lieu=FILE_DU_LIEU, file_cau_hinh=FILE_CAU_HINH):
        self.file_du_lieu = Path(file_du_lieu)
        self.file_cau_hinh = Path(file_cau_hinh)
        self.du_lieu = None
        self.cau_hinh = None
        self.tai()

    # ---------- đọc / ghi ----------
    def tai(self):
        ch = _doc_json(self.file_cau_hinh)
        self.cau_hinh = hop_nhat_cau_hinh(CAU_HINH_MAC_DINH, ch) if ch else CAU_HINH_MAC_DINH
        if ch is None:
            _ghi_json_an_toan(self.file_cau_hinh, self.cau_hinh)

        dl = _doc_json(self.file_du_lieu)
        if dl is None:
            dl = du_lieu_mau()
            _ghi_json_an_toan(self.file_du_lieu, dl)
        dl.setdefault("ky_muc_tieu", [])
        dl.setdefault("muc_tieu", [])
        dl.setdefault("phieu_danh_gia", {})
        dl.setdefault("nguoi_dung", {"ho_ten": "", "chuc_vu": "", "don_vi": ""})
        # bổ sung trường mới cho bản ghi cũ
        dl["muc_tieu"] = [muc_tieu_moi(**{**m}) for m in dl["muc_tieu"]]
        self.du_lieu = dl

    def luu(self):
        _ghi_json_an_toan(self.file_du_lieu, self.du_lieu)

    def xuat(self, duong_dan):
        _ghi_json_an_toan(Path(duong_dan), self.du_lieu)

    def nhap(self, duong_dan):
        dl = _doc_json(Path(duong_dan))
        if not isinstance(dl, dict) or "muc_tieu" not in dl:
            raise ValueError("File không đúng định dạng dữ liệu Nhím KPI.")
        _ghi_json_an_toan(self.file_du_lieu, dl)
        self.tai()

    # ---------- Kỳ mục tiêu ----------
    @property
    def ds_ky(self):
        return self.du_lieu["ky_muc_tieu"]

    @property
    def ds_muc_tieu(self):
        return self.du_lieu["muc_tieu"]

    def tim_ky(self, ky_id):
        return next((k for k in self.ds_ky if k["id"] == ky_id), None)

    def luu_ky(self, ky):
        cu = self.tim_ky(ky["id"])
        if cu:
            cu.update(ky)
        else:
            self.ds_ky.append(ky)
        self.luu()

    def xoa_ky(self, ky_id):
        """Xoá kỳ cùng các mục tiêu & phiếu thuộc kỳ."""
        self.du_lieu["ky_muc_tieu"] = [k for k in self.ds_ky if k["id"] != ky_id]
        self.du_lieu["muc_tieu"] = [m for m in self.ds_muc_tieu if m.get("ky_id") != ky_id]
        self.du_lieu["phieu_danh_gia"].pop(ky_id, None)
        self.luu()

    # ---------- Mục tiêu ----------
    def tim_muc_tieu(self, mt_id):
        return next((m for m in self.ds_muc_tieu if m["id"] == mt_id), None)

    def hau_due(self, mt_id):
        """Tập id các mục tiêu con, cháu... của một mục tiêu."""
        kq, hang_doi = set(), [mt_id]
        while hang_doi:
            cur = hang_doi.pop()
            for m in self.ds_muc_tieu:
                if m.get("parent_id") == cur and m["id"] not in kq:
                    kq.add(m["id"])
                    hang_doi.append(m["id"])
        return kq

    def luu_muc_tieu(self, mt, noi_dung_lich_su):
        mt.setdefault("lich_su", []).append({"thoi_gian": bay_gio(), "noi_dung": noi_dung_lich_su})
        cu = self.tim_muc_tieu(mt["id"])
        if cu:
            cu.update(mt)
        else:
            self.ds_muc_tieu.append(mt)
        self.luu()

    def xoa_muc_tieu(self, mt_id):
        bo = self.hau_due(mt_id) | {mt_id}
        self.du_lieu["muc_tieu"] = [m for m in self.ds_muc_tieu if m["id"] not in bo]
        self.luu()

    # ---------- Phiếu đánh giá ----------
    def lay_phieu(self, ky_id):
        return self.du_lieu["phieu_danh_gia"].get(ky_id) or phieu_moi(ky_id)

    def luu_phieu(self, phieu):
        phieu["ngay_cap_nhat"] = bay_gio()
        self.du_lieu["phieu_danh_gia"][phieu["ky_id"]] = phieu
        self.luu()
