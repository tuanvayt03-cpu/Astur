; Astur VI in-place update. SAME AppId as upstream to upgrade existing Astur,
; not create a second product. Backs up current binaries and user config first.
; Version 2.4.0.9 is a pre-release, not the official upstream Astur release.
#define AppName "Astur"
#define AppVersion "2.4.0.9"
#define AppExe "Astur.exe"

[Setup]
; Keep this GUID IDENTICAL to packaging/astur.iss. It is the update key.
AppId={{7C7F9E2A-4A1E-4B3D-9E2C-0A1B2C3D4E5F}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName=Astur VI Update {#AppVersion} (Preview)
AppPublisher=Astur VI Community Fork
AppPublisherURL=https://github.com/tuanvayt03-cpu/Astur
AppSupportURL=https://github.com/tuanvayt03-cpu/Astur
DefaultDirName={autopf}\Astur
UsePreviousAppDir=yes
UsePreviousTasks=yes
DefaultGroupName=Astur
DisableProgramGroupPage=yes
UninstallDisplayName=Astur
UninstallDisplayIcon={app}\{#AppExe}
LicenseFile=..\LICENSE
InfoBeforeFile=upgrade-install-notice.txt
SetupIconFile=..\crates\astur\assets\astur.ico
OutputDir=..\dist\upgrade
OutputBaseFilename=Astur-VI-Update-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
CloseApplications=yes
RestartApplications=no

[Tasks]
Name: "startup"; Description: "Start Astur automatically when I sign in"; GroupDescription: "Startup:"

[Files]
Source: "..\target\release\astur.exe"; DestDir: "{app}"; DestName: "{#AppExe}"; Flags: ignoreversion
Source: "..\target\release\astur-settings.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\THIRD_PARTY_NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "upgrade-install-notice.txt"; DestDir: "{app}"; DestName: "ASTUR_VI_UPDATE_README.txt"; Flags: ignoreversion

[Icons]
Name: "{group}\Astur"; Filename: "{app}\{#AppExe}"
Name: "{group}\Uninstall Astur"; Filename: "{uninstallexe}"
Name: "{userstartup}\Astur"; Filename: "{app}\{#AppExe}"; Tasks: startup

[Run]
Filename: "{app}\{#AppExe}"; Description: "Launch Astur after update"; Flags: nowait postinstall skipifsilent

[Code]
// Never overwrite the only copy of a user's existing executable/config.
// On reinstall, preserve the FIRST original backup rather than replacing it.
function BackupExisting(const Src, BackupDir, Name: String): Boolean;
var Dest: String;
begin
  Result := True;
  if not FileExists(Src) then Exit;
  Dest := AddBackslash(BackupDir) + Name;
  if FileExists(Dest) then Exit;
  if not ForceDirectories(BackupDir) then begin
    Result := False;
    Exit;
  end;
  Result := FileCopy(Src, Dest, False);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var BackupDir, UserDir, InstallDir: String;
begin
  Result := '';
  BackupDir := ExpandConstant('{localappdata}\Astur\UpgradeBackup\before-vi-update-2.4.0.1');
  InstallDir := ExpandConstant('{app}');
  UserDir := ExpandConstant('{%USERPROFILE}\.astur');
  if not BackupExisting(AddBackslash(InstallDir) + 'Astur.exe', BackupDir, 'Astur.exe') or
     not BackupExisting(AddBackslash(InstallDir) + 'astur-settings.exe', BackupDir, 'astur-settings.exe') or
     not BackupExisting(AddBackslash(UserDir) + 'astur.conf', BackupDir, 'astur.conf') or
     not BackupExisting(AddBackslash(UserDir) + 'navbar.conf', BackupDir, 'navbar.conf') then
  begin
    Result := 'Cannot back up the existing Astur installation. Update cancelled without overwriting it.';
  end;
end;
