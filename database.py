"""
Database setup, schema migration, and initial seeding for Peacock Library Management System.
Includes all 31 student records provided in the student details sheet.
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'peacock_library.db')

STUDENT_DATA = [
    (1, "23GK1A0501", "A.RAJESH", "4TH B.TECH", "CSE"),
    (2, "23GK1A0502", "A.PRAVEEN", "4TH B.TECH", "CSE"),
    (3, "23GK1A0503", "B.NAGENDRA BABU", "4TH B.TECH", "CSE"),
    (4, "23GK1A0504", "CH. ANAND KUMAR", "4TH B.TECH", "CSE"),
    (5, "23GK1A0505", "D.SIRESHA", "4TH B.TECH", "CSE"),
    (6, "23GK1A0506", "D.BALA ARJUN", "4TH B.TECH", "CSE"),
    (7, "23GK1A0508", "G.GAYATHRI", "4TH B.TECH", "CSE"),
    (8, "23GK1A0510", "J.PREETHI", "4TH B.TECH", "CSE"),
    (9, "23GK1A0511", "J.VIMALA", "4TH B.TECH", "CSE"),
    (10, "23GK1A0513", "K.DEEPTHI", "4TH B.TECH", "CSE"),
    (11, "23GK1A0514", "K.V.SAI REDDY", "4TH B.TECH", "CSE"),
    (12, "23GK1A0515", "K.DINESH", "4TH B.TECH", "CSE"),
    (13, "23GK1A0516", "K.KEERTHANA", "4TH B.TECH", "CSE"),
    (14, "23GK1A0517", "K.VASU DEVA RAO", "4TH B.TECH", "CSE"),
    (15, "23GK1A0522", "O.PRAVEEN", "4TH B.TECH", "CSE"),
    (16, "23GL1A0524", "P.MOUNIKA", "4TH B.TECH", "CSE"),
    (17, "23GL1A0525", "P.AKSHAY SAI GOVARDHAN", "4TH B.TECH", "CSE"),
    (18, "23GK1A0532", "S.JYOSTANA", "4TH B.TECH", "CSE"),
    (19, "23GK1A0533", "S.THARUN KUMAR", "4TH B.TECH", "CSE"),
    (20, "23GK1A0534", "S.SUBHASH", "4TH B.TECH", "CSE"),
    (21, "23GK1A0436", "T.BHANU PRAKASH", "4TH B.TECH", "CSE"),
    (22, "23GK1A0437", "T.PRANEESH", "4TH B.TECH", "CSE"),
    (23, "23GK1A0438", "U.VARSHITHA", "4TH B.TECH", "CSE"),
    (24, "23GK1A0439", "V.ASRITHA", "4TH B.TECH", "CSE"),
    (25, "23GK1A0544", "B.CHINNARAJU", "4TH B.TECH", "CSE"),
    (26, "23GK1A0548", "E.PAVAN", "4TH B.TECH", "CSE"),
    (27, "23GK1A0549", "K.VYSHNAVI", "4TH B.TECH", "CSE"),
    (28, "23GK1A0554", "MD.SHOIAB", "4TH B.TECH", "CSE"),
    (29, "23GK1A0557", "SK.SALAR", "4TH B.TECH", "CSE"),
    (30, "23GK1A0558", "J.SREE DEVI", "4TH B.TECH", "CSE"),
    (31, "24GK1A0501", "N.ARJUN", "4TH B.TECH", "CSE (LATERAL)")
]

BOOK_DATA = [
    ("978-0132350884", "Clean Code: Agile Software Craftsmanship", "Robert C. Martin", "Software Engineering", 6, 5, "Shelf A-101"),
    ("978-0262033848", "Introduction to Algorithms (CLRS 4th Ed)", "Thomas H. Cormen, C. Leiserson", "Algorithms & DS", 8, 5, "Shelf A-102"),
    ("978-0131103627", "The C Programming Language (2nd Ed)", "Brian W. Kernighan, Dennis Ritchie", "Programming", 5, 4, "Shelf B-201"),
    ("978-0134685991", "Effective Java (3rd Edition)", "Joshua Bloch", "Java Programming", 7, 6, "Shelf B-202"),
    ("978-0136083207", "Artificial Intelligence: A Modern Approach", "Stuart Russell, Peter Norvig", "AI & Machine Learning", 5, 3, "Shelf C-301"),
    ("978-0078022159", "Database System Concepts (7th Edition)", "Abraham Silberschatz, Henry Korth", "Database Systems", 9, 7, "Shelf D-401"),
    ("978-0133594140", "Operating System Concepts (10th Edition)", "Silberschatz, Galvin, Gagne", "Operating Systems", 8, 6, "Shelf D-402"),
    ("978-0132126953", "Computer Networks: Principles and Protocols", "Andrew S. Tanenbaum", "Computer Networks", 7, 5, "Shelf E-501"),
    ("978-1491957660", "Designing Data-Intensive Applications", "Martin Kleppmann", "Cloud & Distributed", 6, 5, "Shelf E-502"),
    ("978-1593279288", "Python Crash Course (3rd Edition)", "Eric Matthes", "Python Programming", 10, 8, "Shelf B-203"),
    ("978-1449355730", "Full Stack Web Development with React & Node", "Jennifer Robbins, Colin Ihrig", "Web Development", 6, 5, "Shelf F-601"),
    ("978-1718502703", "Black Hat Python: Python for Hackers", "Justin Seitz, Tim Arnold", "Cybersecurity", 5, 4, "Shelf F-602"),
    ("978-1492041139", "Deep Learning & Neural Networks Practical", "Sebastian Raschka, Yuxi Liu", "AI & Machine Learning", 6, 5, "Shelf C-302"),
    ("978-0134494166", "Cloud Computing: Architecture & Services", "Thomas Erl, Zaigham Mahmood", "Cloud & Distributed", 5, 4, "Shelf E-503"),
    ("978-0596517748", "JavaScript: The Good Parts", "Douglas Crockford", "Web Development", 4, 3, "Shelf B-204"),
    ("978-0321751041", "The Art of Computer Programming (Vol 1)", "Donald E. Knuth", "Computer Science Theory", 3, 3, "Shelf A-103")
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed=False):
    conn = get_db()
    cursor = conn.cursor()

    if force_reseed:
        cursor.execute("DROP TABLE IF EXISTS issues")
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("DROP TABLE IF EXISTS students")

    # 1. Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sl_no INTEGER,
            roll_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            year_of_study TEXT NOT NULL,
            branch TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            avatar_seed TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            total_copies INTEGER NOT NULL DEFAULT 1,
            available_copies INTEGER NOT NULL DEFAULT 1,
            shelf_location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Issues / Borrowings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            status TEXT NOT NULL CHECK(status IN ('issued', 'returned', 'overdue')),
            fine_amount REAL DEFAULT 0.0,
            fine_paid INTEGER DEFAULT 0,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    """)

    conn.commit()

    # Seed Students if table empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        phone_counter = 9848020000
        for sl_no, roll, name, year, branch in STUDENT_DATA:
            email = f"{roll.lower()}@college.edu.in"
            phone = f"+91 {phone_counter + sl_no}"
            cursor.execute("""
                INSERT INTO students (sl_no, roll_number, name, year_of_study, branch, email, phone, avatar_seed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sl_no, roll, name, year, branch, email, phone, roll))
        conn.commit()
        print(f"[OK] Successfully seeded {len(STUDENT_DATA)} students from sheet.")

    # Seed Books if table empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        for isbn, title, author, cat, total, avail, shelf in BOOK_DATA:
            cursor.execute("""
                INSERT INTO books (isbn, title, author, category, total_copies, available_copies, shelf_location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (isbn, title, author, cat, total, avail, shelf))
        conn.commit()
        print(f"[OK] Successfully seeded {len(BOOK_DATA)} books.")

    # Seed Initial Transactions / Issues if table empty
    cursor.execute("SELECT COUNT(*) FROM issues")
    if cursor.fetchone()[0] == 0:
        today = datetime.now().date()
        
        sample_issues = [
            # Active (Issued)
            (1, 1, today - timedelta(days=5), today + timedelta(days=9), None, 'issued', 0.0, 0, "Reference for Major Project"),
            (2, 2, today - timedelta(days=4), today + timedelta(days=10), None, 'issued', 0.0, 0, "Algorithms preparation"),
            (5, 4, today - timedelta(days=8), today + timedelta(days=6), None, 'issued', 0.0, 0, "AI Lab curriculum"),
            (6, 6, today - timedelta(days=2), today + timedelta(days=12), None, 'issued', 0.0, 0, "Database query optimization"),
            (7, 8, today - timedelta(days=6), today + timedelta(days=8), None, 'issued', 0.0, 0, "OS Kernel study"),
            (8, 12, today - timedelta(days=3), today + timedelta(days=11), None, 'issued', 0.0, 0, "Networking protocols"),
            (10, 15, today - timedelta(days=7), today + timedelta(days=7), None, 'issued', 0.0, 0, "Python scripting"),
            
            # Overdue issues (with fine calculated: fine rate ₹2 per day late)
            (2, 17, today - timedelta(days=20), today - timedelta(days=6), None, 'overdue', 12.0, 0, "Renewal overdue by 6 days"),
            (6, 21, today - timedelta(days=22), today - timedelta(days=8), None, 'overdue', 16.0, 0, "Semester exam review overdue"),
            (7, 28, today - timedelta(days=18), today - timedelta(days=4), None, 'overdue', 8.0, 0, "Coursework reference"),

            # Returned issues (with history)
            (3, 3, today - timedelta(days=30), today - timedelta(days=16), today - timedelta(days=18), 'returned', 0.0, 1, "Returned on time"),
            (4, 5, today - timedelta(days=25), today - timedelta(days=11), today - timedelta(days=10), 'returned', 0.0, 1, "Good condition"),
            (10, 10, today - timedelta(days=15), today - timedelta(days=1), today - timedelta(days=2), 'returned', 0.0, 1, "Returned peacefully"),
            (12, 16, today - timedelta(days=24), today - timedelta(days=10), today - timedelta(days=8), 'returned', 4.0, 1, "Fine paid at desk")
        ]

        for b_id, s_id, iss_d, due_d, ret_d, st, fine, paid, rem in sample_issues:
            cursor.execute("""
                INSERT INTO issues (book_id, student_id, issue_date, due_date, return_date, status, fine_amount, fine_paid, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (b_id, s_id, iss_d.isoformat(), due_d.isoformat(), ret_d.isoformat() if ret_d else None, st, fine, paid, rem))

        conn.commit()
        print("[OK] Successfully seeded initial library transactions.")

    conn.close()

def update_overdue_statuses(fine_per_day=2.0):
    """Automatically updates overdue statuses and calculates dynamic fines based on current date."""
    conn = get_db()
    cursor = conn.cursor()
    today_str = datetime.now().date().isoformat()
    today = datetime.now().date()

    # Find all 'issued' or 'overdue' records that have not been returned yet
    cursor.execute("""
        SELECT id, due_date, status, fine_paid FROM issues
        WHERE return_date IS NULL
    """)
    records = cursor.fetchall()
    for row in records:
        issue_id = row['id']
        due_date = datetime.strptime(row['due_date'], "%Y-%m-%d").date()
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * fine_per_day
            cursor.execute("""
                UPDATE issues SET status = 'overdue', fine_amount = ? WHERE id = ?
            """, (fine, issue_id))
        else:
            if row['status'] == 'overdue':
                cursor.execute("UPDATE issues SET status = 'issued', fine_amount = 0.0 WHERE id = ?", (issue_id,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db(force_reseed=True)
    update_overdue_statuses()
    print("Database initialization complete.")
