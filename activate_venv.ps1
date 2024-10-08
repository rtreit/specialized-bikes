function Set-Environment-Variables {
    Write-Host "setting env variables"
    $env:POSTGRES_PASSWORD = "specialized"
    $env:POSTGRES_DB = "specialized_bikes"
    $env:POSTGRES_USER = "specialized"
    $env:POSTGRES_HOST = "localhost"
    $env:POSTGRES_PORT = 5432
    $env:DEBUG = 1
}

function Activate-VirtualEnvironment {
    Set-Environment-Variables
    $virtualEnvironmentPath = rg --files --glob "Activate.ps1" --hidden --no-ignore .
    if (Test-Path $virtualEnvironmentPath){
        Write-Host "Activating Virtual Environment $virtualEnvironmentPath"
        & $virtualEnvironmentPath
    } else {
        Write-Host "Could activate virtual environment."
        Write-Host "Virtual Env Path: $virtualEnvironmentPath"
    }

}

Activate-VirtualEnvironment