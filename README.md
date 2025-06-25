# BookingAPI - FastAPI + SQLite3

Simple Fitness Class booking API using FastAPI & SQLite3


# Features
1. View all fitness classes 
2. Book a class
3. View bookings by client email
4. Timezone conversion 
5. SQLite3 local file DB
6. Error handling and validation


# Technologies Used
1. Python 3.10.11
2. FastAPI
3. SQLite3
4. pytz (Timezone management)

# Instructions
1. Download the project
2. Create a virtual Environment
  python -m venv .venv

3. Activate the virtual environment (.venv):
    .\.venv\Scripts\activate

4. Install dependencies:
  pip install -r requirements.txt

5. Start the server:
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


# Swagger 

http://127.0.0.1:8000/docs



## 🎥 Demo / Walkthrough Video

Watch the full project walkthrough on Loom:  
👉 [Click here to watch](https://www.loom.com/share/6e3620d227ec4672bc41a027751734b3?sid=c06a7993-fcd2-4f35-bb52-5b3911e590ec)




