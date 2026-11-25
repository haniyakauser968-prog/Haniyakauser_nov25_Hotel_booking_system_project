from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hotel.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                guests INTEGER NOT NULL,
                room_type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Hotel Booking System", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    phone: str = Field(min_length=7, max_length=20)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=10)
    room_type: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/api/bookings")
async def create_booking(booking: BookingCreate):
    if "@" not in booking.email or "." not in booking.email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    if booking.check_in < date.today():
        raise HTTPException(status_code=400, detail="Check-in date cannot be in the past.")
    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in.")
    allowed_rooms = {"Standard", "Deluxe", "Suite"}
    if booking.room_type not in allowed_rooms:
        raise HTTPException(status_code=400, detail="Please select a valid room type.")

    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO bookings
            (customer_name, email, phone, check_in, check_out, guests, room_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            booking.customer_name.strip(), str(booking.email), booking.phone.strip(),
            booking.check_in.isoformat(), booking.check_out.isoformat(),
            booking.guests, booking.room_type
        ))
        booking_id = cursor.lastrowid

    return {"message": "Booking confirmed successfully!", "booking_id": booking_id}

@app.get("/api/bookings")
async def get_bookings():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, customer_name, email, phone, check_in, check_out,
                   guests, room_type, created_at
            FROM bookings ORDER BY id DESC
        """).fetchall()
    return [dict(row) for row in rows]