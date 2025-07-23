import streamlit as st
import pandas as pd

# Load the data to get column names and unique values
df = pd.read_csv('./student_personality_prediction/student.csv', skiprows=1)
df = df.dropna()
df = df.drop(['Class_Lable', 'Rollno'], axis=1)

# Create the selectbox for roll numbers
st.header('SELECT YOUR ROLL NO.')
all_lists = {
    'Pujitha': [f"20241A{i:04d}" for i in range(1201, 1251)],
    'Vyshnavi': [f"20241A{i:04d}" for i in range(1251, 1300)],
    'Preethi': [f"20241A12{j}{i}" for j in [''] + [chr(c) for c in range(ord('A'), ord('J'))] for i in range(10)],
    'PQR': [f"20241A05{j}{i}" for j in [''] + [chr(c) for c in range(ord('A'), ord('J'))] for i in range(10)],
    'KLM': [f"20241A05{j}{i}" for j in [chr(c) for c in range(ord('I'), ord('N'))] for i in range(1, 10)],
    'JEN': [f"20241A04{j}{i}" for j in [''] + [chr(c) for c in range(ord('A'), ord('J'))] for i in range(10)],
    'ABC': [f"20241A0{i:03d}" for i in range(201, 251)],
    'XYZ': [f"20241A0{i:03d}" for i in range(501, 551)],
    'HIJ': [f"20241A0{i:03d}" for i in range(551, 600)],
    'DEF': [f"20241A0{i:03d}" for i in range(401, 451)],
    'VUK': [f"20241A{i:04d}" for i in range(3201, 3251)],
    'HIG': [f"20241A{i:04d}" for i in range(6601, 6652)],
    'MPS': [f"20241A{i:04d}" for i in range(6701, 6752)],
    'JOHN': [f"20241A0{i:03d}" for i in range(451, 500)]
}

selected_roll_no = st.selectbox('Select your roll number', list(all_lists.keys()))

# Create a select box for each feature
user_input = {}
for column in df.columns:
    unique_values = pd.unique(df[column])
    user_input[column] = st.selectbox(f'Select value for {column}', options=unique_values)

