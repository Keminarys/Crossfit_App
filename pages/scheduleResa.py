import streamlit as st
from streamlit_calendar import calendar

# Set up initial events (if any)
initial_events = [
    {"title": "Event 1", "start": "2025-02-03"},
    {"title": "Event 2", "start": "2025-02-06"},
]

# Render the calendar
selected_dates = calendar(
    initial_view="timeGridWeek",  # Set initial view to weekly
    editable=True,  # Enable event editing
    selectable=True,  # Allow date selection
    events=initial_events,  # Pass initial events
)

# Display selected dates or events
if selected_dates:
    st.write("You selected:", selected_dates)

# Handle new events added by clicking on the day
if st.session_state.get('new_event'):
    st.write("New event added:", st.session_state['new_event'])
