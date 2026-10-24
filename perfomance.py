
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date

# ==============================
# STUDENT PERFORMANCE ANALYSIS
# ==============================

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

FILE = Path("student_performance.csv")

SUBJECTS = ["Python", "Mathematics", "Computer Networks"]

SOFT_SKILLS = [
    "Communication",
    "Teamwork",
    "Leadership",
    "Problem Solving",
    "Time Management"
]


# ---------- DATABASE ----------

def load_data():
    if FILE.exists():
        try:
            return pd.read_csv(FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            return pd.DataFrame()
    return pd.DataFrame()


def save_record(record):
    old_data = load_data()
    new_data = pd.DataFrame([record])
    combined = pd.concat([old_data, new_data], ignore_index=True)
    combined.to_csv(FILE, index=False)


# ---------- PERFORMANCE CALCULATION ----------

def analyse_performance(record):
    test_marks = np.array(
        [float(record[f"{s} Test"]) for s in SUBJECTS]
    )
    exam_marks = np.array(
        [float(record[f"{s} Exam"]) for s in SUBJECTS]
    )

    test_average = float(np.mean(test_marks))
    exam_average = float(np.mean(exam_marks))

    # Academic score: tests 30%, exams 70%
    academic_score = (
        test_average * 0.30
        + exam_average * 0.70
    )

    working_days = int(record["Working Days"])
    present_days = int(record["Days Present"])

    attendance = (
        present_days / working_days * 100
        if working_days > 0 else 0
    )

    assignments_given = int(record["Assignments Given"])
    assignments_done = int(record["Assignments Completed"])

    assignment_score = (
        assignments_done / assignments_given * 100
        if assignments_given > 0 else 0
    )

    activity_score = float(record["Activity Rating"]) * 20

    soft_score = float(np.mean([
        float(record[s]) for s in SOFT_SKILLS
    ])) * 20

    sports_score = float(record["Sports Rating"]) * 20
    discipline_score = float(record["Discipline Rating"]) * 20

    # Overall score: illustrative project weighting
    overall = (
        academic_score * 0.45
        + attendance * 0.15
        + assignment_score * 0.10
        + activity_score * 0.10
        + soft_score * 0.10
        + sports_score * 0.05
        + discipline_score * 0.05
    )

    if overall >= 90:
        grade = "A"
    elif overall >= 80:
        grade = "B"
    elif overall >= 70:
        grade = "C"
    elif overall >= 60:
        grade = "D"
    else:
        grade = "Needs Improvement"

    failed = [
        subject for subject in SUBJECTS
        if record[f"{subject} Test"] < 35
        or record[f"{subject} Exam"] < 35
    ]

    return {
        "Test Average": round(test_average, 2),
        "Exam Average": round(exam_average, 2),
        "Academic Score": round(academic_score, 2),
        "Attendance %": round(attendance, 2),
        "Assignment Completion %": round(assignment_score, 2),
        "Activity Score": round(activity_score, 2),
        "Soft Skills Score": round(soft_score, 2),
        "Sports Score": round(sports_score, 2),
        "Discipline Score": round(discipline_score, 2),
        "Overall Score": round(overall, 2),
        "Overall Grade": grade,
        "Subject Alerts": ", ".join(failed) if failed else "None"
    }


# ---------- STUDENT SUGGESTIONS ----------

def get_suggestions(record):
    suggestions = []

    if record["Attendance %"] < 75:
        suggestions.append(
            "Attendance is below 75%. Improve attendance."
        )

    if record["Exam Average"] < 50:
        suggestions.append(
            "Provide extra revision and practice for exams."
        )

    if record["Assignment Completion %"] < 80:
        suggestions.append(
            "Complete pending assignments on time."
        )

    if record["Soft Skills Score"] < 60:
        suggestions.append(
            "Practise communication, teamwork and leadership."
        )

    if record["Activity Score"] < 60:
        suggestions.append(
            "Consider participating in clubs, seminars or cultural events."
        )

    if record["Sports Score"] < 60:
        suggestions.append(
            "Consider suitable sports or fitness activities."
        )

    if record["Subject Alerts"] != "None":
        suggestions.append(
            "Additional academic support recommended for: "
            + record["Subject Alerts"]
        )

    if not suggestions:
        suggestions.append(
            "Good overall progress. Continue learning and developing skills."
        )

    return suggestions


# ---------- WEB APPLICATION ----------

st.title("🎓 Student Performance Analysis System")
st.caption(
    "Academic Results | Attendance | Activities | "
    "Soft Skills | Sports | Student Development"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Performance",
        "Student Report",
        "All Records"
    ]
)

data = load_data()


# ==============================
# DASHBOARD
# ==============================

