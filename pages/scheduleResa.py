import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
from utils.functions import go_home

st.set_page_config(layout="wide")
go_home()
# # Get the current date and time
# current_date = datetime.now()
# current_date = current_date.date()

# previous_monday = current_date - timedelta(days=current_date.weekday())

# # Find the next Sunday
# next_sunday = previous_monday + timedelta(days=6)

# st.write(previous_monday, current_date, next_sunday)


# # Initialize the dataframe for the schedule
# if 'schedule' not in st.session_state:
#     week_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
#     initial_schedule = pd.DataFrame({'Day': week_days, 'Activity': [''] * 7})
#     st.session_state['schedule'] = initial_schedule

# # Get the current date
# current_date = datetime.now().date()

# # Find the previous Monday
# start_of_week = current_date - timedelta(days=current_date.weekday())

# # Create a dataframe with the dates for the current week
# current_week_dates = [(start_of_week + timedelta(days=i)).strftime('%d/%m/%y') for i in range(7)]
# st.session_state['dates'] = pd.DataFrame({'Day': week_days, 'Date': current_week_dates})

# # Display the title of the app
# st.title('Weekly Sports Scheduler')
# st.subheader("WORK IN PROGRESS // Only a sketch at the moment")
# # Function to update the schedule
# def update_schedule(day, activity):
#     st.session_state['schedule'].loc[st.session_state['schedule']['Day'] == day, 'Activity'] = activity

# # Initialize the selected day
# if 'selected_day' not in st.session_state:
#     st.session_state['selected_day'] = st.session_state['dates'].iloc[0]

# # Create a row for the day buttons
# columns = st.columns(7)
# for index, row in st.session_state['dates'].iterrows():
#     with columns[index]:
#         day_name = row['Day']
#         date_str = row['Date']
#         if st.button(f"{day_name} ({date_str})"):
#             st.session_state['selected_day'] = row

# # Get the selected day and date
# selected_day = st.session_state['selected_day']

# # Display the editable schedule for the selected day
# day_name = selected_day['Day']
# date_str = selected_day['Date']
# row = st.session_state['schedule'][st.session_state['schedule']['Day'] == day_name].iloc[0]
# activity = st.text_input(f"Activity for {day_name}", row['Activity'], key=day_name)
# update_schedule(day_name, activity)

# # Display the card for the selected day
# st.markdown(f"""
# <div style='background-color: #4CAF50; padding: 20px; margin: 10px; border-radius: 5px; text-align: center;'>
#     <h2 style='color: white;'>{date_str}</h2>
#     <p style='color: white;'>{activity}</p>
# </div>
# """, unsafe_allow_html=True)

# # Display the final schedule
# st.subheader('Your Schedule')
# st.table(st.session_state['schedule'])



# Get current date and determine Monday of the current week
today = date.today()
monday = today - timedelta(days=today.weekday())
days = [monday + timedelta(days=i) for i in range(7)]

# Define example workout details for each day
workout_data = {
    "Monday": "Squat 5x5 & Core Training",
    "Tuesday": "Bench Press & HIIT Cardio",
    "Wednesday": "Deadlifts & Mobility",
    "Thursday": "Pull-ups & Conditioning",
    "Friday": "Power Cleans & Speed Work",
    "Saturday": "Full-body Circuit",
    "Sunday": "Rest & Recovery"
}

# Streamlit UI
st.title("Weekly Workout Plan")

# Display buttons for each day
selected_day = None
for day in days:
    if st.button(day.strftime("%A")):
        selected_day = day.strftime("%A")

# Display workout details for the selected day
if selected_day:
    st.subheader(f"Workout for {selected_day}")
    st.info(workout_data[selected_day])

