# Astur VI Preview 2.4.0-preview.1

**Experimental Windows x64 build. Not the original Astur.**

Includes a Vietnamese/English Settings language selector (367 translation mappings) and a conservative native-popup classification change intended to let notifications **appear normally without joining tiled windows or tab groups**. The notification fix is not yet validated against live Zalo/Telegram/Windows popup windows; not all text is localized.

### Files
- `Astur-VI-Preview-Setup-2.4.0-preview.1.exe`: per-user Windows installer, distinct app identity and install folder.
- `Astur-VI-Preview-Portable-2.4.0-preview.1.zip`: both Windows executables, notice and legal files.
- `SHA256SUMS.txt`: checksums for both downloads.

**Safety:** The installer does not run Astur on completion, modify startup, or close existing apps. **Never run original Astur and Preview at the same time.** They currently **share** the `%USERPROFILE%\.astur` configuration and rescue data. Back up that folder and quit the original before launching Preview. Installing Preview only does not launch its hooks.

No code signing; Windows SmartScreen may warn. Verify the checksum and publisher source before running. Do not use as a stable/production replacement.

CI tests include Rust fmt, Clippy, workspace unit tests and Windows release build, plus a sandboxed installer install/uninstall smoke. **Real desktop GUI and native popup E2E remain unverified.**

Repository: https://github.com/tuanvayt03-cpu/Astur
