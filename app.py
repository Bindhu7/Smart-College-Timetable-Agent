import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# Timetable Builder Function
# -------------------------------
def build_timetable(assignments, courses, faculty, rooms, time_slots, student_groups):
    merged = assignments.merge(courses, on="course_id", how="left") \
                        .merge(faculty, on="faculty_id", how="left") \
                        .merge(rooms, on="room_id", how="left") \
                        .merge(student_groups, on="group_id", how="left") \
                        .merge(time_slots, on="slot_id", how="left")
    timetable = merged[["day","slot_number","course_name","faculty_name","room_name","group_name"]]
    return timetable.sort_values(["day","slot_number"])

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📅 Smart College Timetable Scheduling Agent")

st.markdown("Upload your dataset files (Excel/CSV) to generate and visualize the timetable.")

# File uploaders
assignments_file = st.file_uploader("Upload Assignments Data", type=["xlsx","csv"])
courses_file = st.file_uploader("Upload Courses Data", type=["xlsx","csv"])
faculty_file = st.file_uploader("Upload Faculty Data", type=["xlsx","csv"])
rooms_file = st.file_uploader("Upload Rooms Data", type=["xlsx","csv"])
groups_file = st.file_uploader("Upload Student Groups Data", type=["xlsx","csv"])
slots_file = st.file_uploader("Upload Time Slots Data", type=["xlsx","csv"])

if assignments_file and courses_file and faculty_file and rooms_file and groups_file and slots_file:
    # Load data
    assignments = pd.read_excel(assignments_file) if assignments_file.name.endswith("xlsx") else pd.read_csv(assignments_file)
    courses = pd.read_excel(courses_file) if courses_file.name.endswith("xlsx") else pd.read_csv(courses_file)
    faculty = pd.read_excel(faculty_file) if faculty_file.name.endswith("xlsx") else pd.read_csv(faculty_file)
    rooms = pd.read_excel(rooms_file) if rooms_file.name.endswith("xlsx") else pd.read_csv(rooms_file)
    student_groups = pd.read_excel(groups_file) if groups_file.name.endswith("xlsx") else pd.read_csv(groups_file)
    time_slots = pd.read_excel(slots_file) if slots_file.name.endswith("xlsx") else pd.read_csv(slots_file)

    # Build timetable
    timetable = build_timetable(assignments, courses, faculty, rooms, time_slots, student_groups)

    st.subheader("📋 Detailed Timetable")
    st.dataframe(timetable)

    # Pivoted timetable
    pivot = timetable.pivot_table(index=["day","slot_number"],
                                  columns="group_name",
                                  values="course_name",
                                  aggfunc=lambda x: ', '.join(x))

    st.subheader("📊 Pivoted Timetable by Student Group")
    st.dataframe(pivot)

    # Heatmap visualization
    st.subheader("🎨 Timetable Occupancy Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(pivot.notnull(), cmap="YlGnBu", cbar=False, linewidths=0.5, ax=ax)
    ax.set_title("Timetable Occupancy Heatmap", fontsize=16, color="#1b5e20")
    ax.set_xlabel("Student Groups")
    ax.set_ylabel("Day & Slot")
    st.pyplot(fig)

    # Export option
    st.download_button(
        label="Download Timetable (Excel)",
        data=timetable.to_excel(index=False, engine="openpyxl"),
        file_name="Smart_College_Timetable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload all required files to generate the timetable.")
