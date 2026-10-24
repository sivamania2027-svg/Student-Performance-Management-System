import numpy as np
import pandas as pd
import os


FILE = "students.csv"
SUBJECTS = ["Python", "Maths", "Computer Networks"]




def show_report():
    if not os.path.exists(FILE):
        print("Error: Student database not found!")
        return


    df = pd.read_csv(FILE, dtype={"Student_ID": str})


    if df.empty:
        print("No student records available!")
        return


    # Convert marks into numeric values safely
    df[SUBJECTS] = df[SUBJECTS].apply(pd.to_numeric, errors="coerce")
    marks = df[SUBJECTS].to_numpy(dtype=float)


    # Validate all marks using NumPy
    if not np.all(np.isfinite(marks) & (marks >= 0) & (marks <= 100)):
        print("Error: Invalid marks found in database!")
        return


    # Pandas vectorized calculations: no manual loops
    df["Total"] = df[SUBJECTS].sum(axis=1)
    df["Average"] = df[SUBJECTS].mean(axis=1).round(2)
    df["Percentage"] = (df["Total"] / (len(SUBJECTS) * 100) * 100).round(2)


    # NumPy assigns grades to all students at once
    df["Grade"] = np.select(
        [
            df["Average"] >= 90,
            df["Average"] >= 75,
            df["Average"] >= 60,
            df["Average"] >= 50
        ],
        ["A", "B", "C", "D"],
        default="F"
    )


    # NumPy checks pass/fail for every student
    passed = df[SUBJECTS].ge(35).all(axis=1)
    df["Status"] = np.where(passed, "PASS", "FAIL")


    # Display report using Pandas
    report_columns = [
        "Student_ID", "Name", "Total", "Average",
        "Percentage", "Grade", "Status"
    ]


    print("\n========== CLASS PERFORMANCE REPORT ==========")
    print(df[report_columns].to_string(index=False))


    # Pandas class statistics
    print("\n============= CLASS STATISTICS =============")
    print("Total Students :", len(df))
    print("Class Average  :", round(df["Average"].mean(), 2))
    print("Highest Average:", df["Average"].max())
    print("Lowest Average :", df["Average"].min())
    print("Students Passed:", int(passed.sum()))
    print("Students Failed:", int((~passed).sum()))


    # Pandas finds the topper
    topper = df.loc[df["Average"].idxmax()]


    print("\n=============== CLASS TOPPER ===============")
    print("Student ID :", topper["Student_ID"])
    print("Name       :", topper["Name"])
    print("Average    :", topper["Average"])
    print("Grade      :", topper["Grade"])
    print("============================================")




if __name__ == "__main__":
    show_report()