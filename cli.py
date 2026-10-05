"""
Mayura Library Management System - Interactive Terminal Console Edition
Allows librarians and students to interact with the database via command line.
"""

import sys
from datetime import datetime, timedelta
from database import get_db, init_db, update_overdue_statuses

# Reconfigure stdout for utf-8 on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_banner():
    peacock_tag = "[PEACOCK]"
    print(f"""
{CYAN}{BOLD}========================================================================
   {peacock_tag}  MAYURA LIBRARY MANAGEMENT SYSTEM - CONSOLE EDITION  {peacock_tag}
         4th B.Tech CSE Department Roster (31 Students Loaded)
========================================================================{RESET}
""")

def list_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sl_no, roll_number, name, year_of_study, branch FROM students ORDER BY roll_number ASC")
    rows = cursor.fetchall()
    conn.close()

    print(f"\n{YELLOW}{BOLD}--- REGISTERED CSE STUDENT ROSTER ({len(rows)} Students) ---{RESET}")
    print(f"{'SL':<4} {'ROLL NUMBER':<14} {'STUDENT NAME':<26} {'YEAR':<12} {'BRANCH':<10}")
    print("-" * 68)
    for r in rows:
        print(f"{r['sl_no']:<4} {CYAN}{r['roll_number']:<14}{RESET} {r['name']:<26} {r['year_of_study']:<12} {GREEN}{r['branch']:<10}{RESET}")
    print("-" * 68)

def list_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, isbn, title, author, category, available_copies, total_copies, shelf_location FROM books ORDER BY title ASC")
    rows = cursor.fetchall()
    conn.close()

    print(f"\n{YELLOW}{BOLD}--- BOOK CATALOG INVENTORY ({len(rows)} Titles) ---{RESET}")
    print(f"{'ID':<4} {'TITLE':<38} {'AUTHOR':<24} {'STOCK':<10} {'SHELF':<12}")
    print("-" * 90)
    for r in rows:
        stock = f"{r['available_copies']}/{r['total_copies']}"
        color = GREEN if r['available_copies'] > 0 else MAGENTA
        print(f"{r['id']:<4} {r['title'][:36]:<38} {r['author'][:22]:<24} {color}{stock:<10}{RESET} {CYAN}{r['shelf_location']:<12}{RESET}")
    print("-" * 90)

def list_issues():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, s.roll_number, s.name, b.title, i.issue_date, i.due_date, i.status, i.fine_amount
        FROM issues i
        JOIN students s ON i.student_id = s.id
        JOIN books b ON i.book_id = b.id
        ORDER BY i.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    print(f"\n{YELLOW}{BOLD}--- ACTIVE & RECENT TRANSACTIONS ---{RESET}")
    print(f"{'ID':<5} {'ROLL NO':<14} {'STUDENT':<20} {'BOOK':<28} {'DUE DATE':<12} {'STATUS':<10} {'FINE'}")
    print("-" * 96)
    for r in rows:
        st_color = GREEN if r['status'] == 'returned' else (YELLOW if r['status'] == 'issued' else MAGENTA)
        fine_str = f"Rs.{r['fine_amount']:.1f}" if r['fine_amount'] > 0 else "-"
        print(f"{r['id']:<5} {CYAN}{r['roll_number']:<14}{RESET} {r['name'][:18]:<20} {r['title'][:26]:<28} {r['due_date']:<12} {st_color}{r['status']:<10}{RESET} {fine_str}")
    print("-" * 96)

def issue_book_cli():
    roll = input(f"{CYAN}Enter Student Roll Number (e.g. 23GK1A0501): {RESET}").strip().upper()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, branch FROM students WHERE roll_number = ?", (roll,))
    student = cursor.fetchone()
    if not student:
        print(f"{MAGENTA}[ERROR] Student with Roll Number '{roll}' not found.{RESET}")
        conn.close()
        return

    print(f"{GREEN}[FOUND]{RESET} Student: {student['name']} ({student['branch']})")
    try:
        book_id = int(input(f"{CYAN}Enter Book ID to Issue: {RESET}").strip())
    except ValueError:
        print(f"{MAGENTA}[ERROR] Invalid Book ID.{RESET}")
        conn.close()
        return

    cursor.execute("SELECT id, title, available_copies FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print(f"{MAGENTA}[ERROR] Book ID not found.{RESET}")
        conn.close()
        return

    if book['available_copies'] <= 0:
        print(f"{MAGENTA}[ERROR] Book '{book['title']}' is currently out of stock.{RESET}")
        conn.close()
        return

    today = datetime.now().date()
    due = today + timedelta(days=14)

    cursor.execute("""
        INSERT INTO issues (book_id, student_id, issue_date, due_date, status, fine_amount, fine_paid, remarks)
        VALUES (?, ?, ?, ?, 'issued', 0.0, 0, 'Issued via CLI')
    """, (book['id'], student['id'], today.isoformat(), due.isoformat()))
    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?", (book['id'],))
    conn.commit()
    conn.close()

    print(f"\n{GREEN}[SUCCESS] Book '{book['title']}' issued to {student['name']}! Due date: {due.isoformat()}{RESET}")

def return_book_cli():
    try:
        issue_id = int(input(f"{CYAN}Enter Loan / Issue ID to Return: {RESET}").strip())
    except ValueError:
        print(f"{MAGENTA}[ERROR] Invalid Issue ID.{RESET}")
        return

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, status FROM issues WHERE id = ?", (issue_id,))
    issue = cursor.fetchone()
    if not issue:
        print(f"{MAGENTA}[ERROR] Loan ID #{issue_id} not found.{RESET}")
        conn.close()
        return

    if issue['status'] == 'returned':
        print(f"{YELLOW}[NOTICE] Book already returned.{RESET}")
        conn.close()
        return

    today_str = datetime.now().date().isoformat()
    cursor.execute("UPDATE issues SET status = 'returned', return_date = ? WHERE id = ?", (today_str, issue_id))
    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (issue['book_id'],))
    conn.commit()
    conn.close()

    print(f"\n{GREEN}[SUCCESS] Loan #{issue_id} returned successfully! Inventory replenished.{RESET}")

def main_menu():
    init_db()
    update_overdue_statuses()
    while True:
        print_banner()
        print(" [1] View 31 Students Roster")
        print(" [2] View Book Catalog")
        print(" [3] View Circulation Transactions (Active & Overdue)")
        print(" [4] Issue a Book")
        print(" [5] Return a Book")
        print(" [6] Launch Web GUI Server (Flask)")
        print(" [0] Exit")
        print("-" * 65)
        choice = input(f"{YELLOW}Select an option [0-6]: {RESET}").strip()

        if choice == '1':
            list_students()
            input("\nPress Enter to continue...")
        elif choice == '2':
            list_books()
            input("\nPress Enter to continue...")
        elif choice == '3':
            list_issues()
            input("\nPress Enter to continue...")
        elif choice == '4':
            issue_book_cli()
            input("\nPress Enter to continue...")
        elif choice == '5':
            return_book_cli()
            input("\nPress Enter to continue...")
        elif choice == '6':
            print(f"\n{CYAN}Starting Mayura Web Application at http://127.0.0.1:5000...{RESET}")
            import subprocess
            subprocess.run([sys.executable, "app.py"])
            break
        elif choice == '0':
            print(f"\n{GREEN}Thank you for using Mayura Library Management System!{RESET}\n")
            break
        else:
            print(f"{MAGENTA}Invalid option. Please try again.{RESET}")

if __name__ == '__main__':
    main_menu()
