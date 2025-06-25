from fastapi import FastAPI, HTTPException, Query, Body
from db import create_tables, add_classes, get_connection
from models import FitnessClass, BookingRequest, BookingResponse
from typing import List, Optional
from utils import convert_timezone
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

create_tables()
add_classes()


@app.get('/classes', response_model=List[FitnessClass])
def get_classes(tz: str = Query("Asia/Kolkata", description="Target Timezone (e.g., America/New_York)")):
    logging.info(f"Fetching all classes, converting to timezone: {tz}")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fitness_classes")
    rows = cursor.fetchall()
    conn.close()

    classes = []
    for row in rows:
        row_dict = dict(row)
        row_dict["datetime"] = convert_timezone(
            dt_str=row_dict["datetime"],
            from_tz="Asia/Kolkata",
            to_tz=tz
        )
        classes.append(FitnessClass(**row_dict))

    return classes


@app.post('/book') #@app.post('/book', response_model=BookingResponse)
def book_class(request: BookingRequest):
    logging.info(f"Received booking request for class_id={request.class_id} from {request.client_email}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fitness_classes WHERE id = ?",(request.class_id,))
    cls = cursor.fetchone()
    if not cls:
        logging.warning(f"Booking failed: Class ID {request.class_id} not found.")
        raise HTTPException(status_code=404, detail="Class not found")

    if cls["available_slots"] <= 0:
        logging.warning(f"Booking failed: No slots left for Class ID {request.class_id}")
        raise HTTPException(status_code=409, detail="No Slots available")

    cursor.execute('''
        UPDATE fitness_classes 
        SET available_slots = available_slots-1 WHERE id = ?''',(request.class_id,)
        )

    cursor.execute("INSERT INTO bookings (class_id, client_name, client_email) VALUES (?,?,?)",
    (request.class_id, request.client_name, request.client_email)
    )

    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()

    logging.info(f"Booking Confirmed: ID={booking_id} for {request.client_email} (class_id={request.class_id})")

    return {
        "message":"Booking Successful",
        "data": BookingResponse(
            booking_id=booking_id,
            class_id=request.class_id,
            client_name=request.client_name,
            client_email=request.client_email
            ).dict(exclude_none=True)
        }


@app.get('/bookings', response_model=List[BookingResponse])
def get_bookings(email: Optional[str] = Query(None, description="Client email")):

    conn = get_connection()
    cursor = conn.cursor()

    if email:
        logging.info(f"Retrieving bookings for: {email}")
        #cursor.execute("SELECT * FROM bookings WHERE client_email = ?", (email,))
        cursor.execute("""
            SELECT b.booking_id, b.class_id, f.name AS class_name, b.client_name, b.client_email, f.datetime
            FROM bookings b
            JOIN fitness_classes f ON b.class_id = f.id
            WHERE b.client_email = ?
            """, (email,))
    else:
        cursor.execute("""
        SELECT b.booking_id, b.class_id, f.name AS class_name, b.client_name, b.client_email, f.datetime
        FROM bookings b
        JOIN fitness_classes f ON b.class_id = f.id
        """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No Bookings found")
    
    bookings = [BookingResponse(**dict(row)) for row in rows]
    return bookings


@app.post('/reset-class')
def reset_classes(class_name: str = Body(..., embed=True), slots: int = Body(5, embed=True)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fitness_classes WHERE name = ?", (class_name,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Class not found")
    
    cursor.execute("UPDATE fitness_classes SET available_slots = ? WHERE name = ?", (slots, class_name))
    conn.commit()
    conn.close()

    return {"message":f"Class '{class_name}' reset with {slots} slots."}


@app.delete('/bookings/delete')
def clear_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings")
    conn.commit()
    conn.close()
    
    return {"message":"Cleared all bookings."}


@app.get('/')
async def hello():
    return {"message":"Welcome to the Fitness Club !!!"}

