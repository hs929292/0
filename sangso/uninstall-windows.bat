@echo off
schtasks /Delete /TN "ZhugeLiangSangso" /F
powershell -NoProfile -Command "Remove-Item -ErrorAction SilentlyContinue (Join-Path ([Environment]::GetFolderPath('Startup')) 'ZhugeLiangSangso.lnk'), (Join-Path ([Environment]::GetFolderPath('Desktop')) 'Zhuge Liang Sangso.lnk')"
echo Removed.
pause
