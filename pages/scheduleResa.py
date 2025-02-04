import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()
# Initialize session state to hold tasks
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = {
        "Monday": "",
        "Tuesday": "",
        "Wednesday": "",
        "Thursday": "",
        "Friday": "",
        "Saturday": "",
        "Sunday": ""
    }

# Function to display and edit tasks for a specific day
def edit_task(day):
    task = st.text_input(f"Tasks for {day}", st.session_state['tasks'][day], key=day)
    st.session_state['tasks'][day] = task

# Title of the app
st.title("Weekly Schedule")

# Display buttons for each day
for day in st.session_state['tasks'].keys():
    if st.button(day):
        edit_task(day)

# Display the schedule
st.write("### Your Weekly Schedule")
for day, task in st.session_state['tasks'].items():
    st.write(f"**{day}**: {task}")

# Download the updated schedule
@st.cache_data
def convert_to_csv(tasks):
    import pandas as pd
    df = pd.DataFrame(list(tasks.items()), columns=['Day', 'Tasks'])
    return df.to_csv(index=False).encode('utf-8')

csv = convert_to_csv(st.session_state['tasks'])

st.download_button(
    label="Download Schedule as CSV",
    data=csv,
    file_name='weekly_schedule.csv',
    mime='text/csv',
)
