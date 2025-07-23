import streamlit as st
import sys
import argparse
from subject_tracking import init_db, mark_attendance, add_marks, get_subject_performance, get_all_subjects

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    st.header("Subject-wise Tracking")
    
    # Get all subjects for the user
    subjects = get_all_subjects(args.username)
    
    # Add new subject section
    st.subheader("Add New Subject")
    new_subject = st.text_input("Enter New Subject Name", key="new_subject_input")
    if st.button("Add Subject"):
        if new_subject:
            # Add a dummy attendance record to create the subject in the database
            mark_attendance(args.username, new_subject, "Present")
            st.success(f"Subject {new_subject} added successfully!")
            # Clear the input field
            st.text_input("Enter New Subject Name", value="", key="new_subject_input_clear")
            # Refresh the page to show the new subject
            st.rerun()
    
    # Get updated subjects list
    subjects = get_all_subjects(args.username)
    
    if subjects:
        # Subject selection
        selected_subject = st.selectbox("Select Subject", subjects)
        
        # Attendance Section
        st.subheader("Attendance")
        attendance_status = st.radio("Mark Attendance", ["Present", "Absent"])
        if st.button("Submit Attendance"):
            mark_attendance(args.username, selected_subject, attendance_status)
            st.success("Attendance marked successfully!")
        
        # Marks Section
        st.subheader("Marks")
        test_name = st.text_input("Test Name")
        marks = st.number_input("Marks", min_value=0, max_value=100)
        if st.button("Add Marks"):
            add_marks(args.username, selected_subject, test_name, marks)
            st.success("Marks added successfully!")
        
        # Performance Overview
        st.subheader("Performance Overview")
        attendance_df, marks_df = get_subject_performance(args.username, selected_subject)
        
        if not attendance_df.empty or not marks_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Attendance History")
                if not attendance_df.empty:
                    st.dataframe(attendance_df)
                else:
                    st.info("No attendance records yet")
            with col2:
                st.write("Marks History")
                if not marks_df.empty:
                    st.dataframe(marks_df)
                else:
                    st.info("No marks recorded yet")
        else:
            st.info("No data available for this subject yet. Start by marking attendance or adding marks.")
    else:
        st.info("No subjects added yet. Please add a subject first.")

if __name__ == "__main__":
    main() 