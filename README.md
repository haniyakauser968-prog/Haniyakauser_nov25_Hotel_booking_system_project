# Hotel Booking System

A beginner-friendly single-page hotel booking application built with Python, FastAPI, HTML, CSS, and SQLite.

## Features
- Single-page responsive booking form
- Customer contact details
- Check-in and check-out date validation
- Guest count and room selection
- FastAPI backend
- SQLite database storage
- Booking confirmation with booking ID
- API endpoint to view saved bookings

## Project structure
```text
Hotel_Booking_System/
├── main.py
├── requirements.txt
├── hotel.db              # created automatically when the app starts
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run in VS Code

1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Create and activate a virtual environment (recommended):

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

7. Open this address in your browser:
   http://127.0.0.1:8000

The `hotel.db` SQLite database and `bookings` table are created automatically when the application starts.

## API endpoints
- `GET /` — displays the booking page
- `POST /api/bookings` — validates and saves a booking
- `GET /api/bookings` — returns saved bookings as JSON
- `GET /docs` — interactive FastAPI API documentation

## Database
SQLite is used, so no separate database server or password setup is needed. Booking records are stored in `hotel.db` in the project folder.

## Note
This is an educational mini-project. It does not yet include payment processing, user login, room availability management, or an admin dashboard.
