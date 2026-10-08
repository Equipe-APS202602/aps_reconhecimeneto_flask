<#
Script PowerShell para instalar cada dependência individualmente
Uso: Execute em PowerShell: .\scripts\install-deps.ps1
#>
$ErrorActionPreference = 'Stop'

$packages = @(
    'Flask',
    'opencv-contrib-python',
    'mysql-connector-python',
    'python-dotenv',
    'Flask-Login',
    'bcrypt'
)

foreach ($p in $packages) {
    Write-Host "Instalando $p..." -ForegroundColor Cyan
    python -m pip install $p --upgrade
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha ao instalar $p (exit code $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

Write-Host "Todas as dependências foram instaladas com sucesso." -ForegroundColor Green
