# Aurora Pay - gorev dogrulayici (Windows / PowerShell). verify/run.sh karsiligi.
# Kullanim: .\verify\run.ps1 [m0..m8|all]
Push-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$env:PYTHONUTF8 = '1'
$py = '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
& $py verify\run.py @args
$code = $LASTEXITCODE
Pop-Location
exit $code
