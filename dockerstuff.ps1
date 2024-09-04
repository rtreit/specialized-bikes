Write-Host "Building locally"
docker build -t specialized:latest .
Write-Host "Removing running instances"
docker rm specialized_bikes_web --force
Write-Host "Running locally"
docker run -d -p 5432:5432 -p 8000:8000 --name specialized_bikes_web -e POSTGRES_PASSWORD=mysecurepassword -e POSTGRES_DB=specialized_bikes -e POSTGRES_USER=specialized specialized:latest
Write-Host "Building for container registry"
docker build -t paincave.azurecr.io/specialized:latest .
Write-Host "Pushing to container registry"
docker push paincave.azurecr.io/specialized:latest
Write-Host "Restarting Web App"
az webapp restart --name paincave-webapp --resource-group paincave
