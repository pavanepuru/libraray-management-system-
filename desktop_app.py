"""
MAYURA - VIBRANT PEACOCK LIBRARY MANAGEMENT SYSTEM (DESKTOP GUI)
Standalone Offline Desktop Application built with Python Tkinter & SQLite.
No web server or browser required.
Includes all 31 4th B.Tech CSE students from department sheet.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import csv
from datetime import datetime, timedelta
from database import DB_PATH, init_db, update_overdue_statuses, get_db

# ==========================================
# Vibrant Peacock Palette Constants
# ==========================================
COLOR_BG_DARK       = "#04141f"   # Deep twilight teal
COLOR_SURFACE       = "#082032"   # Panel & card surface
COLOR_SURFACE_LIGHT = "#0c2b42"   # Hover & selected surface
COLOR_CYAN          = "#00f5d4"   # Brilliant peacock eye turquoise
COLOR_TEAL          = "#00b4d8"   # Peacock blue
COLOR_ROYAL         = "#0077b6"   # Royal peacock blue
COLOR_EMERALD       = "#02c39a"   # Lush plumage green
COLOR_GOLD          = "#ffd166"   # Plumage amber gold
COLOR_CRIMSON       = "#ef476f"   # Overdue alert coral/red
COLOR_TEXT_MAIN     = "#f0fdfa"   # Crisp white-teal text
COLOR_TEXT_MUTED    = "#94d2bd"   # Soft mint muted text
COLOR_BORDER        = "#00a896"   # Frame border

class PeacockLMSDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Mayura - Peacock Library Management System (CSE 4th B.Tech)")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)
        self.root.configure(bg=COLOR_BG_DARK)

        # Initialize SQLite database with 31 students
        init_db(force_reseed=False)
        update_overdue_statuses()

        self.setup_styles()
        self.create_header()
        self.create_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Notebook Tabs
        style.configure("Peacock.TNotebook", background=COLOR_BG_DARK, borderwidth=0)
        style.configure("Peacock.TNotebook.Tab",
                        background=COLOR_SURFACE,
                        foreground=COLOR_TEXT_MUTED,
                        padding=[18, 9],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Peacock.TNotebook.Tab",
                  background=[("selected", COLOR_ROYAL)],
                  foreground=[("selected", COLOR_CYAN)])

        # Treeview (Tables)
        style.configure("Peacock.Treeview",
                        background=COLOR_SURFACE,
                        foreground=COLOR_TEXT_MAIN,
                        fieldbackground=COLOR_SURFACE,
                        rowheight=28,
                        font=("Segoe UI", 9),
                        borderwidth=0)
        style.configure("Peacock.Treeview.Heading",
                        background="#021a2d",
                        foreground=COLOR_CYAN,
                        font=("Segoe UI", 9, "bold"),
                        relief="flat")
        style.map("Peacock.Treeview",
                  background=[("selected", COLOR_SURFACE_LIGHT)],
                  foreground=[("selected", COLOR_CYAN)])

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#021422", height=70, padx=20, pady=10)
        header_frame.pack(fill="x", side="top")

        # Title & Subtitle
        title_box = tk.Frame(header_frame, bg="#021422")
        title_box.pack(side="left")

        title_lbl = tk.Label(title_box, text="🦚 MAYURA LIBRARY MANAGEMENT SYSTEM",
                             font=("Segoe UI", 16, "bold"), bg="#021422", fg=COLOR_CYAN)
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(title_box, text="CSE DEPARTMENT ARCHIVE • 4TH B.TECH COHORT (31 STUDENTS ENROLLED)",
                           font=("Segoe UI", 8, "bold"), bg="#021422", fg=COLOR_GOLD)
        sub_lbl.pack(anchor="w")

        # Quick Actions on Right
        actions_box = tk.Frame(header_frame, bg="#021422")
        actions_box.pack(side="right")

        refresh_btn = tk.Button(actions_box, text="🔄 Refresh All", font=("Segoe UI", 9, "bold"),
                                bg=COLOR_SURFACE_LIGHT, fg=COLOR_CYAN, activebackground=COLOR_ROYAL,
                                activeforeground="#ffffff", relief="flat", padx=12, pady=5, cursor="hand2",
                                command=self.refresh_all_tabs)
        refresh_btn.pack(side="right", padx=5)

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root, style="Peacock.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=15, pady=12)

        # Tab Frames
        self.tab_dashboard = tk.Frame(self.notebook, bg=COLOR_BG_DARK)
        self.tab_students  = tk.Frame(self.notebook, bg=COLOR_BG_DARK)
        self.tab_books     = tk.Frame(self.notebook, bg=COLOR_BG_DARK)
        self.tab_issues    = tk.Frame(self.notebook, bg=COLOR_BG_DARK)
        self.tab_reports   = tk.Frame(self.notebook, bg=COLOR_BG_DARK)

        self.notebook.add(self.tab_dashboard, text="  📊 Overview Dashboard  ")
        self.notebook.add(self.tab_students,  text="  🎓 Students Roster (31)  ")
        self.notebook.add(self.tab_books,     text="  📚 Book Catalog  ")
        self.notebook.add(self.tab_issues,    text="  🔄 Issue & Return Desk  ")
        self.notebook.add(self.tab_reports,   text="  📄 Reports & Exports  ")

        # Build Tab Content
        self.build_dashboard_tab()
        self.build_students_tab()
        self.build_books_tab()
        self.build_issues_tab()
        self.build_reports_tab()

    # ==========================================
    # TAB 1: DASHBOARD
    # ==========================================
    def build_dashboard_tab(self):
        for w in self.tab_dashboard.winfo_children():
            w.destroy()

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(total_copies), SUM(available_copies) FROM books")
        b_res = c.fetchone()
        tot_books = b_res[0] or 0
        tot_copies = b_res[1] or 0
        avail_copies = b_res[2] or 0

        c.execute("SELECT COUNT(*) FROM students")
        tot_students = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM issues WHERE status = 'issued'")
        active_loans = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM issues WHERE status = 'overdue'")
        overdue_loans = c.fetchone()[0] or 0

        c.execute("SELECT SUM(fine_amount) FROM issues WHERE status = 'overdue' OR (fine_amount > 0 AND fine_paid = 0)")
        pending_fines = c.fetchone()[0] or 0.0

        conn.close()

        # Banner Card
        banner = tk.Frame(self.tab_dashboard, bg=COLOR_SURFACE, padx=20, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 15))

        b_title = tk.Label(banner, text="Welcome to Mayura Desktop Edition", font=("Segoe UI", 14, "bold"), bg=COLOR_SURFACE, fg="#ffffff")
        b_title.pack(anchor="w")
        b_desc = tk.Label(banner, text="Complete offline library management engineered with rich Peacock aesthetics. All 31 CSE department students pre-loaded.",
                          font=("Segoe UI", 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED)
        b_desc.pack(anchor="w", pady=(3, 0))

        # KPI Metrics Row
        kpi_frame = tk.Frame(self.tab_dashboard, bg=COLOR_BG_DARK)
        kpi_frame.pack(fill="x", pady=(0, 15))
        kpi_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="kpi")

        metrics = [
            ("TOTAL TITLES", f"{tot_books} ({tot_copies} copies)", COLOR_TEAL, "📚"),
            ("AVAILABLE STOCK", f"{avail_copies} on shelves", COLOR_EMERALD, "✅"),
            ("ACTIVE LOANS", f"{active_loans} with students", COLOR_CYAN, "🔄"),
            ("OVERDUE LOANS", f"{overdue_loans} alert", COLOR_CRIMSON, "⚠️"),
            ("ENROLLED COHORT", f"{tot_students} CSE Students", COLOR_GOLD, "🎓")
        ]

        for i, (label, val, accent, icon) in enumerate(metrics):
            card = tk.Frame(kpi_frame, bg=COLOR_SURFACE, padx=14, pady=12, highlightthickness=1, highlightbackground=accent)
            card.grid(row=0, column=i, padx=5, sticky="nsew")

            tk.Label(card, text=f"{icon} {label}", font=("Segoe UI", 8, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            tk.Label(card, text=val, font=("Segoe UI", 13, "bold"), bg=COLOR_SURFACE, fg=accent).pack(anchor="w", pady=(5, 0))

        # Recent Transactions Section
        recent_lbl = tk.Label(self.tab_dashboard, text="Recent Circulation Transactions", font=("Segoe UI", 11, "bold"), bg=COLOR_BG_DARK, fg=COLOR_CYAN)
        recent_lbl.pack(anchor="w", pady=(5, 5))

        table_frame = tk.Frame(self.tab_dashboard, bg=COLOR_SURFACE)
        table_frame.pack(fill="both", expand=True)

        cols = ("id", "roll", "student", "book", "issue_date", "due_date", "status", "fine")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Peacock.Treeview")
        tree.heading("id", text="Loan ID")
        tree.heading("roll", text="Roll Number")
        tree.heading("student", text="Student Name")
        tree.heading("book", text="Book Title")
        tree.heading("issue_date", text="Issue Date")
        tree.heading("due_date", text="Due Date")
        tree.heading("status", text="Status")
        tree.heading("fine", text="Fine")

        tree.column("id", width=70, anchor="center")
        tree.column("roll", width=120, anchor="center")
        tree.column("student", width=170, anchor="w")
        tree.column("book", width=260, anchor="w")
        tree.column("issue_date", width=100, anchor="center")
        tree.column("due_date", width=100, anchor="center")
        tree.column("status", width=100, anchor="center")
        tree.column("fine", width=80, anchor="center")

        tree.pack(fill="both", expand=True)

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT i.id, s.roll_number, s.name, b.title, i.issue_date, i.due_date, i.status, i.fine_amount
            FROM issues i
            JOIN students s ON i.student_id = s.id
            JOIN books b ON i.book_id = b.id
            ORDER BY i.id DESC LIMIT 10
        """)
        for r in c.fetchall():
            fine_str = f"₹{r['fine_amount']:.1f}" if r['fine_amount'] > 0 else "-"
            tree.insert("", "end", values=(f"#LN-{r['id']}", r['roll_number'], r['name'], r['title'], r['issue_date'], r['due_date'], r['status'].upper(), fine_str))
        conn.close()

    # ==========================================
    # TAB 2: STUDENTS ROSTER (31 STUDENTS)
    # ==========================================
    def build_students_tab(self):
        for w in self.tab_students.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.tab_students, bg=COLOR_BG_DARK, pady=8)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="Search Student:", font=("Segoe UI", 9, "bold"), bg=COLOR_BG_DARK, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 6))
        self.student_search_var = tk.StringVar()
        s_entry = tk.Entry(top_bar, textvariable=self.student_search_var, bg=COLOR_SURFACE, fg=COLOR_CYAN,
                           insertbackground=COLOR_CYAN, font=("Segoe UI", 10), width=30, relief="flat",
                           highlightthickness=1, highlightbackground=COLOR_BORDER)
        s_entry.pack(side="left", padx=5)
        s_entry.bind("<KeyRelease>", lambda e: self.load_students_table())

        card_btn = tk.Button(top_bar, text="🦚 Generate Digital Library Pass", font=("Segoe UI", 9, "bold"),
                             bg=COLOR_GOLD, fg="#001220", activebackground="#ffb703", relief="flat", padx=12, pady=4,
                             cursor="hand2", command=self.open_selected_student_card)
        card_btn.pack(side="right", padx=5)

        add_btn = tk.Button(top_bar, text="➕ Add Student", font=("Segoe UI", 9, "bold"),
                            bg=COLOR_ROYAL, fg="#ffffff", activebackground=COLOR_TEAL, relief="flat", padx=12, pady=4,
                            cursor="hand2", command=self.open_add_student_dialog)
        add_btn.pack(side="right", padx=5)

        # Table
        table_frame = tk.Frame(self.tab_students, bg=COLOR_SURFACE)
        table_frame.pack(fill="both", expand=True, pady=8)

        cols = ("sl", "roll", "name", "year", "branch", "email", "phone", "active_loans")
        self.students_tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Peacock.Treeview")
        self.students_tree.heading("sl", text="Sl.No")
        self.students_tree.heading("roll", text="Roll Number")
        self.students_tree.heading("name", text="Student Name")
        self.students_tree.heading("year", text="Year of Study")
        self.students_tree.heading("branch", text="Branch")
        self.students_tree.heading("email", text="Email ID")
        self.students_tree.heading("phone", text="Phone Number")
        self.students_tree.heading("active_loans", text="Active Loans")

        self.students_tree.column("sl", width=50, anchor="center")
        self.students_tree.column("roll", width=120, anchor="center")
        self.students_tree.column("name", width=180, anchor="w")
        self.students_tree.column("year", width=110, anchor="center")
        self.students_tree.column("branch", width=130, anchor="center")
        self.students_tree.column("email", width=180, anchor="w")
        self.students_tree.column("phone", width=120, anchor="center")
        self.students_tree.column("active_loans", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.students_tree.pack(side="left", fill="both", expand=True)

        self.load_students_table()

    def load_students_table(self):
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)

        q = self.student_search_var.get().strip().lower()
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT s.id, s.sl_no, s.roll_number, s.name, s.year_of_study, s.branch, s.email, s.phone,
                   (SELECT COUNT(*) FROM issues i WHERE i.student_id = s.id AND i.status IN ('issued', 'overdue')) as loan_count
            FROM students s
            ORDER BY s.roll_number ASC
        """)
        for r in c.fetchall():
            if not q or q in r['roll_number'].lower() or q in r['name'].lower() or q in r['branch'].lower():
                loan_txt = f"{r['loan_count']} Active" if r['loan_count'] > 0 else "0"
                self.students_tree.insert("", "end", iid=str(r['id']), values=(
                    r['sl_no'], r['roll_number'], r['name'], r['year_of_study'], r['branch'], r['email'], r['phone'], loan_txt
                ))
        conn.close()

    def open_selected_student_card(self):
        sel = self.students_tree.selection()
        if not sel:
            messagebox.showwarning("Select Student", "Please click on a student in the table first.")
            return

        student_id = int(sel[0])
        self.show_digital_library_card(student_id)

    def show_digital_library_card(self, student_id):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = c.fetchone()

        c.execute("""
            SELECT b.title, i.due_date, i.status
            FROM issues i
            JOIN books b ON i.book_id = b.id
            WHERE i.student_id = ? AND i.status IN ('issued', 'overdue')
        """, (student_id,))
        loans = c.fetchall()
        conn.close()

        if not student:
            return

        # Peacock Digital Card Window
        card_win = tk.Toplevel(self.root)
        card_win.title(f"Digital Library Pass - {student['roll_number']}")
        card_win.geometry("460x520")
        card_win.configure(bg="#021320")
        card_win.resizable(False, False)

        card_box = tk.Frame(card_win, bg="#062238", padx=20, pady=20, highlightthickness=2, highlightbackground=COLOR_CYAN)
        card_box.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        tk.Label(card_box, text="DEPARTMENT OF CSE • LIBRARY PASS", font=("Segoe UI", 10, "bold"), bg="#062238", fg=COLOR_GOLD).pack()
        tk.Label(card_box, text="🦚 OFFICIAL VERIFIED MEMBER CARD 🦚", font=("Segoe UI", 8), bg="#062238", fg=COLOR_CYAN).pack(pady=(2, 12))

        # Body row
        body = tk.Frame(card_box, bg="#062238")
        body.pack(fill="x", pady=6)

        # Avatar initial
        avatar = tk.Frame(body, bg=COLOR_ROYAL, width=70, height=85, highlightthickness=1, highlightbackground=COLOR_GOLD)
        avatar.pack_propagate(False)
        avatar.pack(side="left", padx=(0, 15))
        tk.Label(avatar, text=student['name'][0], font=("Segoe UI", 28, "bold"), bg=COLOR_ROYAL, fg=COLOR_GOLD).pack(expand=True)

        # Student Details
        info_col = tk.Frame(body, bg="#062238")
        info_col.pack(side="left", fill="x", expand=True)

        tk.Label(info_col, text="STUDENT NAME", font=("Segoe UI", 7, "bold"), bg="#062238", fg=COLOR_TEXT_MUTED).pack(anchor="w")
        tk.Label(info_col, text=student['name'], font=("Segoe UI", 11, "bold"), bg="#062238", fg="#ffffff").pack(anchor="w")

        tk.Label(info_col, text="ROLL NUMBER", font=("Segoe UI", 7, "bold"), bg="#062238", fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(4, 0))
        tk.Label(info_col, text=student['roll_number'], font=("Courier New", 11, "bold"), bg="#062238", fg=COLOR_GOLD).pack(anchor="w")

        tk.Label(info_col, text=f"{student['year_of_study']} • {student['branch']}", font=("Segoe UI", 9), bg="#062238", fg=COLOR_CYAN).pack(anchor="w", pady=(3, 0))

        # Active Loans
        loans_frame = tk.Frame(card_box, bg="#031625", padx=10, pady=8, highlightthickness=1, highlightbackground=COLOR_SURFACE_LIGHT)
        loans_frame.pack(fill="x", pady=(15, 12))
        tk.Label(loans_frame, text="CURRENTLY BORROWED BOOKS:", font=("Segoe UI", 8, "bold"), bg="#031625", fg=COLOR_TEAL).pack(anchor="w")

        if loans:
            for l in loans:
                tk.Label(loans_frame, text=f"• {l['title'][:32]} (Due: {l['due_date']})", font=("Segoe UI", 8), bg="#031625", fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=1)
        else:
            tk.Label(loans_frame, text="No active books borrowed.", font=("Segoe UI", 8, "italic"), bg="#031625", fg=COLOR_TEXT_MUTED).pack(anchor="w")

        # Barcode strip
        bc_frame = tk.Frame(card_box, bg="#ffffff", pady=5)
        bc_frame.pack(fill="x", pady=(10, 5))
        tk.Label(bc_frame, text="||| | | || ||| | ||| || ||| | |||", font=("Courier New", 14, "bold"), bg="#ffffff", fg="#000000").pack()
        tk.Label(bc_frame, text=f"*{student['roll_number']}*", font=("Courier New", 9, "bold"), bg="#ffffff", fg="#000000").pack()

    def open_add_student_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Student")
        dlg.geometry("380x360")
        dlg.configure(bg=COLOR_SURFACE)

        tk.Label(dlg, text="Enroll Student", font=("Segoe UI", 12, "bold"), bg=COLOR_SURFACE, fg=COLOR_CYAN).pack(pady=10)

        form = tk.Frame(dlg, bg=COLOR_SURFACE, padx=20)
        form.pack(fill="both", expand=True)

        fields = [("Roll Number:", "roll"), ("Student Name:", "name"), ("Year of Study:", "year"), ("Branch:", "branch")]
        entries = {}

        for lbl, key in fields:
            tk.Label(form, text=lbl, font=("Segoe UI", 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(5, 2))
            e = tk.Entry(form, bg=COLOR_BG_DARK, fg=COLOR_CYAN, insertbackground=COLOR_CYAN, font=("Segoe UI", 9))
            if key == "year":
                e.insert(0, "4TH B.TECH")
            elif key == "branch":
                e.insert(0, "CSE")
            e.pack(fill="x")
            entries[key] = e

        def save():
            roll = entries["roll"].get().strip().upper()
            name = entries["name"].get().strip().upper()
            year = entries["year"].get().strip()
            branch = entries["branch"].get().strip().upper()

            if not roll or not name:
                messagebox.showerror("Validation", "Roll Number and Name are required!")
                return

            try:
                conn = get_db()
                c = conn.cursor()
                c.execute("SELECT MAX(sl_no) FROM students")
                max_sl = c.fetchone()[0] or 0
                c.execute("""
                    INSERT INTO students (sl_no, roll_number, name, year_of_study, branch, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (max_sl + 1, roll, name, year, branch, f"{roll.lower()}@college.edu.in", "+91 9848020000"))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Student {name} enrolled successfully!")
                dlg.destroy()
                self.load_students_table()
                self.refresh_all_tabs()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        tk.Button(dlg, text="Save Student", font=("Segoe UI", 9, "bold"), bg=COLOR_CYAN, fg="#001420", relief="flat", padx=15, pady=5, command=save).pack(pady=15)

    # ==========================================
    # TAB 3: BOOK CATALOG
    # ==========================================
    def build_books_tab(self):
        for w in self.tab_books.winfo_children():
            w.destroy()

        top_bar = tk.Frame(self.tab_books, bg=COLOR_BG_DARK, pady=8)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="Search Books:", font=("Segoe UI", 9, "bold"), bg=COLOR_BG_DARK, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 6))
        self.book_search_var = tk.StringVar()
        b_entry = tk.Entry(top_bar, textvariable=self.book_search_var, bg=COLOR_SURFACE, fg=COLOR_CYAN,
                           insertbackground=COLOR_CYAN, font=("Segoe UI", 10), width=30, relief="flat",
                           highlightthickness=1, highlightbackground=COLOR_BORDER)
        b_entry.pack(side="left", padx=5)
        b_entry.bind("<KeyRelease>", lambda e: self.load_books_table())

        add_b_btn = tk.Button(top_bar, text="➕ Add Book", font=("Segoe UI", 9, "bold"),
                              bg=COLOR_CYAN, fg="#001420", activebackground="#02c39a", relief="flat", padx=12, pady=4,
                              cursor="hand2", command=self.open_add_book_dialog)
        add_b_btn.pack(side="right", padx=5)

        del_b_btn = tk.Button(top_bar, text="🗑️ Delete Book", font=("Segoe UI", 9, "bold"),
                              bg=COLOR_CRIMSON, fg="#ffffff", activebackground="#d90429", relief="flat", padx=12, pady=4,
                              cursor="hand2", command=self.delete_selected_book)
        del_b_btn.pack(side="right", padx=5)

        table_frame = tk.Frame(self.tab_books, bg=COLOR_SURFACE)
        table_frame.pack(fill="both", expand=True, pady=8)

        cols = ("id", "isbn", "title", "author", "category", "avail", "total", "shelf")
        self.books_tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Peacock.Treeview")
        self.books_tree.heading("id", text="ID")
        self.books_tree.heading("isbn", text="ISBN")
        self.books_tree.heading("title", text="Book Title")
        self.books_tree.heading("author", text="Author(s)")
        self.books_tree.heading("category", text="Category")
        self.books_tree.heading("avail", text="Available")
        self.books_tree.heading("total", text="Total Copies")
        self.books_tree.heading("shelf", text="Shelf Location")

        self.books_tree.column("id", width=40, anchor="center")
        self.books_tree.column("isbn", width=120, anchor="center")
        self.books_tree.column("title", width=250, anchor="w")
        self.books_tree.column("author", width=170, anchor="w")
        self.books_tree.column("category", width=140, anchor="center")
        self.books_tree.column("avail", width=80, anchor="center")
        self.books_tree.column("total", width=90, anchor="center")
        self.books_tree.column("shelf", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.books_tree.pack(side="left", fill="both", expand=True)

        self.load_books_table()

    def load_books_table(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        q = self.book_search_var.get().strip().lower()
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM books ORDER BY title ASC")
        for r in c.fetchall():
            if not q or q in r['title'].lower() or q in r['author'].lower() or q in r['isbn'].lower() or q in r['category'].lower():
                self.books_tree.insert("", "end", iid=str(r['id']), values=(
                    r['id'], r['isbn'], r['title'], r['author'], r['category'], r['available_copies'], r['total_copies'], r['shelf_location']
                ))
        conn.close()

    def open_add_book_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Book")
        dlg.geometry("400x420")
        dlg.configure(bg=COLOR_SURFACE)

        tk.Label(dlg, text="Add Book to Catalog", font=("Segoe UI", 12, "bold"), bg=COLOR_SURFACE, fg=COLOR_CYAN).pack(pady=10)
        form = tk.Frame(dlg, bg=COLOR_SURFACE, padx=20)
        form.pack(fill="both", expand=True)

        fields = [("Title:", "title"), ("Author:", "author"), ("Category:", "cat"), ("ISBN:", "isbn"), ("Copies:", "copies"), ("Shelf Location:", "shelf")]
        entries = {}
        for lbl, key in fields:
            tk.Label(form, text=lbl, font=("Segoe UI", 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(3, 1))
            e = tk.Entry(form, bg=COLOR_BG_DARK, fg=COLOR_CYAN, insertbackground=COLOR_CYAN, font=("Segoe UI", 9))
            if key == "copies": e.insert(0, "5")
            if key == "shelf": e.insert(0, "Shelf A-101")
            e.pack(fill="x")
            entries[key] = e

        def save():
            title = entries["title"].get().strip()
            author = entries["author"].get().strip()
            cat = entries["cat"].get().strip()
            isbn = entries["isbn"].get().strip()
            copies = int(entries["copies"].get() or 1)
            shelf = entries["shelf"].get().strip()

            if not title or not author or not isbn:
                messagebox.showerror("Error", "Title, Author, and ISBN are required.")
                return

            conn = get_db()
            c = conn.cursor()
            c.execute("""
                INSERT INTO books (isbn, title, author, category, total_copies, available_copies, shelf_location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (isbn, title, author, cat, copies, copies, shelf))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"'{title}' added to catalog!")
            dlg.destroy()
            self.load_books_table()
            self.refresh_all_tabs()

        tk.Button(dlg, text="Save Book", font=("Segoe UI", 9, "bold"), bg=COLOR_CYAN, fg="#001420", relief="flat", padx=15, pady=5, command=save).pack(pady=15)

    def delete_selected_book(self):
        sel = self.books_tree.selection()
        if not sel:
            messagebox.showwarning("Select Book", "Please select a book from the table to delete.")
            return

        book_id = int(sel[0])
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            return

        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Book removed from library.")
        self.load_books_table()
        self.refresh_all_tabs()

    # ==========================================
    # TAB 4: ISSUE & RETURN DESK
    # ==========================================
    def build_issues_tab(self):
        for w in self.tab_issues.winfo_children():
            w.destroy()

        # Top Issue Box
        issue_box = tk.Frame(self.tab_issues, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        issue_box.pack(fill="x", pady=(0, 10))

        tk.Label(issue_box, text="⚡ Quick Issue Book to Student", font=("Segoe UI", 11, "bold"), bg=COLOR_SURFACE, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 8))

        row1 = tk.Frame(issue_box, bg=COLOR_SURFACE)
        row1.pack(fill="x")

        # Student Dropdown
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, roll_number, name FROM students ORDER BY roll_number ASC")
        self.student_options = [(r['id'], f"{r['roll_number']} - {r['name']}") for r in c.fetchall()]

        c.execute("SELECT id, title, available_copies FROM books WHERE available_copies > 0 ORDER BY title ASC")
        self.book_options = [(r['id'], f"{r['title']} ({r['available_copies']} left)") for r in c.fetchall()]
        conn.close()

        tk.Label(row1, text="Student:", font=("Segoe UI", 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.sel_student_var = tk.StringVar()
        s_combo = ttk.Combobox(row1, textvariable=self.sel_student_var, values=[opt[1] for opt in self.student_options], width=32, state="readonly")
        s_combo.pack(side="left", padx=(0, 15))
        if self.student_options: s_combo.current(0)

        tk.Label(row1, text="Book:", font=("Segoe UI", 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.sel_book_var = tk.StringVar()
        b_combo = ttk.Combobox(row1, textvariable=self.sel_book_var, values=[opt[1] for opt in self.book_options], width=36, state="readonly")
        b_combo.pack(side="left", padx=(0, 15))
        if self.book_options: b_combo.current(0)

        issue_action_btn = tk.Button(row1, text="Confirm Issue", font=("Segoe UI", 9, "bold"),
                                     bg=COLOR_CYAN, fg="#001420", relief="flat", padx=14, pady=3,
                                     cursor="hand2", command=self.process_issue_action)
        issue_action_btn.pack(side="left")

        # Table Control Bar
        ctrl_bar = tk.Frame(self.tab_issues, bg=COLOR_BG_DARK, pady=6)
        ctrl_bar.pack(fill="x")

        tk.Label(ctrl_bar, text="Filter:", font=("Segoe UI", 9, "bold"), bg=COLOR_BG_DARK, fg=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 5))
        self.issue_filter_var = tk.StringVar(value="All")
        for f in ("All", "Issued", "Overdue", "Returned"):
            rb = tk.Radiobutton(ctrl_bar, text=f, variable=self.issue_filter_var, value=f,
                                bg=COLOR_BG_DARK, fg=COLOR_CYAN, selectcolor=COLOR_SURFACE,
                                activebackground=COLOR_BG_DARK, activeforeground=COLOR_GOLD,
                                command=self.load_issues_table)
            rb.pack(side="left", padx=4)

        ret_btn = tk.Button(ctrl_bar, text="📥 Return Book", font=("Segoe UI", 9, "bold"),
                            bg=COLOR_EMERALD, fg="#001420", activebackground="#00b4d8", relief="flat", padx=12, pady=3,
                            cursor="hand2", command=self.process_return_selected)
        ret_btn.pack(side="right", padx=5)

        renew_btn = tk.Button(ctrl_bar, text="🔄 Renew (14 Days)", font=("Segoe UI", 9, "bold"),
                             bg=COLOR_ROYAL, fg="#ffffff", activebackground=COLOR_TEAL, relief="flat", padx=12, pady=3,
                             cursor="hand2", command=self.process_renew_selected)
        renew_btn.pack(side="right", padx=5)

        fine_btn = tk.Button(ctrl_bar, text="💰 Clear Fine", font=("Segoe UI", 9, "bold"),
                             bg=COLOR_GOLD, fg="#001420", activebackground="#f39c12", relief="flat", padx=12, pady=3,
                             cursor="hand2", command=self.process_pay_fine_selected)
        fine_btn.pack(side="right", padx=5)

        # Issues Table
        table_frame = tk.Frame(self.tab_issues, bg=COLOR_SURFACE)
        table_frame.pack(fill="both", expand=True, pady=4)

        cols = ("id", "roll", "student", "book", "issue_d", "due_d", "return_d", "status", "fine")
        self.issues_tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Peacock.Treeview")
        self.issues_tree.heading("id", text="Loan ID")
        self.issues_tree.heading("roll", text="Roll No")
        self.issues_tree.heading("student", text="Student Name")
        self.issues_tree.heading("book", text="Book Title")
        self.issues_tree.heading("issue_d", text="Issue Date")
        self.issues_tree.heading("due_d", text="Due Date")
        self.issues_tree.heading("return_d", text="Return Date")
        self.issues_tree.heading("status", text="Status")
        self.issues_tree.heading("fine", text="Fine")

        self.issues_tree.column("id", width=65, anchor="center")
        self.issues_tree.column("roll", width=110, anchor="center")
        self.issues_tree.column("student", width=160, anchor="w")
        self.issues_tree.column("book", width=240, anchor="w")
        self.issues_tree.column("issue_d", width=95, anchor="center")
        self.issues_tree.column("due_d", width=95, anchor="center")
        self.issues_tree.column("return_d", width=95, anchor="center")
        self.issues_tree.column("status", width=90, anchor="center")
        self.issues_tree.column("fine", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.issues_tree.yview)
        self.issues_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.issues_tree.pack(side="left", fill="both", expand=True)

        self.load_issues_table()

    def load_issues_table(self):
        for item in self.issues_tree.get_children():
            self.issues_tree.delete(item)

        flt = self.issue_filter_var.get().lower()
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT i.id, s.roll_number, s.name, b.title, i.issue_date, i.due_date, i.return_date, i.status, i.fine_amount, i.fine_paid
            FROM issues i
            JOIN students s ON i.student_id = s.id
            JOIN books b ON i.book_id = b.id
            ORDER BY i.id DESC
        """)
        for r in c.fetchall():
            st = r['status'].lower()
            if flt != "all" and flt != st:
                continue

            fine_str = f"₹{r['fine_amount']:.1f}" if r['fine_amount'] > 0 else "-"
            if r['fine_paid']: fine_str += " (Paid)"

            ret_str = r['return_date'] if r['return_date'] else "—"
            self.issues_tree.insert("", "end", iid=str(r['id']), values=(
                f"#LN-{r['id']}", r['roll_number'], r['name'], r['title'], r['issue_date'], r['due_date'], ret_str, r['status'].upper(), fine_str
            ))
        conn.close()

    def process_issue_action(self):
        s_val = self.sel_student_var.get()
        b_val = self.sel_book_var.get()
        if not s_val or not b_val:
            messagebox.showwarning("Incomplete", "Please select a student and a book.")
            return

        student_id = next(opt[0] for opt in self.student_options if opt[1] == s_val)
        book_id = next(opt[0] for opt in self.book_options if opt[1] == b_val)

        today = datetime.now().date()
        due = today + timedelta(days=14)

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT available_copies, title FROM books WHERE id = ?", (book_id,))
        b_row = c.fetchone()
        if not b_row or b_row['available_copies'] <= 0:
            messagebox.showerror("Out of Stock", "Selected book has no available copies left.")
            conn.close()
            return

        c.execute("""
            INSERT INTO issues (book_id, student_id, issue_date, due_date, status, fine_amount, fine_paid, remarks)
            VALUES (?, ?, ?, ?, 'issued', 0.0, 0, 'Issued via Desktop GUI')
        """, (book_id, student_id, today.isoformat(), due.isoformat()))
        c.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Book '{b_row['title']}' issued successfully! Due on {due.isoformat()}.")
        self.refresh_all_tabs()

    def process_return_selected(self):
        sel = self.issues_tree.selection()
        if not sel:
            messagebox.showwarning("Select Loan", "Please select a loan from the table to return.")
            return

        issue_id = int(sel[0])
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT book_id, status FROM issues WHERE id = ?", (issue_id,))
        iss = c.fetchone()
        if not iss:
            conn.close()
            return

        if iss['status'] == 'returned':
            messagebox.showinfo("Already Returned", "This book was already marked as returned.")
            conn.close()
            return

        today_str = datetime.now().date().isoformat()
        c.execute("UPDATE issues SET status = 'returned', return_date = ? WHERE id = ?", (today_str, issue_id))
        c.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (iss['book_id'],))
        conn.commit()
        conn.close()

        messagebox.showinfo("Restocked", f"Loan #{issue_id} marked returned and book inventory replenished!")
        self.refresh_all_tabs()

    def process_renew_selected(self):
        sel = self.issues_tree.selection()
        if not sel:
            messagebox.showwarning("Select Loan", "Please select an active loan to renew.")
            return

        issue_id = int(sel[0])
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT due_date, status FROM issues WHERE id = ?", (issue_id,))
        iss = c.fetchone()
        if not iss or iss['status'] == 'returned':
            messagebox.showwarning("Cannot Renew", "Returned books cannot be renewed.")
            conn.close()
            return

        curr_due = datetime.strptime(iss['due_date'], "%Y-%m-%d").date()
        new_due = curr_due + timedelta(days=14)
        c.execute("UPDATE issues SET due_date = ?, status = 'issued', fine_amount = 0.0 WHERE id = ?", (new_due.isoformat(), issue_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Renewed", f"Loan #{issue_id} renewed! New due date: {new_due.isoformat()}.")
        self.refresh_all_tabs()

    def process_pay_fine_selected(self):
        sel = self.issues_tree.selection()
        if not sel:
            messagebox.showwarning("Select Loan", "Please select an issue to clear fine.")
            return

        issue_id = int(sel[0])
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE issues SET fine_paid = 1 WHERE id = ?", (issue_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Cleared", f"Fine marked as paid for loan #{issue_id}!")
        self.refresh_all_tabs()

    # ==========================================
    # TAB 5: REPORTS & CSV EXPORTS
    # ==========================================
    def build_reports_tab(self):
        for w in self.tab_reports.winfo_children():
            w.destroy()

        banner = tk.Frame(self.tab_reports, bg=COLOR_SURFACE, padx=20, pady=16, highlightthickness=1, highlightbackground=COLOR_GOLD)
        banner.pack(fill="x", pady=(0, 20))

        tk.Label(banner, text="📄 Official Library Reports & Offline Exports", font=("Segoe UI", 13, "bold"), bg=COLOR_SURFACE, fg=COLOR_GOLD).pack(anchor="w")
        tk.Label(banner, text="Export clean CSV files directly onto your computer for submission, documentation, or departmental records.",
                 font=("Segoe UI", 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(3, 0))

        export_frame = tk.Frame(self.tab_reports, bg=COLOR_BG_DARK)
        export_frame.pack(fill="x", pady=10)
        export_frame.columnconfigure((0, 1, 2), weight=1, uniform="exp")

        cards = [
            ("STUDENT ROSTER (31)", "Download the 31 CSE students roster in CSV format.", self.export_students_csv, COLOR_CYAN),
            ("BOOK INVENTORY", "Download complete catalog with stock and shelf numbers.", self.export_books_csv, COLOR_EMERALD),
            ("CIRCULATION LOGS", "Download all active, overdue, and returned loan records.", self.export_issues_csv, COLOR_GOLD)
        ]

        for i, (title, desc, cmd, color) in enumerate(cards):
            card = tk.Frame(export_frame, bg=COLOR_SURFACE, padx=16, pady=16, highlightthickness=1, highlightbackground=color)
            card.grid(row=0, column=i, padx=8, sticky="nsew")

            tk.Label(card, text=title, font=("Segoe UI", 11, "bold"), bg=COLOR_SURFACE, fg=color).pack(anchor="w")
            tk.Label(card, text=desc, font=("Segoe UI", 8), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, wraplength=260).pack(anchor="w", pady=(4, 12))

            tk.Button(card, text="Export to CSV 📥", font=("Segoe UI", 9, "bold"), bg=color, fg="#001420", relief="flat", padx=12, pady=4, cursor="hand2", command=cmd).pack(anchor="w")

        # Top Borrowed summary
        summary_frame = tk.Frame(self.tab_reports, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        summary_frame.pack(fill="both", expand=True, pady=15)

        tk.Label(summary_frame, text="🏆 Most Borrowed Titles (Department Circulation)", font=("Segoe UI", 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_CYAN).pack(anchor="w", pady=(0, 6))

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT b.title, b.category, COUNT(i.id) as cnt
            FROM books b
            LEFT JOIN issues i ON b.id = i.book_id
            GROUP BY b.id
            ORDER BY cnt DESC LIMIT 5
        """)
        for r in c.fetchall():
            tk.Label(summary_frame, text=f"• {r['title']} [{r['category']}] — Borrowed {r['cnt']} times",
                     font=("Segoe UI", 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=2)
        conn.close()

    def export_students_csv(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="cse_students_roster_31.csv")
        if not f: return
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT sl_no, roll_number, name, year_of_study, branch, email, phone FROM students ORDER BY roll_number ASC")
        rows = c.fetchall()
        conn.close()

        with open(f, "w", newline="", encoding="utf-8") as out:
            w = csv.writer(out)
            w.writerow(["Sl.No", "Roll Number", "Student Name", "Year of Study", "Branch", "Email", "Phone"])
            for r in rows:
                w.writerow([r['sl_no'], r['roll_number'], r['name'], r['year_of_study'], r['branch'], r['email'], r['phone']])
        messagebox.showinfo("Export Successful", f"Saved {len(rows)} student records to:\n{f}")

    def export_books_csv(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="library_books_inventory.csv")
        if not f: return
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT isbn, title, author, category, total_copies, available_copies, shelf_location FROM books ORDER BY title ASC")
        rows = c.fetchall()
        conn.close()

        with open(f, "w", newline="", encoding="utf-8") as out:
            w = csv.writer(out)
            w.writerow(["ISBN", "Title", "Author", "Category", "Total Copies", "Available Copies", "Shelf Location"])
            for r in rows:
                w.writerow([r['isbn'], r['title'], r['author'], r['category'], r['total_copies'], r['available_copies'], r['shelf_location']])
        messagebox.showinfo("Export Successful", f"Saved {len(rows)} book records to:\n{f}")

    def export_issues_csv(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile="library_transactions_export.csv")
        if not f: return
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT i.id, s.roll_number, s.name, b.title, b.isbn, i.issue_date, i.due_date, i.return_date, i.status, i.fine_amount
            FROM issues i
            JOIN students s ON i.student_id = s.id
            JOIN books b ON i.book_id = b.id
            ORDER BY i.id ASC
        """)
        rows = c.fetchall()
        conn.close()

        with open(f, "w", newline="", encoding="utf-8") as out:
            w = csv.writer(out)
            w.writerow(["Loan ID", "Roll Number", "Student Name", "Book Title", "ISBN", "Issue Date", "Due Date", "Return Date", "Status", "Fine Amount"])
            for r in rows:
                w.writerow([r['id'], r['roll_number'], r['name'], r['title'], r['isbn'], r['issue_date'], r['due_date'], r['return_date'] or '', r['status'], r['fine_amount']])
        messagebox.showinfo("Export Successful", f"Saved {len(rows)} loan transaction records to:\n{f}")

    def refresh_all_tabs(self):
        update_overdue_statuses()
        self.build_dashboard_tab()
        self.build_students_tab()
        self.build_books_tab()
        self.build_issues_tab()
        self.build_reports_tab()

def main():
    root = tk.Tk()
    app = PeacockLMSDesktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()
