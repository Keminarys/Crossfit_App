import streamlit as st
from streamlit_calendar import FullCalendar

# Initialize FullCalendar
calendar = FullCalendar(
    plugins=['dayGrid', 'interaction'],  # Enable dayGrid and interaction plugins
    header={
        'left': 'prev,next today',
        'center': 'title',
        'right': 'dayGridMonth,dayGridWeek,dayGridDay'
    },
    initialView='dayGridWeek',  # Set initial view to weekly
    editable=True,  # Enable event editing
    selectable=True,  # Allow date selection
    selectHelper=True,  # Show a placeholder when selecting a range of dates
    selectMirror=True  # Show the time selections in the background
)

# Render the calendar
selected_dates = calendar.render()

# Display selected dates or events
if selected_dates:
    st.write("You selected:", selected_dates)

# Handle new events added by clicking on the day
if st.session_state.get('new_event'):
    st.write("New event added:", st.session_state['new_event'])
