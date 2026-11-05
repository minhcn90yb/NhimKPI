# 🦔 Nhím KPI – Phần mềm quản lý KPI cá nhân

Phần mềm máy tính (Python + CustomTkinter) hiện thực hóa bộ **Hướng dẫn sử dụng hệ thống eKPI – Đánh giá cán bộ**:
kỳ mục tiêu, cây mục tiêu KPI/OKR, phiếu đánh giá 120 điểm và xếp loại 4 mức. Dữ liệu lưu cục bộ bằng JSON.

## 1. Cấu trúc thư mục

```
NhimKPI/
├── main.py                    # Điểm khởi chạy
├── nhim_kpi/
│   ├── cau_hinh.py            # Thang điểm, tiêu chí, ngưỡng xếp loại (mặc định)
│   ├── tinh_diem.py           # Công thức: tiến độ, KPI quy đổi, phiếu 120 điểm, xếp loại
│   ├── luu_tru.py             # Đọc/ghi JSON an toàn + bản sao lưu .bak
│   ├── nhim.py                # Vẽ chú nhím Chibi & biểu đồ tròn bằng Canvas
│   ├── giao_dien_chung.py     # Bảng màu pastel, phông chữ, widget dùng chung
│   ├── hop_thoai.py           # Hộp thoại Thêm/Sửa Kỳ mục tiêu & Mục tiêu
│   ├── trang_tong_quan.py     # Dashboard
│   ├── trang_muc_tieu.py      # Cây mục tiêu
│   ├── trang_phieu.py         # Phiếu đánh giá
│   ├── trang_khac.py          # Kỳ mục tiêu + Cài đặt
│   └── ung_dung.py            # Cửa sổ chính
├── assets/nhim.ico, nhim.png  # Icon chú nhím
├── tests/test_tinh_diem.py    # Kiểm thử công thức
├── build_windows.bat          # Đóng gói .exe
├── installer_windows.iss      # Tạo file cài đặt Setup.exe (Inno Setup)
└── build_mac.sh               # Đóng gói .app + .dmg
```

## 2. Cài đặt & chạy thử

Yêu cầu **Python 3.10 trở lên** (khuyến nghị 3.11/3.12 từ python.org – đã kèm sẵn Tkinter).

**Windows** (mở Command Prompt trong thư mục `NhimKPI`):
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**macOS** (Terminal):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Linux**: cài thêm Tkinter nếu thiếu (`sudo apt install python3-tk`), sau đó làm như macOS.

Kiểm thử công thức (không cần giao diện): `python -m unittest discover tests`

Lần chạy đầu, phần mềm tạo thư mục `NhimKPI` trong thư mục người dùng
(Windows: `C:\Users\<tên>\NhimKPI`, macOS: `/Users/<tên>/NhimKPI`) gồm:
- `du_lieu_kpi.json` – toàn bộ dữ liệu (kèm 1 kỳ mục tiêu minh họa, có thể xoá);
- `du_lieu_kpi.bak` – bản sao lưu tự động trước mỗi lần ghi;
- `cau_hinh.json` – thang điểm & ngưỡng xếp loại (sửa được bằng Notepad).

## 3. Đóng gói thành file cài đặt

### Windows → `NhimKPI.exe` và `NhimKPI_Setup.exe`
1. Nhấp đúp `build_windows.bat` → kết quả ở `dist\NhimKPI\NhimKPI.exe` (chép cả thư mục `dist\NhimKPI` sang máy khác là chạy được).
2. (Tuỳ chọn) Cài [Inno Setup 6](https://jrsoftware.org/isinfo.php), mở `installer_windows.iss` → **Build › Compile**
   → tạo `dist\NhimKPI_Setup.exe` có shortcut Start Menu/Desktop và gỡ cài đặt.

### macOS → `NhimKPI.dmg`
```bash
./build_mac.sh
```
Kết quả: `dist/NhimKPI.app` và `dist/NhimKPI.dmg`. Ứng dụng chưa ký số nên lần mở đầu cần
**chuột phải › Open** (hoặc System Settings › Privacy & Security › Open Anyway).

> PyInstaller không biên dịch chéo: muốn có `.exe` phải build trên Windows, muốn có `.dmg` phải build trên Mac.

## 4. Điều chỉnh quy định chấm điểm
Mở `cau_hinh.json` (Cài đặt › ⚙️ Mở file cấu hình), sửa rồi khởi động lại phần mềm:
- `nhom_I.muc[].tieu_chi[]`: tên & điểm tối đa từng tiêu chí chung. Các dòng có ký hiệu `[...]` là phần
  tài liệu không hiển thị rõ, cần bổ sung theo mẫu phiếu của đơn vị (tổng Nhóm I nên giữ = 30).
- `nhom_II.he_so_quy_doi` (70), `nhom_III.diem_toi_da` (20), `nhom_III.ty_le_toi_da_so_voi_nhom_II` (0.3).
- `xep_loai[].diem_tu`: ngưỡng dưới của từng mức xếp loại (thang 120).
- `tran_ty_le_hoan_thanh`: 1.0 = mỗi chỉ tiêu tính tối đa 100%; đặt 1.2 nếu cho phép vượt 120%.
