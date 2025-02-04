import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

# Get the current date and time
current_date = datetime.now()
current_date = current_date.date()


calendar_options = {"editable": "true", "navLinks": "true","selectable": "true"}
calendar_options = {**calendar_options, "headerToolbar": {"left": "today prev,next", "center": "title"}, "initialDate": current_date}


state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key="daygrid",
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

