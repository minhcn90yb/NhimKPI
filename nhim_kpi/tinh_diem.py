# -*- coding: utf-8 -*-
"""
BỘ MÁY TÍNH ĐIỂM – hiện thực hóa công thức trong tài liệu eKPI
---------------------------------------------------------------
1) Tiến độ mục tiêu:
   - KPI theo chỉ tiêu: Σ(min(Đạt/Mục tiêu, trần) × tỷ trọng) / Σ tỷ trọng
   - OKR: tính tương tự trên các Kết quả then chốt (KR)
   - Tự động tổng hợp từ mục tiêu con: bình quân gia quyền theo Trọng số (%) của con
   - Tổng hợp từ dự án/danh sách công việc: số việc hoàn thành / tổng số việc
2) Điểm KPI quy đổi của kỳ = bình quân gia quyền tiến độ các mục tiêu gốc.
3) Phiếu đánh giá 120 điểm = Nhóm I + Nhóm II (KPI quy đổi × 70) + Nhóm III (điểm cộng).
4) Xếp loại theo 4 nhóm dựa trên điểm chốt (ưu tiên: Cấp thẩm quyền > Cấp trên > Tự chấm).
"""
from datetime import date

from .cau_hinh import (PT_CHI_TIEU, PT_TONG_HOP_CON, PT_CONG_VIEC,
                       TT_HOAN_THANH, TT_DANG_THUC_HIEN, TT_QUA_HAN, TT_CHUA_BAT_DAU,
                       cac_tieu_chi_nhom_I)

COT_DIEM = ("tu_cham", "cap_tren", "tham_quyen")
TEN_COT = {"tu_cham": "Điểm do cá nhân tự chấm",
           "cap_tren": "Điểm cấp trên trực tiếp chấm",
           "tham_quyen": "Điểm do cấp có thẩm quyền xác nhận"}


# ===================== Tiện ích số & ngày =====================
def so(gia_tri, mac_dinh=0.0):
    """Chuyển về số thực an toàn (chấp nhận dấu phẩy thập phân)."""
    if gia_tri is None or gia_tri == "":
        return mac_dinh
    try:
        return float(str(gia_tri).replace(",", ".").strip())
    except (TypeError, ValueError):
        return mac_dinh


def doc_ngay(chuoi):
    """Đọc ngày ISO 'YYYY-MM-DD' -> date (hoặc None)."""
    if not chuoi:
        return None
    try:
        return date.fromisoformat(chuoi)
    except (TypeError, ValueError):
        return None


def ty_le(dat, muc_tieu, tran=1.0):
    """Tỷ lệ hoàn thành của một chỉ tiêu, giới hạn trong [0, trần]."""
    mt = so(muc_tieu)
    if mt <= 0:
        return 0.0
    return max(0.0, min(so(dat) / mt, tran))


def binh_quan_gia_quyen(cap_gia_tri_trong_so):
    """Bình quân gia quyền; nếu tổng trọng số = 0 thì lấy bình quân cộng."""
    ds = list(cap_gia_tri_trong_so)
    if not ds:
        return 0.0
    tong_ts = sum(max(0.0, ts) for _, ts in ds)
    if tong_ts <= 0:
        return sum(v for v, _ in ds) / len(ds)
    return sum(v * max(0.0, ts) for v, ts in ds) / tong_ts


# ===================== Tiến độ mục tiêu =====================
def muc_tieu_con(muc_tieu, ds_muc_tieu):
    return [m for m in ds_muc_tieu if m.get("parent_id") == muc_tieu["id"]]


