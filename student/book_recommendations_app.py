import streamlit as st
import sys
import argparse
from subject_tracking import get_all_subjects
from book_recommendations import get_book_recommendations

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    args = parser.parse_args()
    
    st.header("Book Recommendations for Weak Subjects")
    
    subjects = get_all_subjects(args.username)
    
    if subjects:
        selected_subject = st.selectbox("Select Subject", subjects)
        performance_level = st.select_slider(
            "Performance Level",
            options=["Very Weak", "Weak", "Average", "Good", "Excellent"]
        )
        
        if st.button("Get Recommendations"):
            recommendations = get_book_recommendations(selected_subject, performance_level)
            st.markdown(recommendations)
    else:
        st.warning("No subjects found. Please add subjects in the Subject Tracking section.")

if __name__ == "__main__":
    main() 