def predict_personality(input_data):
    # Define thresholds for different personality traits based on user input
    nervous_threshold = 3.5
    listener_threshold = 4.0
    comfort_threshold = 2.0
    joke_reaction_threshold = 3.0
    initiation_threshold = 3.0
    participation_threshold = 4.0
    future_brightness_threshold = 4.0
    bad_situation_threshold = 3.0
    disagreement_threshold = 3.5
    empathy_threshold = 3.5
    initiative_threshold = 3.0
    responsibility_threshold = 3.5
    feedback_threshold = 3.0
    appreciation_threshold = 3.5
    interest_threshold = 3.0
    exam_satisfaction_threshold = 3.5
    class_pace_threshold = 3.0
    learning_environment_threshold = 3.5
    working_mode_threshold = 3.0
    motivation_threshold = 3.0
    deadline_threshold = 3.5
    weakness_identification_threshold = 3.5
    inspiration_threshold = 3.5
    conversation_initiation_threshold = 3.0
    talking_to_strangers_threshold = 3.5
    nervous_to_talk_threshold = 2.5
    quiet_due_to_skills_threshold = 2.5
    quiet_due_to_communication_threshold = 3.5
    work_recognition_threshold = 3.0
    teamwork_completion_threshold = 3.5
    good_listener_threshold = 4.0
    time_for_others_threshold = 3.0
    volunteering_threshold = 3.5
    fear_of_corruption_threshold = 3.0
    pressure_to_join_threshold = 3.0
    course_comprehension_threshold = 3.5
    concept_reflection_threshold = 3.0
    prerequisite_knowledge_threshold = 3.0
    knowledge_gap_filling_threshold = 3.5
    shy_to_ask_doubts_threshold = 3.5
    exam_preparation_threshold = 3.0

    # Extract input values from input data
    nervousness = input_data['I feel Nervous in a group']
    listener = input_data['I am a good Listener']
    comfort = input_data['I am comfortable around people']
    joke_reaction = input_data['How do I react to jokes cracked on me ?']
    initiation = input_data['I cannot take initiation']
    participation = input_data['My Participation in a College Annual Events (Multiple answers possible)']
    future_brightness = input_data['I look my future is bright']
    bad_situation_reaction = input_data['I can come out of Bad Situations / Bad memories Quickly']
    disagreement_handling = input_data['If people [Parents/Friends] disagree with me, I cannot accept and express my anger.']
    empathy = input_data['I do not see things from others perspective']
    volunteering = input_data['If someone needs my help, but hesitates to ask, I volunteer my help spontaneously and unconditionally']
    responsibility = input_data['In general I feel I am responsible for my works']
    feedback_handling = input_data['I get defensive when receiving poor feedback.']
    appreciation = input_data['I can appreciate the achievements of my competitors']
    interest = input_data['The Branch of study is the field of my interest']
    exam_satisfaction = input_data['I am able to crack the exams to my satisfaction']
    class_pace = input_data['I am able to cope up with the pace of classwork']
    learning_environment = input_data['I am happy with the learning environment of the college']
    working_mode = input_data['My Working Mode']
    motivation = input_data['I can motivate myself to do difficult tasks']
    deadline_meeting = input_data['I never miss the deadlines']
    weakness_identification = input_data['I can identify my weakness and set targets to overcome them']
    inspiration = input_data['I get inspired by the contributions of people in my field']
    conversation_initiation_difficulty = input_data['It is difficult for me to initiate a conversation in a new Group or with a new person']
    talking_to_strangers_preference = input_data['I prefer to talk to different people whom I have not met before']
    nervous_to_talk = input_data['I am a bit nervous to talk to new people, so I am quiet']
    quiet_due_to_skills = input_data['I am quiet with new people, as I feel my communication skills are poor']
    quiet_due_to_communication = input_data['I am quiet with new people, as I think the other person knows better than me']
    work_recognition_preference = input_data['In a team work my work must be noticed and recognized.']
    teamwork_completion_preference = input_data['In a team work successful completion of the work matters, whether I am leading the team or someone else is leading the team']
    good_listener_preference = input_data['I am a good listener, I can get the essence of the topic in context with ease']
    time_for_others_preference = input_data['I always volunteer to take out time for others']
    volunteering_preference = input_data['I always volunteer to take out time for others']
    fear_of_corruption = input_data['I am scared, unless I am corrupt I cannot survive in this real world']
    pressure_to_join = input_data['I have joined B.Tech. with parents/relatives/friends pressure']
    course_comprehension = input_data['I can understand my course work with ease']
    concept_reflection = input_data['I usually spend time to reflect on the topics discussed in the class with my classmates for concept assimilation.']
    prerequisite_knowledge_lack = input_data['I am unable to follow the course work, it is bouncing. I understand I lack pre-requisite knowledge for some courses.']
    knowledge_gap_filling_approach = input_data['In case of a difficult course, to fill the pre-requisite knowledge gap, I take time to refer internet, consult faculty for guidance and do not hesitate to take the help of classmates who understood the topic.']
    shy_to_ask_doubts = input_data['I feel shy to ask my friends or faculty my doubts in a course work.']
    exam_preparation_approach = input_data['If certain course work is bouncing, I don\'t bother, I learn the important questions for the exams and pass the exam.']

    # Define personality classes based on the thresholds
    if nervousness >= nervous_threshold and comfort >= comfort_threshold and good_listener_preference >= good_listener_threshold:
        return 'Ambivert'
    elif nervousness >= nervous_threshold and comfort < comfort_threshold and good_listener_preference < good_listener_threshold:
        return 'Introvert'
    elif nervousness < nervous_threshold and comfort >= comfort_threshold and good_listener_preference < good_listener_threshold:
        return 'Extrovert'
    else:
        return 'Unknown'
# Make prediction
#prediction = predict_personality(user_input)
# Make prediction function
def make_prediction(input_data):
    prediction = predict_personality(input_data)
    st.write(f"Predicted Personality Class: {prediction}")
# Display prediction
#st.write(f"Predicted Personality Class: {prediction}")

# Save user data to a CSV file when "Submit" button is pressed
if st.button('Submit'):
    selected_roll_numbers = all_lists[selected_roll_no]
    df_user_input = pd.DataFrame([user_input] * len(selected_roll_numbers))
    df_user_input.insert(0, 'Rollno', selected_roll_numbers)
    filename = f"./student_personality_prediction/{selected_roll_no}.csv"
    df_user_input.to_csv(filename, mode='a', header=False, index=False)
    st.success(f"User data saved to: {filename}")
# Predict button to initiate personality prediction
if st.button('Predict'):
    make_prediction(user_input)