import streamlit as st
from datetime import datetime, timedelta

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()

previous_monday = current_date - timedelta(days=current_date.weekday())

# Find the next Sunday
next_sunday = previous_monday + timedelta(days=6)

st.write(previous_monday, current_date, next_sunday)



import pandas as pd


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

# Display the editable schedule
for index, row in st.session_state['schedule'].iterrows():
    activity = st.text_input(f"Activity for {row['Day']}", row['Activity'], key=row['Day'])
    update_schedule(row['Day'], activity)

# Display the final schedule
st.subheader('Your Schedule')
st.table(st.session_state['schedule'])
