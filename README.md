# Fleet Tracking (Company ki 20 cars, owner ka ek login)

## Setup
    pip install -r requirements.txt

## Chalane ka tareeqa (2 terminals)

Terminal 1 - mock third-party provider:
    cd mock_provider
    uvicorn mock_provider:app --port 9000

Terminal 2 - backend (pehli dafa seed chalayen):
    cd backend
    python seed.py
    uvicorn main:app --port 8000 --reload

Swagger docs: http://localhost:8000/docs

## Demo login
    email: owner@demo.com
    password: owner123

## Test
    curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email":"owner@demo.com","password":"owner123"}'
    curl http://localhost:8000/vehicles -H "Authorization: Bearer <token>"

Note: SECRET_KEY production mein environment variable se lein.

## Frontend
    cd frontend
    python -m http.server 5500
    # browser: http://localhost:5500/login.html
(Backend aur mock provider pehle se chal rahe hon.)

## Docker se chalana (sab se aasan)
    # (optional) .env.example ko .env naam se copy kar ke SECRET_KEY likhein
    docker compose up --build

- Frontend: http://localhost:5500/login.html
- Backend docs: http://localhost:8000/docs
- Login: owner@demo.com / owner123

Roknay ke liye: `docker compose down`
Database bhi saaf karna ho: `docker compose down -v`
Logs dekhne ke liye: `docker compose logs -f backend`
