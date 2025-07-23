import streamlit as st
from streamlit import session_state
import sqlite3
import os
from PIL import Image, ImageDraw
import base64
from subject_tracking import init_db, mark_attendance, add_marks, get_subject_performance, get_all_subjects
from book_recommendations import get_book_recommendations

# Create Users and Admin Tables
def create_users_table():
    conn = sqlite3.connect("users1.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, contact TEXT, email TEXT, role TEXT)')
    conn.commit()

def create_admins_table():
    conn = sqlite3.connect("admins.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS admins(username TEXT, password TEXT, contact TEXT, email TEXT)')
    conn.commit()

# Add User Function
def add_user(username, password, contact, email, role='user'):
    conn = sqlite3.connect("users1.db")
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, contact, email, role) VALUES (?,?,?,?,?)',
                (username, password, contact, email, role))
    conn.commit()
    st.success(f"{role.capitalize()} account created successfully!")

# Add Admin Function
def add_admin(username, password, contact, email):
    conn = sqlite3.connect("admins.db")
    c = conn.cursor()
    c.execute('INSERT INTO admins(username, password, contact, email) VALUES (?,?,?,?)',
                (username, password, contact, email))
    conn.commit()
    st.success("Admin account created successfully!")

# Get User or Admin
def get_user(username):
    conn = sqlite3.connect("users1.db")
    c = conn.cursor()
    user_info = c.execute('SELECT * FROM users WHERE username =?', (username,))
    for row in user_info:
        return row
    return None

def get_admin(username):
    conn = sqlite3.connect("admins.db")
    c = conn.cursor()
    admin_info = c.execute('SELECT * FROM admins WHERE username =?', (username,))
    for row in admin_info:
        return row
    return None

