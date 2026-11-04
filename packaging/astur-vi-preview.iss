; Astur VI Preview - isolated installer identity; does not replace upstream Astur.
; Built only on Windows after a fresh cargo --release build.
; This is a testing preview, not the production Astur or a fully verified localization.
#define AppName "Astur VI Preview"
#define AppVersion "2.4.0"
#define PreviewLabel "2.4.0-preview.1"
#define AppExe "Astur.exe"

[Setup]
; Distinct from upstream GUID {7C7F9E2A-4A1E-4B3D-9E2C-0A1B2C3D4E5F}.
AppId={{C5C68023-EC09-4794-A0E6-4B74885BC910}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#PreviewLabel}
AppPublisher=Astur VI Community Fork
AppPublisherURL=https://github.com/tuanvayt03-cpu/Astur
AppSupportURL=https://github.com/tuanvayt03-cpu/Astur/issues
DefaultDirName={localappdata}\Programs\Astur VI Preview
DefaultGroupName=Astur VI Preview
DisableProgramGroupPage=yes
UsePreviousAppDir=no
UsePreviousTasks=no
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExe}
LicenseFile=..\LICENSE
InfoBeforeFile=preview-install-notice.txt
SetupIconFile=..\crates\astur\assets\astur.ico
OutputDir=..\dist\preview
OutputBaseFilename=Astur-VI-Preview-Setup-{#PreviewLabel}
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
; Never forcibly close upstream Astur, running windows, or foreign applications.
CloseApplications=no
RestartApplications=no
; No autostart task; no automatically starting experimental hooks after install.

[Files]
Source: "..\target\release\astur.exe"; DestDir: "{app}"; DestName: "{#AppExe}"; Flags: ignoreversion
Source: "..\target\release\astur-settings.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\THIRD_PARTY_NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "preview-install-notice.txt"; DestDir: "{app}"; Flags: ignoreversion; DestName: "READ_ME_FIRST.txt"

[Icons]
Name: "{group}\Astur VI Preview"; Filename: "{app}\{#AppExe}"
Name: "{group}\Settings (Astur VI Preview)"; Filename: "{app}\astur-settings.exe"
Name: "{group}\Uninstall Astur VI Preview"; Filename: "{uninstallexe}"