def tien_do(muc_tieu, ds_muc_tieu, cau_hinh, _dang_xet=None):
    """Tiến độ hoàn thành (0..trần) của một mục tiêu theo phương thức đánh giá."""
    tran = so(cau_hinh.get("tran_ty_le_hoan_thanh", 1.0), 1.0)
    _dang_xet = set() if _dang_xet is None else _dang_xet
    if muc_tieu["id"] in _dang_xet:          # chống vòng lặp cha-con lỗi
        return 0.0
    _dang_xet = _dang_xet | {muc_tieu["id"]}

    pt = muc_tieu.get("phuong_thuc", PT_CHI_TIEU)

    if pt == PT_TONG_HOP_CON:
        con = muc_tieu_con(muc_tieu, ds_muc_tieu)
        return binh_quan_gia_quyen(
            (tien_do(c, ds_muc_tieu, cau_hinh, _dang_xet), so(c.get("trong_so"))) for c in con)

    if pt == PT_CONG_VIEC:
        cv = muc_tieu.get("cong_viec", [])
        if not cv:
            return 0.0
        return sum(1 for c in cv if c.get("hoan_thanh")) / len(cv)

    # PT_CHI_TIEU: KPI dùng "chi_tieu", OKR dùng "ket_qua_then_chot"
    dong = muc_tieu.get("chi_tieu" if muc_tieu.get("loai") == "KPI" else "ket_qua_then_chot", [])
    return binh_quan_gia_quyen(
        (ty_le(d.get("gia_tri_dat"), d.get("gia_tri_muc_tieu"), tran), so(d.get("ty_trong")))
        for d in dong)


def trang_thai(muc_tieu, tien_do_mt, hom_nay=None):
    """Trạng thái hiển thị: Hoàn thành / Quá hạn / Chưa bắt đầu / Đang thực hiện."""
    hom_nay = hom_nay or date.today()
    if tien_do_mt >= 0.9999:
        return TT_HOAN_THANH
    ket_thuc = doc_ngay(muc_tieu.get("ngay_ket_thuc"))
    bat_dau = doc_ngay(muc_tieu.get("ngay_bat_dau"))
    if ket_thuc and hom_nay > ket_thuc:
        return TT_QUA_HAN
    if bat_dau and hom_nay < bat_dau:
        return TT_CHUA_BAT_DAU
    return TT_DANG_THUC_HIEN


def muc_tieu_trong_ky(ky_id, ds_muc_tieu):
    return [m for m in ds_muc_tieu if ky_id is None or m.get("ky_id") == ky_id]


def diem_kpi_quy_doi(ky_id, ds_muc_tieu, cau_hinh):
    """Điểm KPI quy đổi (0..1) = bình quân gia quyền tiến độ các mục tiêu GỐC trong kỳ."""
    ds = muc_tieu_trong_ky(ky_id, ds_muc_tieu)
    ids = {m["id"] for m in ds}
    goc = [m for m in ds if not m.get("parent_id") or m.get("parent_id") not in ids]
    gia_tri = binh_quan_gia_quyen((tien_do(m, ds_muc_tieu, cau_hinh), so(m.get("trong_so"))) for m in goc)
    return min(gia_tri, 1.0)


def kiem_tra_trong_so(ds_muc_tieu, ky_id):
    """Cảnh báo các nhóm mục tiêu cùng cha có tổng trọng số khác 100%."""
    nhom = {}
    for m in muc_tieu_trong_ky(ky_id, ds_muc_tieu):
        nhom.setdefault(m.get("parent_id"), []).append(m)
    canh_bao = []
    ten_theo_id = {m["id"]: m.get("ten", "") for m in ds_muc_tieu}
    for cha, con in nhom.items():
        tong = sum(so(c.get("trong_so")) for c in con)
        if abs(tong - 100) > 0.01:
            noi = "các mục tiêu gốc" if cha is None else f"con của «{ten_theo_id.get(cha, '?')}»"
            canh_bao.append(f"Tổng trọng số {noi} = {tong:g}% (cần 100%)")
    return canh_bao


def thong_ke(ky_id, ds_muc_tieu, cau_hinh, hom_nay=None):
    """Số liệu cho 4 thẻ chỉ số & biểu đồ tròn trên Dashboard."""
    ds = muc_tieu_trong_ky(ky_id, ds_muc_tieu)
    dem = {TT_HOAN_THANH: 0, TT_DANG_THUC_HIEN: 0, TT_QUA_HAN: 0, TT_CHUA_BAT_DAU: 0}
    for m in ds:
        dem[trang_thai(m, tien_do(m, ds_muc_tieu, cau_hinh), hom_nay)] += 1
    return {"tong": len(ds), "theo_trang_thai": dem,
            "kpi": sum(1 for m in ds if m.get("loai") == "KPI"),
            "okr": sum(1 for m in ds if m.get("loai") == "OKR")}


