# 🕒️ Easy Rostr API

**Easy Rostr API** is a Django-based RESTful service for managing employee time punch records. It allows
uploading and processing CSV files, tracks file history, validates data and supports pagination.

---

## 🧰 Tech Stack

- **Redis** for caching
- **Rabbitmq** as celery broker
- **MysQL** for data persistence
- **Celery** for asynchronous task execution
- **Docker** for containerization

---

---

## ⚙️ Main Technical Decisions

- **Django REST Framework**: Chosen for its robustness and ease of building RESTful APIs quickly.
- **MySQL**: Used as the primary relational database to store time punches.
- **Redis**: Utilized as a caching layer.
- **Celery**: Handles asynchronous background tasks.
- **Docker & Docker Compose**: Containerize the app and orchestrate dependencies like Redis and MySQL for easy setup and consistent environments.
- **Modular Project Structure**: Separates core utilities, shared code, and domain-specific apps for better maintainability.

---

## 🚀 Getting Started

### 🔧 Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/eliseup/erostr-api.git
   ```

---

### 🔧 Development Environment

After cloning the repository, follow these steps:

1. **Navigate to the `erostr-api` directory**
   ```bash
   cd erostr-api
   ```
   
2. **Create the logs directory**
   ```bash
   mkdir -p ./src/logs
   ```

3. **Create the development .env_dev file with initial content**
   ```bash
   echo -e "MYSQL_USER=erostr_dev\nMYSQL_PASSWORD=etr7011\nMYSQL_DATABASE=erostr_dev_db\nMYSQL_ROOT_PASSWORD=typ34pu\n\nDJANGO_DB_USER=erostr_dev\nDJANGO_DB_NAME=erostr_dev_db\nDJANGO_DB_PASSWORD=etr7011\nDJANGO_DB_HOST=mysql\n\nDJANGO_SETTINGS_MODULE=erostr_api.settings.dev\nDJANGO_SECRET_KEY=28859f16\n" > ./src/.env_dev
   ```

4. **Edit the .env_dev file accordingly**
   - Use any text editor you prefer.
   

5. **Build Docker images and Start the Development Containers**
    - To build the images:
    ```bash
   docker compose -f docker/docker-compose-build-dev.yml build 
   ```
    - To start the development environment, use the following command:
   ```bash
   docker compose -f docker/docker-compose-dev.yml up
   ```
    - To run the containers in the background, add the -d flag:
   ```bash
   docker compose -f docker/docker-compose-dev.yml up -d
   ```

In another terminal, access the containers:

6. **Access the application container**
   ```bash
   docker exec -it erostr-dev-app-1 bash
   ```   
    - **Apply migrations**
      ```bash
      python manage.py migrate
      ```
      
    - **Run tests:**
      ```bash
      python manage.py test
      ```

    - **Start the Django development server:**
      ```bash
      python manage.py runserver 0.0.0.0:8000
      ```

**Port Mapping for Django Development Server**

- **Container Port**: `8000`
- **Host Port**: `8010`

The Django development server runs on port `8000` inside the Docker container. This port is exposed to the host machine on port `8010`

- Access the server **on the host machine** at `http://localhost:8010`


---

### 🔧 Production Environment

After cloning the repository, follow these steps:

1. **Navigate to the `erostr-api` directory**
   ```bash
   cd erostr-api
   ```

2. **Build the application Docker images**
   ```bash
   docker compose -f docker/docker-compose-build-prod.yml build 
   ```

3. **Apply migrations**
   ```bash
   docker compose -f docker/docker-compose-prod.yml run --rm app bash -c "sleep 7 && python app/manage.py migrate"
   ```

4. **Start the Application**
   ```bash
   docker compose -f docker/docker-compose-prod.yml up
   ```

**Port Mapping for Production Application**

- **Container Port**: `8000`
- **Host Port**: `8088`

The production application runs on port `8000` inside the Docker container. This port is exposed to the host machine on port `8088`

- Access the application **on the host machine** at `http://localhost:8088`

---

# API Endpoints Documentation
*Production environment*

## Base URL
`http://localhost:8088/api/v1`
---

## ⚠️ Note about Production Environment

The production environment has **not been fully tested** in this project.  
It is included only to serve as a basic example or starting point.  

Further configuration and testing are needed before using it in a real production scenario.

---