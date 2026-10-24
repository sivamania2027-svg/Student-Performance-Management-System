import numpy as np
import pandas as pd
from pathlib import Path


FILE = Path(__file__).resolve().parent / "students.csv"


COLUMNS = [
    "RollNo", "Name", "Department",
    "Maths", "Science", "English"
]




def read_data():
    if not FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)


    return pd.read_csv(FILE, dtype={"RollNo": str})




def save_data(df):
    df.to_csv(FILE, index=False)




def add_data(student):
    df = read_data()


    # Validate student details
    if not student.get("RollNo") or not student.get("Name"):
        print("Roll number and name cannot be empty!")
        return


    roll = str(student["RollNo"]).strip()


    # Pandas duplicate check
    if df["RollNo"].eq(roll).any():
        print("Roll number already exists!")
        return


    # NumPy validation for subject marks
    subjects = ["Maths", "Science", "English"]


    try:
        marks = np.asarray(
            [student[subject] for subject in subjects],
            dtype=float
        )
    except (KeyError, TypeError, ValueError):
        print("Invalid or missing subject marks!")
        return


    if not np.all(np.isfinite(marks) & (marks >= 0) & (marks <= 100)):
        print("Marks must be between 0 and 100!")
        return


    student["RollNo"] = roll


    # Pandas adds the new record
    new_record = pd.DataFrame([student], columns=COLUMNS)
    df = pd.concat([df, new_record], ignore_index=True)


    save_data(df)
    print("Student data added successfully!")




def delete_data(roll):
    df = read_data()
    roll = str(roll).strip()


    # Pandas checks whether the roll number exists
    if not df["RollNo"].eq(roll).any():
        print("Student not found!")
        return


    # Remove matching record without a manual loop
    df = df.loc[~df["RollNo"].eq(roll)]


    save_data(df)
    print("Student data deleted successfully!")
