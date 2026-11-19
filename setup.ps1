# Aurora Pay - one-time workshop setup (Windows / PowerShell). setup.sh karsiligi.
# Usage: .\setup.ps1                  python deps only
#        .\setup.ps1 -Scanners        also installs semgrep (Mission 5) in an isolated venv
#        .\setup.ps1 -Scanners -Python C:\Python312\python.exe     (veya $env:PYTHON ile)
# Not: Bu dosyayi ASCII tutun; Windows PowerShell 5.1 BOM'suz dosyayi ANSI okur.
# Not: semgrep'in bagimliliklari (ruamel.yaml.clib) Windows'ta cok yeni Python'lar (3.14+) icin hazir paket
#      sunmayabilir. -Scanners, .venv-tools icin otomatik olarak Python 3.13/3.12/3.11 arar (py launcher).
[CmdletBinding()]
param(
    [switch]$Scanners,
    [string]$Python = $env:PYTHON
)

# Windows PowerShell 5.1: native komutun stderr'i 'Stop' ile hata sayilir; $LASTEXITCODE'u kendimiz kontrol ediyoruz.
$ErrorActionPreference = 'Continue'
$env:PYTHONUTF8 = '1'

function Test-PythonCandidate([string]$Exe, [string[]]$Extra) {
    try {
        & $Exe @Extra -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Stop-Setup([string]$Message) {
    Write-Host $Message
    Pop-Location
    exit 1
}

# semgrep icin uygun (3.11 - 3.13) bir Python bulur; yoksa ana Python'a duser.
function Find-ToolsPython([string]$MainExe, [string[]]$MainExtra) {
    foreach ($v in '3.13', '3.12', '3.11') {
        $found = & py "-$v" -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $found) { return @{ Exe = ($found | Select-Object -First 1); Extra = @() } }
    }
    return @{ Exe = $MainExe; Extra = $MainExtra }
}

Push-Location -LiteralPath $PSScriptRoot

$exe = $null
$extra = @()
if ($Python) {
    if (Test-PythonCandidate $Python @()) { $exe = $Python }
} elseif (Test-PythonCandidate 'python' @()) {
    $exe = 'python'
} elseif (Test-PythonCandidate 'py' @('-3')) {
    $exe = 'py'
    $extra = @('-3')
}
if (-not $exe) {
    Stop-Setup "Python 3.10+ gerekli. (Windows'ta 'python3' yerine 'python' kullanin; gerekirse: .\setup.ps1 -Python <python.exe yolu>)"
}

if (-not (Test-Path '.venv\Scripts\python.exe')) {
    & $exe @extra -m venv .venv
    if ($LASTEXITCODE -ne 0) { Stop-Setup "'.venv' olusturulamadi." }
}
& .venv\Scripts\python.exe -m pip install -q --upgrade pip
& .venv\Scripts\python.exe -m pip install -q -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { Stop-Setup "Bagimliliklar kurulamadi (requirements-dev.txt). Agi/proxy'yi kontrol edip .\setup.ps1'i tekrar calistirin." }

if ($Scanners) {
    # semgrep pins its own opentelemetry versions; keep it away from the app venv.
    if (-not (Test-Path '.venv-tools\Scripts\python.exe')) {
        $tools = Find-ToolsPython $exe $extra
        & $tools.Exe @($tools.Extra) -m venv .venv-tools
        if ($LASTEXITCODE -ne 0) { Stop-Setup "'.venv-tools' olusturulamadi." }
    }
    & .venv-tools\Scripts\python.exe -m pip install -q --upgrade pip
    & .venv-tools\Scripts\python.exe -m pip install -q semgrep
    if ($LASTEXITCODE -ne 0) {
        Stop-Setup "semgrep kurulamadi. Python 3.14+ ile semgrep kurulmayabilir: Python 3.12 kurun (winget install Python.Python.3.12), '.venv-tools' klasorunu silip .\setup.ps1 -Scanners'i tekrar calistirin."
    }
}

Pop-Location
Write-Host ""
Write-Host "Kurulum tamam. Kontrol icin:  .\verify\run.ps1 m0"
Write-Host "Sanal ortami etkinlestirmek icin (istege bagli):  .\.venv\Scripts\Activate.ps1"