# ===================== Phiếu đánh giá 120 điểm =====================
def diem_he_thong(cau_hinh, quy_doi):
    """Cột 'Hệ thống đánh giá': Nhóm I = điểm tối đa, Nhóm II = quy đổi × 70, Nhóm III = 0."""
    kq = {tc["ma"]: so(tc["diem_toi_da"]) for tc in cac_tieu_chi_nhom_I(cau_hinh)}
    nII = cau_hinh["nhom_II"]
    kq["II"] = round(min(quy_doi * so(nII["he_so_quy_doi"]), so(nII["diem_toi_da"])), 2)
    kq["III"] = 0.0
    return kq


def cot_co_du_lieu(phieu, cot):
    return any(v.get(cot) not in (None, "") for v in phieu.get("diem", {}).values())


def _gia_tri_o(phieu, ma, cot, he_thong):
    """Giá trị một ô điểm. Ô trống được KẾ THỪA từ cột liền trước:
    Tự chấm ← Hệ thống đánh giá; Cấp trên ← Tự chấm; Thẩm quyền ← Cấp trên."""
    v = phieu.get("diem", {}).get(ma, {}).get(cot)
    if v not in (None, ""):
        return so(v)
    if cot == "tu_cham":
        return so(he_thong.get(ma, 0.0))
    return _gia_tri_o(phieu, ma, COT_DIEM[COT_DIEM.index(cot) - 1], he_thong)


def tong_cot(phieu, cot, cau_hinh, he_thong):
    """Tính điểm từng nhóm & tổng của một cột chấm điểm (có kế thừa ô trống)."""
    def lay(ma, toi_da):
        return max(0.0, min(_gia_tri_o(phieu, ma, cot, he_thong), toi_da))

    nhom_I = sum(lay(tc["ma"], so(tc["diem_toi_da"])) for tc in cac_tieu_chi_nhom_I(cau_hinh))
    nhom_II = lay("II", so(cau_hinh["nhom_II"]["diem_toi_da"]))
    nIII = cau_hinh["nhom_III"]
    # Điểm cộng không quá 30% điểm kết quả thực hiện chức trách, nhiệm vụ (Nhóm II)
    tran_III = min(so(nIII["diem_toi_da"]), so(nIII["ty_le_toi_da_so_voi_nhom_II"]) * nhom_II)
    nhom_III = min(lay("III", so(nIII["diem_toi_da"])), tran_III)
    return {"I": round(nhom_I, 2), "II": round(nhom_II, 2), "III": round(nhom_III, 2),
            "tran_III": round(tran_III, 2), "tong": round(nhom_I + nhom_II + nhom_III, 2)}


def xep_loai(diem, cau_hinh):
    """Trả về bản ghi xếp loại (dict) tương ứng với điểm."""
    thang = sorted(cau_hinh["xep_loai"], key=lambda x: so(x["diem_tu"]), reverse=True)
    for muc in thang:
        if diem >= so(muc["diem_tu"]):
            return muc
    return thang[-1]


def ket_qua_phieu(phieu, ky_id, ds_muc_tieu, cau_hinh):
    """Tổng hợp đầy đủ một phiếu: điểm hệ thống, 3 cột, điểm chốt và xếp loại."""
    quy_doi = diem_kpi_quy_doi(ky_id, ds_muc_tieu, cau_hinh)
    he_thong = diem_he_thong(cau_hinh, quy_doi)
    cot = {c: tong_cot(phieu, c, cau_hinh, he_thong) for c in COT_DIEM}
    nguon_chot = "tu_cham"
    for c in ("tham_quyen", "cap_tren"):
        if cot_co_du_lieu(phieu, c):
            nguon_chot = c
            break
    diem_chot = cot[nguon_chot]["tong"]
    return {"quy_doi": quy_doi, "he_thong": he_thong, "cot": cot,
            "nguon_chot": nguon_chot, "diem_chot": diem_chot,
            "xep_loai": xep_loai(diem_chot, cau_hinh)}
