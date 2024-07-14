# GoodReads-simple
## FastAPI simple Project 

## 
## Installation



Install the dependencies and devDependencies and start the server.
1- Clone  the repository:
```sh
cd GoodReads-simple
docker-compose up --build -d
docker-compose exec fastapi-app python db_fake_data_initiator.py
```

Access the FastAPI application:

Navigate to http://localhost:8010/docs in your browser.
Click on the "Authorize" button (green button on the upper right).
Use the default admin credentials provided in the Docker Compose environment variables.
Login using the default admin user and password.
Default Admin Credentials
Username: admin@example.com
Password: 123321456
Project Structure
app/: Contains the FastAPI application code.
db_fake_data_initiator.py: Script to initialize fake data into the PostgreSQL database.
docker-compose.yml: Docker Compose configuration file.
Dockerfile: Dockerfile for building the FastAPI application container.
