

import json
import os
from datetime import datetime

STUDENTS_FILE = "students.json"
ATTENDANCE_FILE = "attendance.json"
ELIGIBILITY_THRESHOLD = 75.0  # percentage


# Utilities for file I/O 
def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Data helpers 
def ensure_data_files():
    # students: list of dicts { "id": int, "name": str }
    students = load_json(STUDENTS_FILE, [])
    attendance = load_json(ATTENDANCE_FILE, {})  # date -> { student_id: "P"/"A" }
    save_json(STUDENTS_FILE, students)
    save_json(ATTENDANCE_FILE, attendance)
    return students, attendance


def next_student_id(students):
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


#Student management
def add_student():
    students = load_json(STUDENTS_FILE, [])
    name = input("Enter student name: ").strip()
    if not name:
        print("Name can't be empty.")
        return
    sid = next_student_id(students)
    students.append({"id": sid, "name": name})
    save_json(STUDENTS_FILE, students)
    print(f"Added: [{sid}] {name}")


def view_students():
    students = load_json(STUDENTS_FILE, [])
    if not students:
        print("No students found. Please add students first.")
        return
    print("\n--- Students List ---")
    for s in students:
        print(f"[{s['id']}] {s['name']}")
    print("---------------------\n")


def remove_student():
    students = load_json(STUDENTS_FILE, [])
    view_students()
    try:
        sid = int(input("Enter student ID to remove (or 0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        return
    if sid == 0:
        return
    new_students = [s for s in students if s["id"] != sid]
    if len(new_students) == len(students):
        print("Student ID not found.")
    else:
        save_json(STUDENTS_FILE, new_students)
        # Also remove this student from attendance records
        attendance = load_json(ATTENDANCE_FILE, {})
        for date in attendance:
            if str(sid) in attendance[date]:
                attention = attendance[date].pop(str(sid))
        save_json(ATTENDANCE_FILE, attendance)
        print(f"Removed student ID {sid}.")


# Attendance 
def take_attendance():
    students = load_json(STUDENTS_FILE, [])
    if not students:
        print("No students to take attendance for. Add students first.")
        return

    date_input = input("Enter date for attendance (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_input:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date_str = date_input
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    attendance = load_json(ATTENDANCE_FILE, {})

    if date_str in attendance:
        overwrite = input(f"Attendance for {date_str} already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("Cancelled taking attendance.")
            return

    print(f"\nTaking attendance for {date_str}. Mark P for present, A for absent.")
    print("Press Enter to mark default 'P' (present).\n")

    day_record = {}
    for s in students:
        while True:
            entry = input(f"[{s['id']}] {s['name']} (P/A): ").strip().upper()
            if entry == "":
                entry = "P"  # default present
            if entry in ("P", "A"):
                day_record[str(s["id"])] = entry
                break
            else:
                print("Please enter 'P' or 'A' (or press Enter for P).")

    attendance[date_str] = day_record
    save_json(ATTENDANCE_FILE, attendance)
    print(f"\nSaved attendance for {date_str}. {len(day_record)} records.\n")


# Reports 
def calculate_attendance_percentages():
    students = load_json(STUDENTS_FILE, [])
    attendance = load_json(ATTENDANCE_FILE, {})

    dates = sorted(attendance.keys())
    total_classes = len(dates)
    # initialize counts
    counts = {str(s["id"]): 0 for s in students}
    for d in dates:
        for sid_str, val in attendance[d].items():
            if val == "P":
                if sid_str in counts:
                    counts[sid_str] += 1

    results = []
    for s in students:
        sid_str = str(s["id"])
        present = counts.get(sid_str, 0)
        percent = (present / total_classes * 100) if total_classes > 0 else 0.0
        results.append({
            "id": s["id"],
            "name": s["name"],
            "present": present,
            "total_classes": total_classes,
            "percent": percent
        })
    return results


def view_eligibility():
    results = calculate_attendance_percentages()
    if not results:
        print("No students or attendance data found.")
        return
    print("\n--- Eligibility Report ---")
    for r in results:
        status = "Eligible ✅" if r["percent"] >= ELIGIBILITY_THRESHOLD else "Not Eligible ❌"
        print(f"[{r['id']}] {r['name']}: {r['present']}/{r['total_classes']} = {r['percent']:.2f}% -> {status}")
    print("--------------------------\n")


def view_student_history():
    students = load_json(STUDENTS_FILE, [])
    attendance = load_json(ATTENDANCE_FILE, {})
    view_students()
    try:
        sid = int(input("Enter student ID to view history (or 0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        return
    if sid == 0:
        return
    sid_str = str(sid)
    dates = sorted(attendance.keys())
    if not dates:
        print("No attendance data yet.")
        return
    print(f"\nAttendance history for student ID {sid}\n")
    total_present = 0
    for d in dates:
        mark = attendance[d].get(sid_str, "-")
        print(f"{d}: {mark}")
        if mark == "P":
            total_present += 1
    percent = (total_present / len(dates) * 100) if dates else 0
    print(f"\nTotal: {total_present}/{len(dates)} = {percent:.2f}%\n")


# ---------- Main menu ----------
def main_menu():
    ensure_data_files()
    while True:
        print("====== Student Attendance Manager ======")
        print("1. Add student")
        print("2. View students")
        print("3. Remove student")
        print("4. Take attendance")
        print("5. View eligibility report")
        print("6. View a student's attendance history")
        print("0. Exit")
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Enter a number from menu.")
            continue

        if choice == 1:
            add_student()
        elif choice == 2:
            view_students()
        elif choice == 3:
            remove_student()
        elif choice == 4:
            take_attendance()
        elif choice == 5:
            view_eligibility()
        elif choice == 6:
            view_student_history()
        elif choice == 0:
            print("Exiting. Bye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
