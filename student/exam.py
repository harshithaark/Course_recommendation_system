import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyArFsF8XTEyuPDbQhtvGjZfygziLN6RF7o")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def generate_response(text: str):
    prompt = f'''You are a helpful mentor chatbot. Respond to the following in a supportive, educational, and engaging way: {text}'''
    try:
        response = model.generate_content(prompt)
        if len(response.text) == 0:
            return "I'm sorry, I don't understand. Can you please rephrase?"
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.title("Exam Training Planner")

exam_days = st.number_input("How many days are there until your exam?", min_value=1, step=1)
subject_count = st.number_input("How many subjects do you have?", min_value=1, step=1)

subjects = []
for i in range(subject_count):
    subject = st.text_input(f"Enter the name of subject {i + 1}:")
    subjects.append(subject)

if st.button("Generate Syllabus and Timetable"):
    syllabus = ""
    for subject in subjects:
        syllabus += f"Subject: {subject}\n"
        syllabus_response = generate_response(f"Please provide a syllabus for {subject}. Just give a list like output and don't do a lot of extra effort.")
        syllabus += syllabus_response + "\n\n"
    
    timetable_prompt = f"Create a study timetable for a student who has {exam_days} days left for their exam and needs to study the following subjects: {', '.join(subjects)}."
    timetable = generate_response(timetable_prompt)

    st.subheader("Generated Syllabus:")
    st.markdown(syllabus)

    st.subheader("Suggested Timetable:")
    st.markdown(timetable)