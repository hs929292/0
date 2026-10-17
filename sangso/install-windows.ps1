# Registers the memorial to open every day at 7:00 AM and whenever you sign in.
# No administrator rights needed. Undo with uninstall-windows.bat.
$ErrorActionPreference = "Stop"

$dir    = Split-Path -Parent $MyInvocation.MyCommand.Path
$opener = Join-Path $dir "open-sangso.ps1"
$psArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$opener`""
$taskName = "ZhugeLiangSangso"

# 1) Every day at 7:00 AM. If the PC was off at 7, it runs as soon as possible after.
$action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $psArgs
$trigger  = New-ScheduledTaskTrigger -Daily -At "07:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

# 2) At sign-in: a shortcut in the Startup folder.
$startup = [Environment]::GetFolderPath("Startup")
$shell   = New-Object -ComObject WScript.Shell
$lnk     = $shell.CreateShortcut((Join-Path $startup "ZhugeLiangSangso.lnk"))
$lnk.TargetPath       = "powershell.exe"
$lnk.Arguments        = $psArgs
$lnk.WorkingDirectory = $dir
$lnk.WindowStyle      = 7
$lnk.Save()

# 3) A desktop shortcut to reopen it any time.
$desk = [Environment]::GetFolderPath("Desktop")
$lnk2 = $shell.CreateShortcut((Join-Path $desk "Zhuge Liang Sangso.lnk"))
$lnk2.TargetPath       = "powershell.exe"
$lnk2.Arguments        = "$psArgs -Force"
$lnk2.WorkingDirectory = $dir
$lnk2.WindowStyle      = 7
$lnk2.Save()

Write-Host "Installed: daily 7:00 AM + at sign-in + desktop shortcut."
& $opener -Force