if page == "Dashboard":
    st.header("📊 Performance Dashboard")

    if data.empty:
        st.info("No student records available. Add a record first.")
    elif "Overall Score" not in data.columns:
        st.warning(
            "Please add a new performance record to generate "
            "the analysis columns."
        )
    else:
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Records", len(data))
        c2.metric(
            "Average Overall Score",
            f"{pd.to_numeric(data['Overall Score'], errors='coerce').mean():.1f}%"
        )
        c3.metric(
            "Average Attendance",
            f"{pd.to_numeric(data['Attendance %'], errors='coerce').mean():.1f}%"
        )
        c4.metric(
            "Students Below 75% Attendance",
            int((pd.to_numeric(
                data["Attendance %"], errors="coerce"
            ) < 75).sum())
        )

        st.subheader("Overall Score Comparison")

        chart = data[["Student ID", "Name", "Overall Score"]].copy()
        chart["Student"] = (
            chart["Student ID"].astype(str)
            + " - "
            + chart["Name"].astype(str)
        )
        chart["Overall Score"] = pd.to_numeric(
            chart["Overall Score"], errors="coerce"
        )
        st.bar_chart(chart.set_index("Student")["Overall Score"])

        st.subheader("Recent Records")
        st.dataframe(data.tail(10), use_container_width=True)

        if "Overall Score" in data.columns:
            st.subheader("Top Performance Records")
            top = data.sort_values(
                "Overall Score", ascending=False
            ).head(5)
            st.dataframe(top, use_container_width=True)


# ==============================
# ADD PERFORMANCE
# ==============================

elif page == "Add Performance":
    st.header("➕ Add Student Performance")

    with st.form("student_performance_form"):
        st.subheader("1. Student Details")

        c1, c2, c3 = st.columns(3)
        student_id = c1.text_input("Student ID *")
        name = c2.text_input("Student Name *")
        department = c3.text_input("Department / Class")

        c4, c5 = st.columns(2)
        semester = c4.text_input("Semester / Term")
        assessment_date = c5.date_input(
            "Assessment Date", value=date.today()
        )

        st.subheader("2. Test and Examination Marks")

        marks = {}

        for subject in SUBJECTS:
            left, right = st.columns(2)

            marks[f"{subject} Test"] = left.number_input(
                f"{subject} - Test Mark / 100",
                min_value=0.0, max_value=100.0,
                value=0.0, step=1.0,
                key=f"test_{subject}"
            )

            marks[f"{subject} Exam"] = right.number_input(
                f"{subject} - Exam Mark / 100",
                min_value=0.0, max_value=100.0,
                value=0.0, step=1.0,
                key=f"exam_{subject}"
            )

        st.subheader("3. Attendance")

        a1, a2 = st.columns(2)

        working_days = a1.number_input(
            "Total Working Days", min_value=0, value=100
        )
        days_present = a2.number_input(
            "Days Present", min_value=0, value=90
        )

        st.subheader("4. Assignments")

        b1, b2 = st.columns(2)

        assignments_given = b1.number_input(
            "Assignments Given", min_value=0, value=10
        )
        assignments_completed = b2.number_input(
            "Assignments Completed", min_value=0, value=8
        )

        st.subheader("5. Co-curricular Activities")

        activity_rating = st.slider(
            "Participation Rating (1-5)",
            min_value=1, max_value=5, value=3
        )

        activities = st.text_area(
            "Activities, Seminars, Clubs, Cultural Events, Volunteering"
        )

        st.subheader("6. Soft Skills (1 = Low, 5 = Excellent)")

        skills = {}

        skill_cols = st.columns(5)
        for col, skill in zip(skill_cols, SOFT_SKILLS):
            skills[skill] = col.slider(
                skill, min_value=1, max_value=5,
                value=3, key=f"skill_{skill}"
            )

        st.subheader("7. Sports and Achievements")

        sports_rating = st.slider(
            "Sports Participation Rating (1-5)",
            min_value=1, max_value=5, value=3
        )

        sports_achievements = st.text_area(
            "Sports Achievements / Awards"
        )

        other_achievements = st.text_area(
            "Projects, Certifications and Other Achievements"
        )

        st.subheader("8. Discipline and Teacher Feedback")

        discipline_rating = st.slider(
            "Punctuality, Responsibility and Conduct (1-5)",
            min_value=1, max_value=5, value=3
        )

        teacher_remarks = st.text_area("Teacher Remarks / Support Plan")

        submitted = st.form_submit_button(
            "Calculate Performance and Save",
            type="primary"
        )

    if submitted:
        if not student_id.strip() or not name.strip():
            st.error("Student ID and Student Name are required.")

        elif working_days == 0 and days_present > 0:
            st.error("Working days must be greater than zero.")

        elif days_present > working_days:
            st.error("Days Present cannot exceed Working Days.")

        elif assignments_completed > assignments_given:
            st.error(
                "Assignments Completed cannot exceed Assignments Given."
            )

        else:
            record = {
                "Student ID": student_id.strip(),
                "Name": name.strip(),
                "Department / Class": department,
                "Semester / Term": semester,
                "Assessment Date": str(assessment_date),
                **marks,
                "Working Days": int(working_days),
                "Days Present": int(days_present),
                "Assignments Given": int(assignments_given),
                "Assignments Completed": int(assignments_completed),
                "Activity Rating": activity_rating,
                "Activities": activities,
                **skills,
                "Sports Rating": sports_rating,
                "Sports Achievements": sports_achievements,
                "Other Achievements": other_achievements,
                "Discipline Rating": discipline_rating,
                "Teacher Remarks": teacher_remarks
            }

            analysis = analyse_performance(record)
            record.update(analysis)

            try:
                save_record(record)

                st.success("Student performance saved successfully!")

                st.subheader("Performance Summary")

                m1, m2, m3, m4 = st.columns(4)
                m1.metric(
                    "Academic Score",
                    f"{analysis['Academic Score']:.1f}%"
                )
                m2.metric(
                    "Attendance",
                    f"{analysis['Attendance %']:.1f}%"
                )
                m3.metric(
                    "Overall Score",
                    f"{analysis['Overall Score']:.1f}%"
                )
                m4.metric("Grade", analysis["Overall Grade"])

                st.subheader("Category-wise Analysis")

                categories = pd.DataFrame({
                    "Score (%)": {
                        "Academic": analysis["Academic Score"],
                        "Attendance": analysis["Attendance %"],
                        "Assignments": analysis["Assignment Completion %"],
                        "Co-curricular": analysis["Activity Score"],
                        "Soft Skills": analysis["Soft Skills Score"],
                        "Sports": analysis["Sports Score"],
                        "Discipline": analysis["Discipline Score"]
                    }
                })

                st.bar_chart(categories)

                st.subheader("Analysis and Improvement Suggestions")
                for suggestion in get_suggestions(analysis):
                    st.write("- " + suggestion)

                st.caption(
                    "The overall score uses illustrative project weights: "
                    "Academic 45%, Attendance 15%, Assignments 10%, "
                    "Activities 10%, Soft Skills 10%, Sports 5%, "
                    "Discipline 5%. Confirm these weights with your teacher."
                )

            except OSError as error:
                st.error(f"Unable to save the CSV file: {error}")


