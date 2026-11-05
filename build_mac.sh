#!/bin/bash
# ===== Đóng gói Nhím KPI thành NhimKPI.app và NhimKPI.dmg (macOS) =====
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-build.txt

# Tạo icon .icns từ assets/nhim.png
mkdir -p build/nhim.iconset
for s in 16 32 64 128 256 512; do
  sips -z $s $s assets/nhim.png --out build/nhim.iconset/icon_${s}x${s}.png >/dev/null
  d=$((s*2)); sips -z $d $d assets/nhim.png --out build/nhim.iconset/icon_${s}x${s}@2x.png >/dev/null
done
iconutil -c icns build/nhim.iconset -o build/nhim.icns

pyinstaller --noconfirm --clean --windowed \
  --name NhimKPI \
  --icon build/nhim.icns \
  --add-data "assets:assets" \
  --collect-data customtkinter \
  main.py

# Đóng gói .dmg (kéo thả vào Applications)
rm -rf build/dmg && mkdir -p build/dmg
cp -R dist/NhimKPI.app build/dmg/
ln -s /Applications build/dmg/Applications
hdiutil create -volname "Nhim KPI" -srcfolder build/dmg -ov -format UDZO dist/NhimKPI.dmg
echo "Xong! File cài đặt: dist/NhimKPI.dmg"
