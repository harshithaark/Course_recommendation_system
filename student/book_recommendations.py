import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyArFsF8XTEyuPDbQhtvGjZfygziLN6RF7o")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

gen_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def get_book_recommendations(subject, performance_level):
    prompt = f'''You are an educational assistant. Based on the following information:
    Subject: {subject}
    Performance Level: {performance_level}
    
    Please recommend 3-5 books or study materials that would help improve understanding in this subject.
    For each recommendation, include:
    1. Book/Resource name
    2. Author
    3. Brief description
    4. Why it's suitable for the given performance level
    
    Format the response in a clear, structured way.'''
    
    try:
        response = gen_model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "I'm sorry, couldn't generate recommendations at this time." 