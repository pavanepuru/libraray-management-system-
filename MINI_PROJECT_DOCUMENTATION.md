# 🦚 MINI PROJECT REPORT
## TITLE: MAYURA - PEACOCK THEMED LIBRARY MANAGEMENT SYSTEM
**Department**: Computer Science and Engineering (CSE)  
**Target Cohort**: 4th Year B.Tech (31 Students Enrolled)  
**Technology Stack**: Python 3, Tkinter GUI, SQLite3  
**Project Classification**: Offline Academic Desktop Mini Project  

---

## 1. ABSTRACT
The **Mayura Library Management System** is a standalone, offline Python desktop application developed to automate book cataloging, circulation operations, and student borrowing records for academic institutions. Unlike conventional monochrome or web-server-dependent applications, Mayura is styled with a distinct, vibrant **Peacock Jewel-Tone Theme** (Royal Blue, Radiant Cyan, Emerald Green, and Plumage Gold). The system comes pre-configured with the official department roster of **31 4th B.Tech CSE students**, featuring automatic loan duration tracking (14 days), dynamic overdue fine calculation (₹2/day), digital student library pass generation with simulated barcodes, and 1-click CSV spreadsheet report generation.

---

## 2. SYSTEM OBJECTIVES
* **Zero Dependency on Web Servers / Browsers**: Operates 100% offline via native Python Tkinter GUI.
* **Academic Cohort Integration**: Complete roster of 31 CSE students loaded with roll numbers, contact records, and active loan counters.
* **Real-time Inventory Tracking**: Prevents over-issuing by dynamically decrementing stock upon issue and replenishing stock upon return.
* **Automated Overdue Enforcement**: Automatically checks date deltas on launch and computes late fees.
* **Digital Identity Verification**: Generates official Mayura Student Library Passes with custom barcodes for each student.

---

## 3. DATABASE DESIGN & SCHEMA

The database is built on **SQLite3** (`peacock_library.db`), structured across 3 relational tables:

```
+------------------------------------+        +------------------------------------+
|             STUDENTS               |        |               BOOKS                |
+------------------------------------+        +------------------------------------+
| id (INTEGER, PK)                   |        | id (INTEGER, PK)                   |
| sl_no (INTEGER)                    |        | isbn (TEXT, UNIQUE)                |
| roll_number (TEXT, UNIQUE)         |        | title (TEXT)                       |
| name (TEXT)                        |        | author (TEXT)                      |
| year_of_study (TEXT)               |        | category (TEXT)                    |
| branch (TEXT)                      |        | total_copies (INTEGER)             |
| email (TEXT)                       |        | available_copies (INTEGER)         |
| phone (TEXT)                       |        | shelf_location (TEXT)              |
+-----------------+------------------+        +-----------------+------------------+
                  |                                             |
                  | 1                                         1 |
                  |                                             |
                  | N                                         N |
            +-----+---------------------------------------------+-----+
            |                         ISSUES                          |
            +---------------------------------------------------------+
            | id (INTEGER, PK)                                        |
            | book_id (INTEGER, FK -> books.id)                       |
            | student_id (INTEGER, FK -> students.id)                 |
            | issue_date (DATE)                                       |
            | due_date (DATE)                                         |
            | return_date (DATE)                                      |
            | status (TEXT: 'issued', 'overdue', 'returned')          |
            | fine_amount (REAL)                                      |
            | fine_paid (INTEGER: 0 or 1)                             |
            | remarks (TEXT)                                          |
            +---------------------------------------------------------+
```

---

## 4. CLASS ROSTER DATA LOADED (31 STUDENTS)

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

## 5. HARDWARE & SOFTWARE SPECIFICATIONS

### Software Requirements
* **Operating System**: Windows 10 / 11 (or Linux / macOS)
* **Programming Language**: Python 3.8+ (Tested on Python 3.12)
* **GUI Library**: `tkinter` & `tkinter.ttk` (Standard Python Library - No external pip install required)
* **Database**: `sqlite3` (Standard Python Library)

### Hardware Requirements
* **Processor**: Intel Core i3 or equivalent (or higher)
* **RAM**: 2 GB Minimum (4 GB Recommended)
* **Disk Space**: Under 25 MB

---

## 6. HOW TO RUN (ZERO CONFIGURATION)

### Method 1: Double Click `run_desktop.bat`
Navigate to `C:\Users\acer\.gemini\antigravity\scratch\peacock-library-system` and double-click:
```bat
run_desktop.bat
```

### Method 2: Command Line
```powershell
cd C:\Users\acer\.gemini\antigravity\scratch\peacock-library-system
python main.py
```

---

## 7. VIVA VOCE QUESTIONS & MODEL ANSWERS

**Q1: Why did you choose Tkinter over a web framework?**  
*A: Tkinter provides an offline, native desktop experience that does not require starting local web servers, opening web browsers, or depending on active network ports, making it ideal for stand-alone departmental kiosks.*

**Q2: How does the system prevent issuing books that are out of stock?**  
*A: The system maintains two copy counters: `total_copies` and `available_copies`. Before issuing, it executes an atomic verification: `available_copies > 0`. If copies are exhausted, the operation is blocked and flagged.*

**Q3: How are fines calculated for late returns?**  
*A: The function `update_overdue_statuses()` calculates the date difference between `current_date` and `due_date`. If `current_date > due_date`, the difference in days is multiplied by the configured daily rate (₹2.00/day).*

**Q4: How did you implement the Peacock color theme?**  
*A: We defined a structured color system using hexadecimal constants for deep navy (`#04141f`), twilight surface (`#082032`), radiant turquoise (`#00f5d4`), plumage green (`#02c39a`), and gold (`#ffd166`), applied via custom ttk styling and widget configurations.*
