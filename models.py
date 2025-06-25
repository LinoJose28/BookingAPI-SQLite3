from pydantic import BaseModel, EmailStr
from typing import Optional

class FitnessClass(BaseModel):
    id: int
    name: str
    datetime: str
    instructor: str
    available_slots: int

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingResponse(BaseModel):
    booking_id: int
    class_id: int
    class_name: Optional[str] = None
    client_name: str
    client_email: EmailStr
    datetime: Optional[str] = None