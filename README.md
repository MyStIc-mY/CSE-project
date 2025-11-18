# 🏫 Student Attendance Manager (Python CLI Project)

This is a **menu-driven, problem-solving based attendance management system** written in Python.  
It allows a teacher/user to:

- Add students  
- View all students  
- Take attendance (P/A) for any date  
- Automatically save attendance records  
- Calculate attendance percentage  
- Check exam eligibility (≥ 75%)  
- View detailed attendance history of any student  

This project uses **JSON files** for data storage so all information remains saved even after the program is closed.


## 🚀 Features

### ✔ 1. Add Students  
User can enter student names, and each student gets a unique ID.  
Saved in `students.json`.

### ✔ 2. View Students  
Displays full list of students with IDs.

### ✔ 3. Remove Student  
Remove by ID.  
Attendance data of that student gets cleaned automatically.

### ✔ 4. Take Attendance  
- Enter date (default: today)  
- All students list is shown  
- Mark **P** (Present) or **A** (Absent)  
- Press Enter = default **P**  
- Saved in `attendance.json`

### ✔ 5. Eligibility Report  
Calculates attendance % using:

`percentage = (present_classes / total_classes) × 100`

Shows:  
- Present count  
- Total classes  
- Percentage  
- Eligible / Not Eligible (≥ 75%)

### ✔ 6. Attendance History  
See complete history of any student:
- Daily P/A record  
- Total present  
- Overall %  


## 💡 Why This Is a Strong Problem-Solving Project?

It demonstrates:

- Input handling  
- Data validation  
- Looping  
- Decision-making  
- File storage  
- Functions & modular code  
- Real-life use case  



## 🛠️ Installation & Setup

### 1️⃣ Install Python  
Download from: https://www.python.org/downloads/

### 2️⃣ Project Files