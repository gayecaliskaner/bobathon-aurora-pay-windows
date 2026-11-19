# Semgrep ile guvenlik taramasi (Mission 5), Windows / PowerShell. scan.sh karsiligi.
# Cikis kodu: 0 = temiz, 1 = bulgu var, 2 = semgrep calistirilamadi.
# Kullanim:  .\scripts\scan.ps1            (ozet)
#            .\scripts\scan.ps1 --verbose  (her bulgu)
Push-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$env:PYTHONUTF8 = '1'
$py = '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
& $py scripts\scan.py @args
$code = $LASTEXITCODE
Pop-Location
exit $code
