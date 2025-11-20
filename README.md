# ???? Student Attendance Manager (Python CLI Project)

This is a **menu-driven, problem-solving-based attendance management system** written in Python.

It allows a teacher/user to:
- Add students
- View all students
Take attendance - P/A for any date
- Automatically save the attendance records
- Calculate attendance percentage

- Check exam eligibility: ≥ 75%


- View the detailed attendance history of any student

This project uses JSON files for data storage so that all information remains saved after the program closes.
Features

1. Add Students

User can input student names, and each student will get a unique ID number.
Saved in `students.json`.

2. View Students
Displays the full list of students with IDs.
3. Remove Student
Remove by ID.
Attendance data of that student gets cleaned automatically.

4. Take Attendance

- Enter date. Default: today

- All the students list is shown.
- Mark **P** (Present) or **A** (Absent)
- Press Enter = default **P**
- Saved in `attendance.json`

5. Eligibility Report
Calculates attendance % using:
`percentage = (present_classes / total_classes) × 100`
Shows:


- Present count

- Total classes

- Percentage
- Eligible / Not Eligible (≥ 75%)
6. Attendance History
See the complete history of any student:
- Daily P/A record
- Total present  ***-