# ==============================
# INDIVIDUAL STUDENT REPORT
# ==============================

elif page == "Student Report":
    st.header("🧾 Individual Student Report")

    if data.empty or "Student ID" not in data.columns:
        st.info("No student records found. Add a record first.")

    else:
        student_ids = sorted(
            data["Student ID"].dropna().astype(str).unique()
        )

        selected_id = st.selectbox("Select Student ID", student_ids)

        student_data = data[
            data["Student ID"].astype(str) == selected_id
        ].copy()

        st.dataframe(student_data, use_container_width=True)

        if "Overall Score" in student_data.columns:
            latest = student_data.iloc[-1]

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Overall Score",
                f"{float(latest['Overall Score']):.1f}%"
            )
            c2.metric(
                "Attendance",
                f"{float(latest['Attendance %']):.1f}%"
            )
            c3.metric("Grade", str(latest["Overall Grade"]))

            st.subheader("Subject-wise Marks")

            subject_report = pd.DataFrame({
                "Test": [
                    latest.get(f"{s} Test", 0) for s in SUBJECTS
                ],
                "Exam": [
                    latest.get(f"{s} Exam", 0) for s in SUBJECTS
                ]
            }, index=SUBJECTS)

            st.bar_chart(subject_report)

            st.subheader("Improvement Suggestions")
            for suggestion in get_suggestions(latest):
                st.write("- " + suggestion)

        st.download_button(
            "Download Student Report (CSV)",
            data=student_data.to_csv(index=False).encode("utf-8"),
            file_name=f"student_{selected_id}_report.csv",
            mime="text/csv"
        )


# ==============================
# ALL STUDENT RECORDS
# ==============================

elif page == "All Records":
    st.header("📚 All Student Records")

    if data.empty:
        st.info("No records available.")

    else:
        search_id = st.text_input("Search by Student ID")

        view = data.copy()

        if search_id:
            view = view[
                view["Student ID"].astype(str).str.contains(
                    search_id, case=False, na=False
                )
            ]

        st.dataframe(view, use_container_width=True)

        st.download_button(
            "Download All Records (CSV)",
            data=view.to_csv(index=False).encode("utf-8"),
            file_name="student_performance_records.csv",
            mime="text/csv"
        )

        st.caption(f"CSV file: {FILE.resolve()}")

