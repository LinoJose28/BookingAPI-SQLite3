import sqlite3

def get_connection():
    conn = sqlite3.connect("studio.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fitness_classes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        datetime TEXT NOT NULL,
        instructor TEXT NOT NULL,
        available_slots INTEGER NOT NULL 
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        client_name TEXT NOT NULL,
        client_email TEXT NOT NULL,
        FOREIGN KEY(class_id) REFERENCES fitness_class(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_classes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM fitness_classes")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_data = [
            (1, "Yoga", "2025-06-25T10:00:00", "Rahul", 5),
            (2, "Zumba", "2025-06-26T16:00:00", "Kevin", 4),
            (3, "HIIT", "2025-06-27T07:00:00", "Ajay", 3)
        ]

        cursor.executemany('''
        INSERT INTO fitness_classes (id, name, datetime, instructor, available_slots)
        VALUES (?,?,?,?,?)
        ''', sample_data)

        print("✅ Added sample classes into database.")


    conn.commit()
    conn.close()