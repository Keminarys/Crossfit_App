import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()
# Title of the app
st.title("Weekly Schedule")

# Calendar options
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGrid"
    },
    "initialView": "dayGrid",
    "events": [
        {
            "title": "Event 1",
            "start": "2023-02-04",
            "end": "2023-02-05"
        }
    ]
}

# Display the calendar
calendar(events=calendar_options['events'], options=calendar_options, key='daygrid')

# Download the updated schedule
@st.cache_data
def convert_to_csv(events):
    import pandas as pd
    df = pd.DataFrame(events)
    return df.to_csv(index=False).encode('utf-8')

csv = convert_to_csv(calendar_options['events'])

st.download_button(
    label="Download Schedule as CSV",
    data=csv,
    file_name='weekly_schedule.csv',
    mime='text/csv',
)
