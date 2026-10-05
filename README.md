# 🦚 Mayura - Vibrant Peacock Library Management System

> **A Unique, High-Circulation Mini Project for Computer Science & Engineering (CSE)**  
> **Engineered with Python (Flask + SQLite) & Radiant Peacock Jewel-Tone Aesthetics**

---

## 🌟 1. Project Overview & The Peacock Theme

**Mayura LMS** is a unique, fully-functional mini-project designed specifically with an iridescent **Peacock Color Palette**:
* **Deep Royal Peacock Blue** (`#001e3d` / `#0077b6`) – Reflecting the majestic plumage body and core frame.
* **Vibrant Turquoise & Neon Cyan** (`#00f5d4` / `#00b4d8`) – Luminous ocelli / feather-eye glowing borders, buttons, and badges.
* **Lush Emerald Teal** (`#02c39a` / `#028090`) – In-stock indicators, successful loans, and restock confirmations.
* **Shimmering Plumage Gold** (`#ffd166` / `#f39c12`) – Student roll numbers, badges, crest accents, and fine receipts.
* **Amethyst / Deep Violet** (`#7209b7` / `#3a0ca3`) – Secondary highlights, gradient blends, and analytics bars.

---

## 📋 2. Student Data Loaded (From Department Class Sheet)

All **31 Students** from the provided 4th B.Tech CSE cohort are seeded into the database:

| Sl.No | Roll Number | Student Name | Year of Study | Branch |
|:---:|:---:|:---|:---:|:---:|
| 1 | `23GK1A0501` | A.RAJESH | 4TH B.TECH | CSE |
| 2 | `23GK1A0502` | A.PRAVEEN | 4TH B.TECH | CSE |
| 3 | `23GK1A0503` | B.NAGENDRA BABU | 4TH B.TECH | CSE |
| 4 | `23GK1A0504` | CH. ANAND KUMAR | 4TH B.TECH | CSE |
| 5 | `23GK1A0505` | D.SIRESHA | 4TH B.TECH | CSE |
| 6 | `23GK1A0506` | D.BALA ARJUN | 4TH B.TECH | CSE |
| 7 | `23GK1A0508` | G.GAYATHRI | 4TH B.TECH | CSE |
| 8 | `23GK1A0510` | J.PREETHI | 4TH B.TECH | CSE |
| 9 | `23GK1A0511` | J.VIMALA | 4TH B.TECH | CSE |
| 10 | `23GK1A0513` | K.DEEPTHI | 4TH B.TECH | CSE |
| 11 | `23GK1A0514` | K.V.SAI REDDY | 4TH B.TECH | CSE |
| 12 | `23GK1A0515` | K.DINESH | 4TH B.TECH | CSE |
| 13 | `23GK1A0516` | K.KEERTHANA | 4TH B.TECH | CSE |
| 14 | `23GK1A0517` | K.VASU DEVA RAO | 4TH B.TECH | CSE |
| 15 | `23GK1A0522` | O.PRAVEEN | 4TH B.TECH | CSE |
| 16 | `23GL1A0524` | P.MOUNIKA | 4TH B.TECH | CSE |
| 17 | `23GL1A0525` | P.AKSHAY SAI GOVARDHAN | 4TH B.TECH | CSE |
| 18 | `23GK1A0532` | S.JYOSTANA | 4TH B.TECH | CSE |
| 19 | `23GK1A0533` | S.THARUN KUMAR | 4TH B.TECH | CSE |
| 20 | `23GK1A0534` | S.SUBHASH | 4TH B.TECH | CSE |
| 21 | `23GK1A0436` | T.BHANU PRAKASH | 4TH B.TECH | CSE |
| 22 | `23GK1A0437` | T.PRANEESH | 4TH B.TECH | CSE |
| 23 | `23GK1A0438` | U.VARSHITHA | 4TH B.TECH | CSE |
| 24 | `23GK1A0439` | V.ASRITHA | 4TH B.TECH | CSE |
| 25 | `23GK1A0544` | B.CHINNARAJU | 4TH B.TECH | CSE |
| 26 | `23GK1A0548` | E.PAVAN | 4TH B.TECH | CSE |
| 27 | `23GK1A0549` | K.VYSHNAVI | 4TH B.TECH | CSE |
| 28 | `23GK1A0554` | MD.SHOIAB | 4TH B.TECH | CSE |
| 29 | `23GK1A0557` | SK.SALAR | 4TH B.TECH | CSE |
| 30 | `23GK1A0558` | J.SREE DEVI | 4TH B.TECH | CSE |
| 31 | `24GK1A0501` | N.ARJUN | 4TH B.TECH | CSE (LATERAL) |

