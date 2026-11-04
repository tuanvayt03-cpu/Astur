#!/usr/bin/env python3
"""Read-only safety contract for the isolated Astur VI Preview installer."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
stable = (root / "packaging/astur.iss").read_text(encoding="utf-8")
preview = (root / "packaging/astur-vi-preview.iss").read_text(encoding="utf-8")
notice = (root / "packaging/preview-install-notice.txt").read_text(encoding="utf-8")
workflow = (root / ".github/workflows/preview-release.yml").read_text(encoding="utf-8")

def app_id(source):
    match = re.search(r"(?m)^AppId=(.+)$", source)
    assert match, "Missing AppId"
    return match.group(1).strip().lower()

assert app_id(stable) != app_id(preview), "Preview would overwrite upstream install registry"
assert re.search(r"(?m)^DefaultDirName=\{localappdata\}\\Programs\\Astur VI Preview$", preview)
assert re.search(r"(?m)^DefaultGroupName=Astur VI Preview$", preview)
assert re.search(r"(?m)^PrivilegesRequired=lowest$", preview)
assert re.search(r"(?m)^CloseApplications=no$", preview)
assert re.search(r"(?m)^RestartApplications=no$", preview)
assert "[Run]" not in preview, "Installer must never start an experimental WM automatically"
assert "[Tasks]" not in preview and "{userstartup}" not in preview
assert "target\\release\\astur.exe" in preview
assert "target\\release\\astur-settings.exe" in preview
assert "LICENSE" in preview and "THIRD_PARTY_NOTICES.md" in preview
assert "InfoBeforeFile=preview-install-notice.txt" in preview
assert "%USERPROFILE%\\.astur" in notice, "Must warn about shared configuration"
assert "Do NOT run original Astur and Astur VI Preview simultaneously." in notice
assert "workflow_dispatch:" in workflow
assert "if: github.ref == 'refs/heads/feat/vi-notifications'" in workflow
assert "Smoke test installer in isolated runner directory" in workflow
assert "Verify portable ZIP content" in workflow
assert "SHA256SUMS.txt" in workflow
assert "gh release create" in workflow and "--prerelease" in workflow
assert "PREVIEW_TAG: astur-vi-preview-" in workflow, "Prevent release.yml v* collisions"
print("Preview installer isolation / legal / safety / build / smoke / checksums: PASS")
