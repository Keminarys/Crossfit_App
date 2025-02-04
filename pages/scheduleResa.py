import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()

# Title of the app
st.title("Weekly Schedule")

# Create a dictionary to hold the schedule data
schedule = {
    "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "Tasks": [""] * 7  # Initial empty tasks
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(schedule)

# Function to edit tasks
def edit_tasks():
    for index, row in df.iterrows():
        task = st.text_input(f"Tasks for {row['Day']}", row['Tasks'], key=row['Day'])
        df.at[index, 'Tasks'] = task

edit_tasks()

# Display the schedule
st.write("### Your Weekly Schedule")
st.dataframe(df)

# Download the updated schedule
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download Schedule as CSV",
    data=csv,
    file_name='weekly_schedule.csv',
    mime='text/csv',
)
