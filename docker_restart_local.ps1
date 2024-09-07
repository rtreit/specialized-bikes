# Write-Host "Building locally"
# docker build -t specialized:latest .
$runningContainer = docker ps -f name=specialized_bikes_web
Write-Host "Running Container: $runningContainer"
if ($runningContainer){
    Write-Host "Removing running instances"
    Write-Host "Stopping Container $runningContainer"
    docker rm specialized_bikes_web --force
} else {
    Write-Host "No instances running"
}
Write-Host "running docker locally with command:"
Write-Host "docker run -p 5432:5432 -p 8000:8000 -p 5672:5672 -p 15672:15672 --name specialized_bikes_web -e POSTGRES_PASSWORD=mysecurepassword -e POSTGRES_DB=specialized_bikes -e POSTGRES_USER=specialized specialized:latest"
docker run -p 5432:5432 -p 8000:8000 -p 5672:5672 -p 15672:15672 --name specialized_bikes_web -e POSTGRES_PASSWORD=mysecurepassword -e POSTGRES_DB=specialized_bikes -e POSTGRES_USER=specialized specialized:latest
