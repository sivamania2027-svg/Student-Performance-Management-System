import numpy as np
import pandas as pd
import os
FILE = "students.csv"
SUBJECTS = ["Python", "Maths", "Computer Networks"]
def calculate_performance():
    if not os.path.exists(FILE):
        print("Error: Student database not found!")
        return
    df = pd.read_csv(FILE, dtype={"Student_ID": str})
    if df.empty:
        print("No student records available!")
        return
    print("\n===== STUDENT PERFORMANCE =====")
    student_id = input("Enter Student ID: ").strip()
    # Pandas filtering replaces manual search loops
    result = df.loc[df["Student_ID"] == student_id]
    if result.empty:
        print("Student not found!")
        return
    student = result.iloc[0]
    # NumPy array for subject marks
    try:
        marks = student[SUBJECTS].to_numpy(dtype=float)
    except (ValueError, TypeError):
        print("Error: Invalid marks found in database!")
        return
    # NumPy validation
    if not np.all(np.isfinite(marks) & (marks >= 0) & (marks <= 100)):
        print("Error: Invalid marks found in database!")
        return
    # NumPy calculations
    total = np.sum(marks)
    average = np.mean(marks)
    percentage = np.mean(marks)
    # np.select replaces the if-elif grade conditions
    grade = np.select(
        [
            average >= 90,
            average >= 75,
            average >= 60,
            average >= 50
        ],
        ["A", "B", "C", "D"],
        default="F"
    )
    # NumPy checks all subject marks
    status = np.where(np.all(marks >= 35), "PASS", "FAIL")
    # Pandas replaces the for loop used to display subject marks
    marks_report = pd.DataFrame({
        "Subject": SUBJECTS,
        "Mark": marks
    })
    marks_report["Mark"] = marks_report["Mark"].map(
        lambda mark: f"{mark:g}"
    )
    print("\n----- Performance Report -----")
    print("Student ID :", student["Student_ID"])
    print("Name       :", student["Name"])
    print(marks_report.to_string(index=False, header=False))
    print("------------------------------")
    print(f"Total      : {total:g} / 300")
    print(f"Average    : {average:.2f}")
    print(f"Percentage : {percentage:.2f}%")
    print("Grade      :", grade)
    print("Status     :", status)
    print("------------------------------")
if __name__ == "__main__":
    calculate_performan
