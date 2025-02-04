import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()

previous_monday = current_date - timedelta(days=current_date.weekday())

# Find the next Sunday
next_sunday = previous_monday + timedelta(days=6)

st.write(previous_monday, current_date, next_sunday)


# Initialize the dataframe for the schedule
if 'schedule' not in st.session_state:
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    initial_schedule = pd.DataFrame({'Day': week_days, 'Activity': [''] * 7})
    st.session_state['schedule'] = initial_schedule

# Get the current date
current_date = datetime.now().date()

# Find the previous Monday
start_of_week = current_date - timedelta(days=current_date.weekday())

# Create a dataframe with the dates for the current week
current_week_dates = [(start_of_week + timedelta(days=i)).strftime('%A, %d %B') for i in range(7)]
st.session_state['dates'] = pd.DataFrame({'Day': week_days, 'Date': current_week_dates})

# Display the title of the app
st.title('Weekly Sports Scheduler')

# Function to update the schedule
def update_schedule(day, activity):
    st.session_state['schedule'].loc[st.session_state['schedule']['Day'] == day, 'Activity'] = activity

# Display the headers with dates
selected_day = st.selectbox('Select a day to view or edit:', current_week_dates)

# Get the corresponding day name
day_name = st.session_state['dates'].loc[st.session_state['dates']['Date'] == selected_day, 'Day'].values[0]

# Display the editable schedule for the selected day
row = st.session_state['schedule'][st.session_state['schedule']['Day'] == day_name].iloc[0]
activity = st.text_input(f"Activity for {day_name}", row['Activity'], key=day_name)
update_schedule(day_name, activity)

# Display the card for the selected day
st.markdown(f"""
<div style='background-color: #4CAF50; padding: 20px; margin: 10px; border-radius: 5px; text-align: center;'>
    <h2 style='color: white;'>{selected_day}</h2>
    <p style='color: white;'>{activity}</p>
</div>
""", unsafe_allow_html=True)

# Display the final schedule
st.subheader('Your Schedule')
st.table(st.session_state['schedule'])
