
import numpy as np
import pandas as pd

from student import add_student, view_students, search_student, delete_student
from performance import calculate_performance
from reports import show_report


def main():
    while True:
        print("\n======================================")
        print(" STUDENT PERFORMANCE MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Calculate Performance")
        print("6. Class Performance Report")
        print("7. Exit")
        print("======================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            calculate_performance()

        elif choice == "6":
            show_report()

        elif choice == "7":
            print("Thank you for using the application!")
            break

        else:
            print("Invalid choice! Please enter 1 to 7.")


if __name__ == "__main__":
    main()
