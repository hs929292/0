# Opens today's memorial once per day (7 AM task or at logon, whichever comes first).
# Run with -Force to open it again regardless.
param([switch]$Force)

$dir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$stamp = Join-Path $dir ".last-shown"
$today = Get-Date -Format "yyyy-MM-dd"

if (-not $Force -and (Test-Path $stamp)) {
    if ((Get-Content $stamp -Raw).Trim() -eq $today) { exit 0 }
}
Set-Content -Path $stamp -Value $today

$page = Join-Path $dir "index.html"
$url  = ([System.Uri]$page).AbsoluteUri

# Edge app mode gives a clean popup window without tabs or address bar.
$edge = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

if ($edge) {
    Start-Process -FilePath $edge -ArgumentList "--app=$url", "--window-size=900,1000"
} else {
    Start-Process -FilePath $page
}
