[Setup]
AppName=Singlish
AppVersion=2.05
DefaultDirName={commonpf}\SinglishQt
DefaultGroupName=Singlish
OutputDir=Output
OutputBaseFilename="SinglishSetup 2.05"
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\iconmr.ico
UninstallDisplayName=Singlish
SetupIconFile=dist\SinglishQt 2.05\iconmr.ico

[Files]
// Ensure the paths below are correct and accessible
Source: "dist\SinglishQt 2.05\SinglishQt 2.05.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\SinglishQt 2.05\iconmr.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\SinglishQt 2.05\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs
// Ensure this folder exists and contains files. If not, remove this line.

[Icons]
Name: "{group}\Singlish"; Filename: "{app}\SinglishQt 2.05.exe"; IconFilename: "{app}\iconmr.ico"
Name: "{commondesktop}\Singlish"; Filename: "{app}\SinglishQt 2.05.exe"; IconFilename: "{app}\iconmr.ico"

[Run]
Filename: "{app}\SinglishQt 2.05.exe"; Description: "Launch Singlish"; Flags: postinstall nowait

[UninstallDelete]
Type: filesandordirs; Name: "{app}\_internal"
Type: files; Name: "{app}\SinglishQt 2.05.exe"
Type: files; Name: "{app}\iconmr.ico"

[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"
Type: files; Name: "{app}\SinglishQt 2.05.exe"
Type: files; Name: "{app}\iconmr.ico"

