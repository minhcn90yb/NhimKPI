# -*- coding: utf-8 -*-
"""Kiểm thử công thức tính điểm (không cần giao diện): python -m unittest discover tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["NHIM_KPI_HOME"] = tempfile.mkdtemp()

from nhim_kpi import tinh_diem as td                      # noqa: E402
from nhim_kpi.cau_hinh import CAU_HINH_MAC_DINH as CH     # noqa: E402
from nhim_kpi.luu_tru import KhoDuLieu                     # noqa: E402


class KiemThu(unittest.TestCase):
    def setUp(self):
        self.kho = KhoDuLieu()
        self.ky = self.kho.ds_ky[0]["id"]

    def test_tien_do_va_quy_doi(self):
        # Dữ liệu mẫu: 60% (w40) + 75% (w30) + 2/3 (w30) -> 66,5%
        self.assertAlmostEqual(td.diem_kpi_quy_doi(self.ky, self.kho.ds_muc_tieu, CH), 0.665, places=3)

    def test_xep_loai_theo_vi_du_tai_lieu(self):
        for diem, ten in ((110, "Hoàn thành xuất sắc nhiệm vụ"), (90, "Hoàn thành xuất sắc nhiệm vụ"),
                          (76.67, "Hoàn thành tốt nhiệm vụ"), (65.33, "Hoàn thành nhiệm vụ"),
                          (20, "Không hoàn thành nhiệm vụ")):
            self.assertEqual(td.xep_loai(diem, CH)["ten"], ten)

    def test_diem_cong_khong_qua_30_phan_tram(self):
        phieu = {"diem": {"II": {"tu_cham": 40}, "III": {"tu_cham": 20}}}
        kq = td.ket_qua_phieu(phieu, self.ky, self.kho.ds_muc_tieu, CH)
        self.assertEqual(kq["cot"]["tu_cham"]["III"], 12.0)          # 30% × 40
        self.assertEqual(kq["cot"]["tu_cham"]["tong"], 30 + 40 + 12)

    def test_ke_thua_va_diem_chot(self):
        phieu = {"diem": {"II": {"tham_quyen": 60}}}
        kq = td.ket_qua_phieu(phieu, self.ky, self.kho.ds_muc_tieu, CH)
        self.assertEqual(kq["nguon_chot"], "tham_quyen")
        self.assertEqual(kq["diem_chot"], 30 + 60 + 0)


if __name__ == "__main__":
    unittest.main()
