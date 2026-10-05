"""
Mayura Library Management System - Main Flask Application
Unique Peacock Themed Library System built with Python, SQLite, and Flask.
Includes 31 pre-seeded 4th B.Tech CSE students from department sheet.
"""

import os
import csv
import io
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from database import get_db, init_db, update_overdue_statuses

app = Flask(__name__)
app.secret_key = "mayura_peacock_secret_key_lms_2026"

# Ensure DB is created on startup
with app.app_context():
    init_db(force_reseed=False)
    update_overdue_statuses()

@app.context_processor
def inject_global_data():
    """Injects students and books for global modals like quick issue anywhere in the app."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, roll_number, name, year_of_study, branch FROM students ORDER BY roll_number ASC")
        students = cursor.fetchall()

        cursor.execute("SELECT id, title, available_copies, total_copies, shelf_location FROM books ORDER BY title ASC")
        books = cursor.fetchall()
        conn.close()
        return dict(all_students_quick=students, all_books_quick=books)
    except Exception as e:
        return dict(all_students_quick=[], all_books_quick=[])

# ==========================================
# 1. Dashboard View
# ==========================================
@app.route('/')
@app.route('/dashboard')
def dashboard():
    update_overdue_statuses()
    conn = get_db()
    cursor = conn.cursor()

    # Metrics
    cursor.execute("SELECT COUNT(*), SUM(total_copies), SUM(available_copies) FROM books")
    b_stats = cursor.fetchone()
    total_books = b_stats[0] or 0
    total_copies = b_stats[1] or 0
    available_copies = b_stats[2] or 0

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'issued'")
    active_issues = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'overdue'")
    overdue_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'returned'")
    returned_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(fine_amount) FROM issues WHERE status = 'overdue' OR (fine_amount > 0 AND fine_paid = 0)")
    unpaid_fines = cursor.fetchone()[0] or 0.0

    stats = {
        'total_books': total_books,
        'total_copies': total_copies,
        'available_copies': available_copies,
        'total_students': total_students,
        'active_issues': active_issues,
        'overdue_count': overdue_count,
        'returned_count': returned_count,
        'unpaid_fines': unpaid_fines
    }

    # Category breakdown for Chart
    cursor.execute("SELECT category, COUNT(*) as cnt FROM books GROUP BY category ORDER BY cnt DESC")
    cat_rows = cursor.fetchall()
    category_labels = [r['category'] for r in cat_rows]
    category_counts = [r['cnt'] for r in cat_rows]

    # Recent Transactions
    cursor.execute("""
        SELECT i.id, i.issue_date, i.due_date, i.status, i.fine_amount, i.fine_paid,
               b.title as book_title, b.category,
               s.name as student_name, s.roll_number, s.branch
        FROM issues i
        JOIN books b ON i.book_id = b.id
        JOIN students s ON i.student_id = s.id
        ORDER BY i.id DESC
        LIMIT 8
    """)
    recent_transactions = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html',
                           active_page='dashboard',
                           stats=stats,
                           category_labels=category_labels,
                           category_counts=category_counts,
                           recent_transactions=recent_transactions)

# ==========================================
# 2. Books Catalog
# ==========================================
@app.route('/books')
def books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY title ASC")
    all_books = cursor.fetchall()

    cursor.execute("SELECT DISTINCT category FROM books ORDER BY category ASC")
    categories = [r['category'] for r in cursor.fetchall()]
    conn.close()

    return render_template('books.html', active_page='books', books=all_books, categories=categories)

@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    category = request.form.get('category', '').strip()
    isbn = request.form.get('isbn', '').strip()
    total_copies = int(request.form.get('total_copies', 1))
    shelf = request.form.get('shelf_location', 'Main Section').strip()

    if not title or not author or not isbn:
        flash("Title, Author, and ISBN are required.", "danger")
        return redirect(url_for('books'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (isbn, title, author, category, total_copies, available_copies, shelf_location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (isbn, title, author, category, total_copies, total_copies, shelf))
        conn.commit()
        conn.close()
        flash(f"Book '{title}' added successfully to catalog!", "success")
    except Exception as e:
        flash(f"Error adding book: {str(e)}", "danger")

    return redirect(url_for('books'))

@app.route('/books/edit/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    category = request.form.get('category', '').strip()
    isbn = request.form.get('isbn', '').strip()
    total_copies = int(request.form.get('total_copies', 1))
    available_copies = int(request.form.get('available_copies', 1))
    shelf = request.form.get('shelf_location', '').strip()

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, category = ?, isbn = ?, total_copies = ?, available_copies = ?, shelf_location = ?
            WHERE id = ?
        """, (title, author, category, isbn, total_copies, available_copies, shelf, book_id))
        conn.commit()
        conn.close()
        flash("Book details updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating book: {str(e)}", "danger")

    return redirect(url_for('books'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        flash("Book removed from catalog.", "success")
    except Exception as e:
        flash(f"Error deleting book: {str(e)}", "danger")

    return redirect(url_for('books'))

# ==========================================
# 3. Students Roster (Includes all 31 sheet records)
# ==========================================
@app.route('/students')
def students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*,
               (SELECT COUNT(*) FROM issues i WHERE i.student_id = s.id AND i.status IN ('issued', 'overdue')) as active_loan_count
        FROM students s
        ORDER BY s.roll_number ASC
    """)
    all_students = cursor.fetchall()
    conn.close()

    return render_template('students.html', active_page='students', students=all_students)

@app.route('/students/add', methods=['POST'])
def add_student():
    roll_number = request.form.get('roll_number', '').strip().upper()
    name = request.form.get('name', '').strip().upper()
    year_of_study = request.form.get('year_of_study', '4TH B.TECH').strip()
    branch = request.form.get('branch', 'CSE').strip().upper()
    email = request.form.get('email', '').strip().lower() or f"{roll_number.lower()}@college.edu.in"
    phone = request.form.get('phone', '').strip()

    if not roll_number or not name:
        flash("Roll Number and Name are required.", "danger")
        return redirect(url_for('students'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(sl_no) FROM students")
        max_sl = cursor.fetchone()[0] or 0
        new_sl = max_sl + 1

        cursor.execute("""
            INSERT INTO students (sl_no, roll_number, name, year_of_study, branch, email, phone, avatar_seed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_sl, roll_number, name, year_of_study, branch, email, phone, roll_number))
        conn.commit()
        conn.close()
        flash(f"Student {name} ({roll_number}) enrolled successfully!", "success")
    except Exception as e:
        flash(f"Error adding student: {str(e)}", "danger")

    return redirect(url_for('students'))

@app.route('/students/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    roll = request.form.get('roll_number', '').strip().upper()
    name = request.form.get('name', '').strip().upper()
    year = request.form.get('year_of_study', '').strip()
    branch = request.form.get('branch', '').strip().upper()
    email = request.form.get('email', '').strip().lower()
    phone = request.form.get('phone', '').strip()

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET roll_number = ?, name = ?, year_of_study = ?, branch = ?, email = ?, phone = ?
            WHERE id = ?
        """, (roll, name, year, branch, email, phone, student_id))
        conn.commit()
        conn.close()
        flash("Student profile updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating student: {str(e)}", "danger")

    return redirect(url_for('students'))

# ==========================================
# 4. Issue & Return Desk
# ==========================================
@app.route('/issues')
def issues():
    update_overdue_statuses()
    status_filter = request.args.get('status', 'all').lower()

    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT i.id, i.issue_date, i.due_date, i.return_date, i.status, i.fine_amount, i.fine_paid, i.remarks,
               b.title as book_title, b.shelf_location, b.isbn,
               s.name as student_name, s.roll_number, s.branch, s.year_of_study
        FROM issues i
        JOIN books b ON i.book_id = b.id
        JOIN students s ON i.student_id = s.id
    """
    params = []

    if status_filter == 'active':
        query += " WHERE i.status = 'issued'"
    elif status_filter == 'overdue':
        query += " WHERE i.status = 'overdue'"
    elif status_filter == 'returned':
        query += " WHERE i.status = 'returned'"

    query += " ORDER BY i.id DESC"
    cursor.execute(query, params)
    issues_list = cursor.fetchall()

    # Counts
    cursor.execute("SELECT COUNT(*) FROM issues")
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'issued'")
    active_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'overdue'")
    overdue_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'returned'")
    returned_count = cursor.fetchone()[0]

    conn.close()

    return render_template('issues.html',
                           active_page='issues',
                           issues=issues_list,
                           current_filter=status_filter,
                           total_count=total_count,
                           active_count=active_count,
                           overdue_count=overdue_count,
                           returned_count=returned_count)

@app.route('/api/issue', methods=['POST'])
def api_issue_book():
    student_id = request.form.get('student_id')
    book_id = request.form.get('book_id')
    loan_days = int(request.form.get('loan_days', 14))
    remarks = request.form.get('remarks', '').strip()

    if not student_id or not book_id:
        flash("Please select both a student and a book.", "danger")
        return redirect(request.referrer or url_for('dashboard'))

    conn = get_db()
    cursor = conn.cursor()

    # Check book availability
    cursor.execute("SELECT available_copies, title FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if not book or book['available_copies'] <= 0:
        conn.close()
        flash("Sorry, this book is currently out of stock!", "danger")
        return redirect(request.referrer or url_for('dashboard'))

    today = datetime.now().date()
    due_date = today + timedelta(days=loan_days)

    cursor.execute("""
        INSERT INTO issues (book_id, student_id, issue_date, due_date, status, fine_amount, fine_paid, remarks)
        VALUES (?, ?, ?, ?, 'issued', 0.0, 0, ?)
    """, (book_id, student_id, today.isoformat(), due_date.isoformat(), remarks))

    # Decrement available copies
    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    flash(f"Book '{book['title']}' issued successfully! Due on {due_date.isoformat()}.", "success")
    return redirect(request.referrer or url_for('issues'))

@app.route('/api/return/<int:issue_id>', methods=['POST'])
def api_return_book(issue_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id, status FROM issues WHERE id = ?", (issue_id,))
    issue = cursor.fetchone()
    if not issue:
        conn.close()
        return jsonify({'success': False, 'message': 'Loan record not found.'}), 404

    if issue['status'] == 'returned':
        conn.close()
        return jsonify({'success': False, 'message': 'Book already returned.'})

    today_str = datetime.now().date().isoformat()
    cursor.execute("""
        UPDATE issues
        SET status = 'returned', return_date = ?
        WHERE id = ?
    """, (today_str, issue_id))

    # Restock book
    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (issue['book_id'],))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Book marked returned and restocked.'})

@app.route('/api/renew/<int:issue_id>', methods=['POST'])
def api_renew_book(issue_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT due_date, status FROM issues WHERE id = ?", (issue_id,))
    issue = cursor.fetchone()
    if not issue or issue['status'] == 'returned':
        conn.close()
        return jsonify({'success': False, 'message': 'Cannot renew a returned loan.'})

    current_due = datetime.strptime(issue['due_date'], "%Y-%m-%d").date()
    new_due = current_due + timedelta(days=14)

    cursor.execute("""
        UPDATE issues
        SET due_date = ?, status = 'issued', fine_amount = 0.0
        WHERE id = ?
    """, (new_due.isoformat(), issue_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'new_due_date': new_due.isoformat()})

@app.route('/api/pay-fine/<int:issue_id>', methods=['POST'])
def api_pay_fine(issue_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE issues SET fine_paid = 1 WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Fine marked as paid.'})

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_student_profile(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    cursor.execute("""
        SELECT i.id, i.due_date, b.title as book_title
        FROM issues i
        JOIN books b ON i.book_id = b.id
        WHERE i.student_id = ? AND i.status IN ('issued', 'overdue')
    """, (student_id,))
    active_issues = cursor.fetchall()
    conn.close()

    return jsonify({
        'student': dict(student),
        'active_issues': [dict(row) for row in active_issues]
    })

# ==========================================
# 5. Reports & CSV Exports
# ==========================================
@app.route('/reports')
def reports():
    conn = get_db()
    cursor = conn.cursor()

    # Top borrowed books
    cursor.execute("""
        SELECT b.title, b.category, COUNT(i.id) as issue_count
        FROM books b
        LEFT JOIN issues i ON b.id = i.book_id
        GROUP BY b.id
        ORDER BY issue_count DESC
        LIMIT 6
    """)
    top_books = cursor.fetchall()

    # Frequent student borrowers
    cursor.execute("""
        SELECT s.roll_number, s.name, COUNT(i.id) as issue_count
        FROM students s
        LEFT JOIN issues i ON s.id = i.student_id
        GROUP BY s.id
        ORDER BY issue_count DESC
        LIMIT 6
    """)
    top_students = cursor.fetchall()
    conn.close()

    return render_template('reports.html', active_page='reports', top_books=top_books, top_students=top_students)

@app.route('/export/issues.csv')
def export_issues_csv():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, s.roll_number, s.name as student_name, b.title as book_title, b.isbn,
               i.issue_date, i.due_date, i.return_date, i.status, i.fine_amount, i.fine_paid
        FROM issues i
        JOIN students s ON i.student_id = s.id
        JOIN books b ON i.book_id = b.id
        ORDER BY i.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Loan ID', 'Student Roll No', 'Student Name', 'Book Title', 'ISBN', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Fine Amount', 'Fine Paid'])
    for r in rows:
        writer.writerow([r['id'], r['roll_number'], r['student_name'], r['book_title'], r['isbn'], r['issue_date'], r['due_date'], r['return_date'] or '', r['status'], r['fine_amount'], 'Yes' if r['fine_paid'] else 'No'])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=library_transactions_export.csv"}
    )

@app.route('/export/students.csv')
def export_students_csv():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sl_no, roll_number, name, year_of_study, branch, email, phone FROM students ORDER BY roll_number ASC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Sl.No', 'Roll Number', 'Student Name', 'Year of Study', 'Branch', 'Email', 'Phone'])
    for r in rows:
        writer.writerow([r['sl_no'], r['roll_number'], r['name'], r['year_of_study'], r['branch'], r['email'], r['phone']])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=cse_students_roster_31.csv"}
    )

@app.route('/export/books.csv')
def export_books_csv():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT isbn, title, author, category, total_copies, available_copies, shelf_location FROM books ORDER BY title ASC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ISBN', 'Title', 'Author', 'Category', 'Total Copies', 'Available Copies', 'Shelf Location'])
    for r in rows:
        writer.writerow([r['isbn'], r['title'], r['author'], r['category'], r['total_copies'], r['available_copies'], r['shelf_location']])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=library_books_inventory.csv"}
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "="*65)
    print("   MAYURA - VIBRANT PEACOCK LIBRARY MANAGEMENT SYSTEM")
    print("   CSE Department Cohort Loaded: 31 Students Active")
    print("="*65)
    print(f" * Server running on port {port}")
    print(" * Press CTRL+C to stop the server\n")
    app.run(debug=False, host='0.0.0.0', port=port)
