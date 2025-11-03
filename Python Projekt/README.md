# 🏨 Hotels Booking Project

> A full-featured hotel booking application built with **Python** and **FastAPI**.  
> It supports user registration and authentication, hotel and room management, bookings, image uploads, and background task processing.

---

## 🌐 Live Demo
📘 **Interactive API documentation (Swagger UI):** [https://bookingprojekt.ru/docs#](https://bookingprojekt.ru/docs#)


---

## 🚀 Tech Stack

- 🐍 **Python 3.11+**
- ⚙️ **FastAPI** — high-performance web framework
- 🧱 **SQLAlchemy** — ORM for database operations
- 🐘 **PostgreSQL** — main relational database
- 🧵 **Celery + Redis** — background task queue
- 🐳 **Docker** — containerization
- 🧩 **Nginx + Uvicorn** — production web server setup
- ✅ **Pytest** — testing framework

---

## 📦 Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/Yurybar93/Hotels.git
cd Hotels
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables  
Create a `.env` file in the root directory and add your configuration:
```env
# Database configuration
DB_HOST=booking_db
DB_PORT=5432
DB_USER=<username>
DB_PASS=<password>
DB_NAME=booking

# Redis configuration
REDIS_HOST=booking_cache
REDIS_PORT=6379

# JWT settings
JWT_SECRET_KEY=<your_jwt_secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ Do **not** include real credentials in this file when committing to GitHub.  
> Make sure `.env` is listed in your `.gitignore`.

### 5. Run the FastAPI app
```bash
uvicorn src.main:app --reload
```

Now open your browser at 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Run with Docker

### 1. Build and start the app container
```bash
docker-compose up --build
```

The app will automatically build and start inside a container.  
Visit [http://localhost:8000](http://localhost:8000) to access the API.

### 2. Stop and remove containers
```bash
docker-compose down
```

---

### 🧪 Test Environment

For running automated tests, the project uses a separate environment file — `.env-test`.

This file should contain the same variables as `.env`,  
but configured for a **local test database** and **Redis instance**, for example:

```env
MODE=TEST

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=<test_password>
DB_NAME=test

REDIS_HOST=localhost
REDIS_PORT=6379

JWT_SECRET_KEY=<test_secret_key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Running Tests

Run all tests using **pytest**:
```bash
pytest -v
```

Test files are located in the `tests/` directory.

---

## 🌐 API Documentation

FastAPI provides auto-generated interactive documentation:

- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)
- Live version → [https://bookingprojekt.ru/docs#](https://bookingprojekt.ru/docs#)

---

## 🧰 Deployment Details

The production environment runs on a Linux server using **Docker containers**.  
PostgreSQL and Nginx are started as **separate containers** (not part of `docker-compose`), and all services share the same custom Docker network.

### 1. PostgreSQL database container
```bash
docker run --name booking_db     
-p 6432:5432     
-e POSTGRES_USER=<username>     
-e POSTGRES_PASSWORD=<password>     
-e POSTGRES_DB=booking     
--network=my_network     
--volume pg_booking_data:/var/lib/postgresql/data     
-d postgres:16
```

**Notes:**
- The database listens on host port `6432`.
- Data is persisted in the named volume `pg_booking_data`.
- The `.env` file must use this hostname for internal communication:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@booking_db:5432/booking
```

---

### 2. Application container
The FastAPI app container connects to the same Docker network (`my_network`)  
and communicates with the `booking_db` service internally.

All environment variables are passed from the `.env` file.

---

### 3. Nginx reverse proxy (HTTPS / SSL)
```bash
docker run --name booking_nginx     
--volume ./nginx.conf:/etc/nginx/nginx.conf     
--volume /etc/letsencrypt/:/etc/letsencrypt   
--volume /var/lib/letsencrypt:/var/lib/letsencrypt    
 --network=my_network     
 --rm -p 443:443 nginx
```

**Notes:**
- Nginx proxies HTTPS traffic on port `443` to the FastAPI app container.  
- SSL certificates are provided from `/etc/letsencrypt/`.  
- The Nginx configuration file defines upstream routing to your app.

---

### 4. Network & orchestration
- All containers (FastAPI app, DB, Nginx, Redis, Celery, etc.) are connected to the same Docker network:  
  `my_network`.
- This isolates internal traffic and exposes only Nginx on port `443` publicly.
- Persistent volumes are used for database and certificates.

---

### 5. Summary

| Component      | Technology               | Notes                        |
|----------------|--------------------------|-------------------------------|
| OS             | Ubuntu 22.04             |                              |
| Reverse proxy  | Nginx                    | SSL via Let's Encrypt         |
| App server     | Uvicorn / Gunicorn       |                              |
| Database       | PostgreSQL 16            | Runs as separate container   |
| Task queue     | Celery + Redis           | Background processing        |
| Container mgmt | Docker                   | Manual orchestration         |

---

## 👨‍💻 Author

**Iurii Barynin**  
📧 [yury.barynin@gmail.com](mailto:yury.barynin@gmail.com)  
🌐 GitHub: [Yurybar93](https://github.com/Yurybar93)  
💼 LinkedIn: [Iurii Barynin](https://www.linkedin.com/in/iuriibarynin/)

---

> 💡 Tip: Add GitHub badges for Python version, build status, and license —  
> they’ll automatically appear at the top of your README.
