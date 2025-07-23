import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('subject_tracking.db')
    return conn

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subject_attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        subject TEXT NOT NULL,
        date DATE NOT NULL,
        status TEXT NOT NULL
    )
    ''')
    
    # Create marks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subject_marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        subject TEXT NOT NULL,
        test_name TEXT NOT NULL,
        marks INTEGER NOT NULL,
        date DATE NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def mark_attendance(username, subject, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First check if attendance for this day already exists
    cursor.execute('''
    SELECT id FROM subject_attendance 
    WHERE username = ? AND subject = ? AND date = date('now')
    ''', (username, subject))
    
    existing_record = cursor.fetchone()
    
    if existing_record:
        # Update existing record
        cursor.execute('''
        UPDATE subject_attendance 
        SET status = ? 
        WHERE id = ?
        ''', (status, existing_record[0]))
    else:
        # Insert new record
        cursor.execute('''
        INSERT INTO subject_attendance (username, subject, date, status)
        VALUES (?, ?, date('now'), ?)
        ''', (username, subject, status))
    
    conn.commit()
    conn.close()

def add_marks(username, subject, test_name, marks):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO subject_marks (username, subject, test_name, marks, date)
    VALUES (?, ?, ?, ?, date('now'))
    ''', (username, subject, test_name, marks))
    conn.commit()
    conn.close()

def get_subject_performance(username, subject):
    conn = get_db_connection()
    
    # Get attendance data
    attendance_df = pd.read_sql_query('''
    SELECT subject, date, status 
    FROM subject_attendance 
    WHERE username = ? AND subject = ?
    ORDER BY date DESC
    ''', conn, params=(username, subject))
    
    # Get marks data
    marks_df = pd.read_sql_query('''
    SELECT subject, test_name, marks, date 
    FROM subject_marks 
    WHERE username = ? AND subject = ?
    ORDER BY date DESC
    ''', conn, params=(username, subject))
    
    conn.close()
    
    return attendance_df, marks_df

def get_all_subjects(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT DISTINCT subject 
    FROM subject_marks 
    WHERE username = ?
    UNION
    SELECT DISTINCT subject 
    FROM subject_attendance 
    WHERE username = ?
    ''', (username, username))
    subjects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return subjects 