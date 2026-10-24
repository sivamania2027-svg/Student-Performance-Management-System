
import numpy as np
from database import load_data

SUBJECTS = ["Python", "Maths", "Computer_Networks"]

def show_report():
    df = load_data()

    if df.empty:
        print("No student records available.")
        return

    marks = df[SUBJECTS].to_numpy(dtype=float)
    averages = np.mean(marks, axis=1)
    passed = np.all(marks >= 35, axis=1)

    print("\n===== CLASS PERFORMANCE REPORT =====")
    print("Total Students:", len(df))
    print("Class Average:", round(np.mean(averages), 2))
    print("Highest Average:", round(np.max(averages), 2))
    print("Lowest Average:", round(np.min(averages), 2))
    print("Students Passed:", int(np.sum(passed)))
    print("Students Failed:", int(np.sum(~passed)))

    topper_index = int(np.argmax(averages))
    print("\n--- CLASS TOPPER ---")
    print("Student ID:", df.iloc[topper_index]["Student_ID"])
    print("Name:", df.iloc[topper_index]["Name"])
    print("Average:", round(averages[topper_index], 2))

    print("\n--- SUBJECT AVERAGES ---")
    for i, subject in enumerate(SUBJECTS):
        print(subject, ":", round(np.mean(marks[:, i]), 2))

    print("\n--- STUDENT RANKING ---")
    ranking = df[["Student_ID", "Name"]].copy()
    ranking["Average"] = np.round(averages, 2)
    ranking = ranking.sort_values(
        "Average", ascending=False
    ).reset_index(drop=True)
    ranking.index += 1
    print(ranking.to_string())
