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

