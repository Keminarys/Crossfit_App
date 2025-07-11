import streamlit as st

def create_button_grid_for_week(days: list, mapping: dict) -> str | None:
    cols = st.columns(len(days))
    for i, day in enumerate(days):
        label = f"{mapping[day.strftime('%A')]} {day.strftime('%d')}"
        if cols[i].button(label):
            return mapping[day.strftime('%A')]
    return None
