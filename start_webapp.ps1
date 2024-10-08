function Set-Environment-Variables {
    Write-Host "setting env variables"
    $env:POSTGRES_PASSWORD = "specialized"
    $env:POSTGRES_DB = "specialized_bikes"
    $env:POSTGRES_USER = "specialized"
    $env:POSTGRES_HOST = "localhost"
    $env:POSTGRES_PORT = 5432
    $env:DEBUG = 1
}

function Start-Webapp {
    Set-Environment-Variables
    $virtualEnvironmentPath = rg --files --glob "Activate.ps1" --hidden --no-ignore .
    $managePyPath = rg --files --glob "manage.py" --hidden --no-ignore .
    if ((Test-Path $virtualEnvironmentPath) -and (Test-Path $managePyPath)){
        & $virtualEnvironmentPath
        & python $managePyPath runserver
    } else {
        Write-Host "Could not start webapp (virtual environment or manage.py could not be found)"
        Write-Host "Virtual Env Path: $virtualEnvironmentPath"
        Write-Host "Manage.py Path: $managePyPath"
    }

}

Start-Webapp