# BookingAPI - FastAPI + SQLite3

Simple Fitness Class booking API using FastAPI & SQLite3


# Features
1. View all fitness classes 
2. Book a class
3. View bookings by client email
4. Timezone conversion 
5. SQLite3 local file DB
6. Error handling and validation


# Instructions
1. Unzip the project
2. Activate the virtual environment (.venv):
    .\.venv\Scripts\activate
3. Start the server:
    uvicorn main:app --reload

# Postman
1. Show all classes:
http://127.0.0.1:8000/classes
Method: GET

2. Timezone conversion:
http://127.0.0.1:8000/classes?tz=Europe/London
Method: GET

3. Book a class:
http://127.0.0.1:8000/book
Method: POST
Headers: Content-Type - application/json
Body (JSON): 
{
  "class_id": 3,
  "client_name": "Jack",
  "client_email": "jack@gmail.com"
}

4. Show bookings with client email
http://127.0.0.1:8000/bookings?email=jack@gmail.com
Method: GET



