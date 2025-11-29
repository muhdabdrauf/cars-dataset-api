# Car Dataset API (FastAPI)

A simple FastAPI service for managing and querying a car dataset.

---

## 🚀 How to Run the Project

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Edit `.env` and set:
```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/car_db
CSV_PATH=
API_KEY=
```

Make sure PostgreSQL is running.

---

### 4. Run database migrations
```bash
alembic upgrade head
```

(This creates the `cars` table.)

---

### 5. Seed the database (optional)
```bash
python seed.py
```

(This imports cars from your CSV into the database.)

---

### 6. Start the FastAPI server
```bash
uvicorn app.main:app --reload
```

Server will start at:
http://127.0.0.1:8000

---

### 7. Open the interactive API docs

Swagger UI:  
http://127.0.0.1:8000/docs

ReDoc:  
http://127.0.0.1:8000/redoc
