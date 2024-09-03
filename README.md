# specialized-bikes
Get current bike info from Specialized's site

# Run Django Web app in development mode

## Prerequisites
1. Install postgres / psql 
2. add psql to PATH variable

## Adding postgres User for development
1. Open psql with default user: 
    ```sh
    psql -U postgres 
    ```
2. add new database user:
    ```psql
    create USER <DB_USER> with password <DB_PASSWORD>; 
    ```
3. Create New Database
    ```psql
    create DATABASE <DB_NAME>;
    ```
4. Grant access to new database to new user 
    ```psql
    GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <DB_USER>;
    GRANT ALL PRIVILEGES ON SCHEMA public TO <DB_USER>;
    GRANT ALL ON DATABASE <DB_NAME> TO <DB_USER>;
    ALTER DATABASE mydb OWNER TO myuser;
    GRANT USAGE, CREATE ON SCHEMA PUBLIC TO <DB_USER>;
    ```

## Confirm user and database have been created:
1. Connect to database
    ```sh
    psql -U specialized -h localhost -d specialized_bikes
    ```
2. When Prompted for password add the password from chosen when creating the user in Step A

## run Django app in development:
1. Create a virtual environment:
    ```py
    python -m venv <environment name>
    ```

2. Activate virtual environment:
    ```sh
    ./myenv/scripts/activate
    ```
3. Install dependencies:
    ```py
    pip install -r requirements.txt
    ```
4. Makemigrations:
    Change direcdtory to folder "webapp" (the folder containing the manage.py file)
    ```py
    python manage.py makemigrations 
    ```

5. Migrate:
    Change direcdtory to folder "webapp" (the folder containing the manage.py file)
    ```py
    python manage.py migrate
    ```

6. Run development server:
    ```py
    python manage.py runserver 
    ```

7. Optionally run on a different port
    ```py
    python manage.py runserver <PORT_NUMBER>
    ```

8. Go to locahost:8000 in the browser of your choice to confirm the web application has started.


## Set up formatting for .html documents
1. Install the Extension: Prettier - Code formatter
2. Install prettier development dependencies: 
```sh
npm install --save-dev prettier prettier-plugin-django
```
3. Add the following the to projects `settings.json`:
```json
{
  ...other settings,
  "editor.formatOnSave": true,
    "prettier.requireConfig": true,
    "[html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[django-html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
}
```

# Run from Docker
This assumes you're running Docker in a Linux WSL2 terminal but should work for Windows as well. 

1. Install Docker Desktop
2. Build the container image
    ```bash
    docker build -t specialized:latest .
    ```
3. Run the container
    ```bash
    docker run -d -p 5432:5432 -p 8000:8000 --name specialized_bikes_web -e POSTGRES_PASSWORD=mysecurepassword -e POSTGRES_DB=specialized_bikes -e POSTGRES_USER=specialized specialized:latest
    ```
4. Check the logs to ensure all is well
    ```bash
    docker logs specialized_bikes_web
    ```
5. Browse to the site:
    ```bash
    http://localhost:8000
    ```

