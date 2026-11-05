[Setup]
AppName=Nhim KPI
AppVersion=1.0.0
AppPublisher=Nhim KPI
DefaultDirName={autopf}\NhimKPI
DefaultGroupName=Nhim KPI
OutputDir=dist
OutputBaseFilename=NhimKPI_Setup
SetupIconFile=assets\nhim.ico
UninstallDisplayIcon={app}\NhimKPI.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Tasks]
Name: "desktopicon"; Description: "Tao bieu tuong ngoai Desktop"; GroupDescription: "Tuy chon:"

[Files]
Source: "dist\NhimKPI\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Nhim KPI"; Filename: "{app}\NhimKPI.exe"
Name: "{autodesktop}\Nhim KPI"; Filename: "{app}\NhimKPI.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NhimKPI.exe"; Description: "Mo Nhim KPI ngay"; Flags: nowait postinstall skipifsilent
