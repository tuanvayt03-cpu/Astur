#!/usr/bin/env python3
"""Static non-destructive Astur VI in-place upgrade contract."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
stable=(root/"packaging/astur.iss").read_text(encoding="utf-8")
update=(root/"packaging/astur-vi-update.iss").read_text(encoding="utf-8")
preview=(root/"packaging/astur-vi-preview.iss").read_text(encoding="utf-8")
workflow=(root/".github/workflows/upgrade-release.yml").read_text(encoding="utf-8")
def line(s,key):
    m=re.search(r"(?m)^"+re.escape(key)+r"=(.+)$",s)
    assert m,(key,"missing")
    return m.group(1).strip()
assert line(stable,"AppId")==line(update,"AppId"),"Must upgrade exact upstream installed app"
assert line(update,"AppId")!=line(preview,"AppId")
assert line(stable,"DefaultDirName")==line(update,"DefaultDirName")
assert line(stable,"DefaultGroupName")==line(update,"DefaultGroupName")
assert line(update,"AppName")=="{#AppName}"
assert line(update,"UsePreviousAppDir")=="yes"
assert line(update,"UsePreviousTasks")=="yes"
assert line(update,"CloseApplications")=="yes"
assert line(update,"RestartApplications")=="no"
assert line(update,"PrivilegesRequired")=="lowest"
assert "[Tasks]" in update and "Name: \"startup\"" in update
assert "[Run]" in update and "postinstall skipifsilent" in update
assert "PrepareToInstall(var NeedsRestart: Boolean)" in update
assert "FileCopy(Src, Dest, False)" in update
assert "if FileExists(Dest) then Exit;" in update
assert "Cannot back up the existing Astur installation" in update
assert "UpgradeBackup" in update and "astur.conf" in update and "navbar.conf" in update
assert "{userprofile}" not in update, "Inno Setup does not support this shell constant"
assert "{%USERPROFILE}" in update, "Must use the official environment-variable constant"
assert "THIRD_PARTY_NOTICES.md" in update and "LICENSE" in update
assert "astur-settings.exe" in update
assert "Smoke-test upgrade over upstream AppId" in workflow
assert "--prerelease" in workflow and "SHA256SUMS.txt" in workflow
assert "gh release create" in workflow
assert "on:" in workflow and "workflow_dispatch:" in workflow
version_match=re.search(r'(?m)^#define AppVersion "([^"]+)"$', update)
assert version_match, "Installer version must be defined"
version=version_match.group(1)
workflow_version=re.search(r"(?m)^  UPGRADE_VERSION: (.+)$",workflow)
workflow_tag=re.search(r"(?m)^  UPGRADE_TAG: (.+)$",workflow)
assert workflow_version and workflow_version.group(1)==version, "Workflow/installer version mismatch"
assert workflow_tag and workflow_tag.group(1)==f"astur-vi-update-{version}", "Release tag/version mismatch"
assert "before-vi-update-2.4.0.1" in update and "before-vi-update-2.4.0.1" in workflow, "Keep the first original backup across upgrades"
print("Astur VI in-place upgrade identity, version, backup, rollback, smoke contract: PASS")