# Main Function
def main():
    if 'username' not in session_state:
        menu = ["Home", "Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu, key='menu_select')
    else:
        menu = ["Home", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu, key='menu_select')

    if choice == "Home":
        st.header("STUDENT TRACKER")
        if 'username' in session_state:
            # Display user profile and features
            st.image("profile_circle.png", width=300)
            st.markdown('<p style="text-align: center;">Username: {}</p>'.format(session_state.username), unsafe_allow_html=True)

            # User feature boxes
            box_texts = ['Student Analysis System', 'Personality Predictor', 'Course Recommender', 
                         'Question Generator', 'Exam Strategy Maker', 'Exam Training',
                         'Subject Tracking', 'Book Recommendations']
            
            col1, col2, col3 = st.columns(3)
            columns = [col1, col2, col3]
            ls = []
            for i in range(8):
                with columns[i % 3]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(to right, #ff7e5f, #feb47b);
                                padding: 10px; border-radius: 10px; box-shadow: 10px 10px 5px grey;
                                transition: transform .2s; margin-bottom: 30px;">
                        <h3 style="text-align: center;color:black">{box_texts[i]}</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <style>
                    .hoverable:hover {
                        transform: scale(1.02);
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    x = st.button(f"View {i+1}")
                    ls.append(x)
            
            if ls[0]:
                os.system("streamlit run analysis.py")
            if ls[1]:
                os.system("streamlit run ./student_personality_prediction/app.py")
            if ls[2]:
                os.system("streamlit run recom.py")
            if ls[3]:
                os.system("streamlit run dox.py")
            if ls[4]:
                os.system("streamlit run stratergy.py")
            if ls[5]:
                os.system("streamlit run exam.py")
            if ls[6]:
                os.system(f"streamlit run subject_tracking_app.py -- --username {session_state.username}")
            if ls[7]:
                os.system(f"streamlit run book_recommendations_app.py -- --username {session_state.username}")
        else:
            st.markdown("""
            ## Features

### 1. Predictive Analysis
Leverage the power of machine learning to foresee future academic trends. This feature uses past data and current variables to predict student performance, academic outcomes, and more. It's a strategic tool that supports educators in creating a better learning environment by anticipating potential challenges and opportunities.

### 2. Performance Analysis on the Basis of Regular Inputs
Consistently monitor student progress with this interactive performance analysis tool. By collecting regular inputs, it provides timely, in-depth insights into each student's strengths and weaknesses, thereby enabling a more targeted and individualized learning approach.

### 3. Risk Subjects Page
The Risk Subjects Page is a dedicated interface for identifying and managing potential academic risks. This page displays subjects where students may be struggling, providing educators with the necessary data to implement interventions or additional support as necessary.

### 4. Course Recommendation
Our platform takes a personalized approach to education. By understanding each student's interests, strengths, and academic history, it suggests the most suitable courses for them. This way, students can pursue learning pathways that resonate with their personal and professional goals.

### 5. Academic Performance History Based on Past Data
This feature offers a comprehensive view of a student's academic journey. By analyzing historical data, it depicts trends in the student's performance, illustrating their growth, areas of improvement, and ongoing challenges. This valuable resource supports both students and educators in decision-making processes.

### 6. Student Quality Analysis
This robust feature provides a holistic view of student potential and capacity. It evaluates not just academic performance but also other factors like engagement, extracurricular activities, and behavioral tendencies to measure student quality.

### 7. Summary of DOX Page
The Summary of DOX Page consolidates all essential documents, notes, and relevant educational resources in one place for easy access. It's an efficient way to keep track of crucial information and enhance study efficiency.

### 8. Question Generation for Practice
With this feature, students can generate custom practice questions based on their learning needs. It's a flexible, adaptive tool that supports continuous learning and revision, helping students gain mastery over their subjects.

### 9. Exam Strategy Maker Based on Inputs
This feature empowers students to approach their exams strategically. By analyzing individual learning styles, subject knowledge, and past performance, it helps students create an effective exam plan that maximizes their chances of success.

### 10. Progress Tracking
Keep your academic journey on track with our Progress Tracking feature. It provides a visual representation of your learning progress, helping you understand where you stand, what you've achieved, and what your next learning goals should be. This feature helps maintain focus and drive towards success.
            """)

    elif choice == "Login":
        st.header("Academic Tracker")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            create_users_table()
            create_admins_table()
            user_info = get_user(username)
            admin_info = get_admin(username)

            if user_info and user_info[1] == password:  # Regular user login
                session_state.username = username
                st.success(f"Logged In as {username}")
                st.rerun()
            elif admin_info and admin_info[1] == password:  # Admin login
                session_state.username = username
                st.success(f"Logged In as Admin {username}")
                st.rerun()
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")

        role = st.radio("Select Role", ["User", "Admin"])

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        contact = st.text_input("Contact")
        email = st.text_input("Email")

        if role == 'Admin':
            if st.button("Signup as Admin"):
                create_admins_table()
                add_admin(new_user, new_password, contact, email)
                st.info("Admin account created. Go to Login to login.")
        elif role == 'User':
            if st.button("Signup as User"):
                create_users_table()
                add_user(new_user, new_password, contact, email)
                st.info("User account created. Go to Login to login.")

    elif choice == "Logout":
        if 'username' in session_state:
            del session_state.username
            st.success("Logged out successfully!")
            st.rerun()

def show_subject_tracking():
    st.header("Subject-wise Tracking")
    
    # Initialize database
    init_db()
    
    # Get all subjects for the user
    subjects = get_all_subjects(session_state.username)
    
    # Subject selection
    selected_subject = st.selectbox("Select Subject", subjects if subjects else ["Add New Subject"])
    
    if selected_subject == "Add New Subject":
        new_subject = st.text_input("Enter New Subject Name")
        if st.button("Add Subject"):
            if new_subject:
                subjects.append(new_subject)
                st.success(f"Subject {new_subject} added successfully!")
    
    # Attendance Section
    st.subheader("Attendance")
    attendance_status = st.radio("Mark Attendance", ["Present", "Absent"])
    if st.button("Submit Attendance"):
        mark_attendance(session_state.username, selected_subject, attendance_status)
        st.success("Attendance marked successfully!")
    
    # Marks Section
    st.subheader("Marks")
    test_name = st.text_input("Test Name")
    marks = st.number_input("Marks", min_value=0, max_value=100)
    if st.button("Add Marks"):
        add_marks(session_state.username, selected_subject, test_name, marks)
        st.success("Marks added successfully!")
    
    # Performance Overview
    st.subheader("Performance Overview")
    if selected_subject != "Add New Subject":
        attendance_df, marks_df = get_subject_performance(session_state.username, selected_subject)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Attendance History")
            st.dataframe(attendance_df)
        with col2:
            st.write("Marks History")
            st.dataframe(marks_df)

def show_book_recommendations():
    st.header("Book Recommendations for Weak Subjects")
    
    subjects = get_all_subjects(session_state.username)
    
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