---

## 🚀 3. Unique & Standout Features

1. **Digital Peacock Library Passes**:
   * Every student has an instant, printable **Digital ID Card** featuring their portrait initial, roll number, department seal, active borrows, and simulated Barcode (`*23GK1A0501*`).
2. **Intelligent Circulation & Overdue Tracker**:
   * Dynamic due dates with automated overdue calculation and late fee computation (₹2/day default).
   * 1-Click Return that immediately replenishes book stock.
   * 1-Click Renew that extends due date by 14 days.
3. **Interactive Visual Analytics (Chart.js)**:
   * Real-time doughnut chart of catalog categories (AI/ML, Algorithms, Systems, Web Dev, etc.).
   * Circulation status bar chart tracking available stock vs active loans.
4. **Universal Quick-Issue Modal**:
   * Accessible anywhere in the app via top navigation with student auto-preview and real-time book inventory checks.
5. **Multi-Format Reporting & Exports**:
   * Export Transactions history, Student Roster, and Book Inventory directly into `.csv` spreadsheets.
   * Dedicated Print Report view for physical library audits.
6. **Dual Interfaces**:
   * **Modern Web App** (Flask + Peacock CSS3 + JavaScript).
   * **Interactive Terminal Console** (`cli.py`) with colored ANSI output for viva presentations!

---

## 📂 4. Project Structure

```
peacock-library-system/
│
├── app.py                     # Main Flask web application & REST routes
├── database.py                # SQLite schema, student roster seed & inventory migration
├── cli.py                     # Interactive Peacock terminal console application
├── run.bat                    # 1-Click Windows launcher (starts server & opens browser)
├── peacock_library.db         # SQLite database file (auto-generated)
│
├── static/
│   ├── css/
│   │   └── peacock_theme.css  # Vibrant peacock jewel-tone design system
│   ├── js/
│   │   └── main.js            # Modals, live filtering, AJAX actions & ID pass generator
│   └── images/
│       └── peacock_logo.svg   # Custom peacock vector logo with book motif
│
├── templates/
│   ├── base.html              # Peacock navbar, alerts & shared modals
│   ├── dashboard.html         # KPI cards, Chart.js charts & recent activity
│   ├── books.html             # Catalog cards, live search, add/edit/delete
│   ├── students.html          # Full 31 students roster with digital ID pass
│   ├── issues.html            # Active loans, returns, renewals & fines desk
│   └── reports.html           # Audits, CSV exports & printable reports
│
└── README.md                  # Comprehensive documentation
```

---

## 💻 5. How to Run the Project

### Option A: 1-Click Windows Launcher (Easiest)
Simply double-click:
```
run.bat
```
This automatically launches the Flask server and opens `http://127.0.0.1:5000` in your default web browser!

---

### Option B: Run Web Application via Terminal
1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   cd C:\Users\acer\.gemini\antigravity\scratch\peacock-library-system
   ```
2. Start the Flask server:
   ```powershell
   python app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

### Option C: Run Terminal Console Edition (`cli.py`)
If your examiner asks to see command-line execution or direct console menu:
```powershell
python cli.py
```

---

## 🎓 6. Viva Voce & Presentation Guide

| Examiner Question | Ideal Response |
|:---|:---|
| **"What database is used and why?"** | *"We used SQLite3 because it is lightweight, serverless, zero-configuration, and natively integrated into Python's standard library with ACID compliance."* |
| **"How did you integrate the class sheet?"** | *"All 31 students from the 4th B.Tech CSE department sheet were structured and seeded automatically into the database via `database.py`. The system generates digital library cards for all 31 students with unique barcodes."* |
| **"How are overdue fines calculated?"** | *"When a book is issued, a due date is recorded (default 14 days). The `update_overdue_statuses()` function compares current date against the due date; if overdue, it computes `(current_date - due_date) * fine_per_day`."* |
| **"Why is the theme peacock?"** | *"The Peacock (Mayura) theme provides high visual contrast with jewel tones (royal blue, radiant cyan, emerald green, and plumage gold), giving the application an elegant, vibrant look compared to generic monotone dashboards."* |
