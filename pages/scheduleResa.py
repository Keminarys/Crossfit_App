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

# Display the title of the app
st.title('Weekly Sports Scheduler')

# Function to update the schedule
def update_schedule(day, activity):
    st.session_state['schedule'].loc[st.session_state['schedule']['Day'] == day, 'Activity'] = activity

# Create a select box for choosing the day
selected_day = st.selectbox('Select a day to view or edit:', st.session_state['schedule']['Day'])

# Display the editable schedule for the selected day
row = st.session_state['schedule'][st.session_state['schedule']['Day'] == selected_day].iloc[0]
activity = st.text_input(f"Activity for {selected_day}", row['Activity'], key=selected_day)
update_schedule(selected_day, activity)

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
