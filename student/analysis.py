import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Define the path to the CSV file
csv_file = 'student_data.csv'

# Check if the file exists
if not os.path.isfile(csv_file):
    # Create a new dataframe with the required columns
    df = pd.DataFrame(columns=[
        "Grade/Class", "Subject", "Attendance", "Test Scores", "Homework Scores", 
        "Project Scores", "Participation", "Final Grade", "Extracurricular Activities", "Special Needs", "Behavior/Conduct"
    ])

    # Write the dataframe to a new CSV file
    df.to_csv(csv_file, index=False)

# Function to write data to CSV
def write_data(data):
    df = pd.DataFrame([data], columns=list(data.keys()))
    df.to_csv(csv_file, mode='a', index=False, header=not os.path.getsize(csv_file) > 0)
    st.success("Data saved successfully!")

# Collect student data
st.write("# Enter Student Data")

data = {
    "Grade/Class": st.number_input('Grade/Class', value=0, min_value=0),
    "Subject": st.text_input('Subject', value=''),
    "Attendance": st.number_input('Attendance', value=0.0, min_value=0.0),
    "Test Scores": st.number_input('Test Scores', value=0.0, min_value=0.0),
    "Homework Scores": st.number_input('Homework Scores', value=0.0, min_value=0.0),
    "Project Scores": st.number_input('Project Scores', value=0.0, min_value=0.0),
    "Participation": st.number_input('Participation', value=0.0, min_value=0.0),
    "Final Grade": st.number_input('Final Grade', value=0.0, min_value=0.0),
    "Extracurricular Activities": st.number_input('Extracurricular Activities', value=0.0, min_value=0.0),
    "Special Needs": st.selectbox('Special Needs', options=['Yes', 'No'], index=1),
    "Behavior/Conduct": st.number_input('Behavior/Conduct', value=0.0, min_value=0.0)
}

# Convert Special Needs to numeric for storage
data["Special Needs"] = 1 if data["Special Needs"] == "Yes" else 0

if st.button('Submit'):
    write_data(data)