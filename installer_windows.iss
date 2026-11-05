\xef\xbb\xbf; ===== Script Inno Setup: tạo file cài đặt NhimKPI_Setup.exe =====
; Yêu cầu: đã chạy build_windows.bat và cài Inno Setup 6 (https://jrsoftware.org/isinfo.php)
[Setup]
AppName=Nhím KPI
AppVersion=1.0.0
AppPublisher=Nhím KPI
DefaultDirName={autopf}\NhimKPI
DefaultGroupName=Nhím KPI
OutputDir=dist
OutputBaseFilename=NhimKPI_Setup
SetupIconFile=assets\nhim.ico
UninstallDisplayIcon={app}\NhimKPI.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Files]
Source: "dist\NhimKPI\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Nhím KPI"; Filename: "{app}\NhimKPI.exe"
Name: "{autodesktop}\Nhím KPI"; Filename: "{app}\NhimKPI.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Tạo biểu tượng ngoài Desktop"; GroupDescription: "Tuỳ chọn:"

[Run]
Filename: "{app}\NhimKPI.exe"; Description: "Mở Nhím KPI ngay"; Flags: nowait postinstall skipifsilent
