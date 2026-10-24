student.py
import numpy as np
import pandas as pd
import os


FILE = "students.csv"


COLUMNS = [
    "Student_ID",
    "Name",
    "Python",
    "Maths",
    "Computer Networks"
]


SUBJECTS = COLUMNS[2:]




def load_data():
    if not os.path.exists(FILE):
        pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)


    return pd.read_csv(FILE, dtype={"Student_ID": str})




def add_student():
    df = load_data()


    student_id = input("Enter Student ID: ").strip()


    if not student_id:
        print("Student ID cannot be empty!")
        return


    # Pandas duplicate checking
    if df["Student_ID"].eq(student_id).any():
        print("Student ID already exists!")
        return


    name = input("Enter Student Name: ").strip()


    if not name:
        print("Student name cannot be empty!")
        return


    marks = []


    # Input validation loop is necessary
    for subject in SUBJECTS:
        while True:
            try:
                mark = float(input(f"Enter {subject} mark (0-100): "))


                if np.isfinite(mark) and 0 <= mark <= 100:
                    marks.append(mark)
                    break


                print("Enter a valid mark between 0 and 100.")


            except ValueError:
                print("Please enter a valid number.")


    # NumPy array for marks
    marks = np.array(marks, dtype=float)


    # Pandas creates the student record
    student = pd.DataFrame([{
        "Student_ID": student_id,
        "Name": name,
        **dict(zip(SUBJECTS, marks))
    }])


    # Add the new record
    df = pd.concat([df, student], ignore_index=True)
    df.to_csv(FILE, index=False)


    print("Student added successfully!")




def view_students():
    df = load_data()


    if df.empty:
        print("No student records found.")
    else:
        print("\n--- Student Records ---")
        print(df.to_string(index=False))




def search_student():
    df = load_data()
    student_id = input("Enter Student ID to search: ").strip()


    # Pandas filtering
    result = df.loc[df["Student_ID"].eq(student_id)]


    if result.empty:
        print("Student not found!")
    else:
        print(result.to_string(index=False))




def delete_student():
    df = load_data()
    student_id = input("Enter Student ID to delete: ").strip()


    # Pandas filtering
    result = df.loc[df["Student_ID"].eq(student_id)]


    if result.empty:
        print("Student not found!")
        return


    # Remove matching student without a manual loop
    df = df.loc[~df["Student_ID"].eq(student_id)]


    df.to_csv(FILE, index=False)
    print("Student deleted successfully!")




if __name__ == "__main__":
    while True:
        print("\n1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Exit")


        choice = input("Enter choice: ").strip()


        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")
