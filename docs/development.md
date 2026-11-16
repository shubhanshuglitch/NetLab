# NetLab Development & Testing Guide

## Prerequisites
- **Python**: 3.10+
- **Node.js**: v18+ (tested on Node v20 & v24)
- **npm**: 9+

---

## 1. Backend Setup

```bash
# Create and activate virtual environment
python -m venv backend_venv
# On Windows PowerShell:
.\backend_venv\Scripts\Activate.ps1
# On Linux / macOS:
source backend_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend development server
uvicorn backend.app.main:app --reload --port 8000
```

Backend will be active at `http://127.0.0.1:8000`.
Interactive Swagger API documentation: `http://127.0.0.1:8000/docs`.

---

## 2. Frontend Setup

```bash
cd frontend

# Install packages
npm install

# Start Vite dev server with proxy
npm run dev
```

Frontend will be active at `http://localhost:5173`.

---

## 3. Running Automated Tests

```bash
# Run backend pytest suite (20 unit and integration tests)
python -m pytest backend/app/tests/ -v

# Run frontend production build verification
cd frontend
npm run build
```

---

## 4. Docker Deployment

```bash
# Run both frontend and backend using Docker Compose
docker-compose up --build
```

