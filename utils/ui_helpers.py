import streamlit as st
from typing import List, Tuple

def render_nav_bar(
    tabs: List[Tuple[str, str]],
    default_key: str = None,
    *,
    radio_key: str = "nav_radio"
) -> str:
    """
    Display a horizontal navigation bar using st.radio and
    store the current tab in session_state['current_tab'].
    
    Args:
        tabs: List of tuples (label, key).
        default_key: key to select on first run.
        radio_key: unique key for the radio widget.
        
    Returns:
        The key of the currently selected tab.
    """
    # Initialize session state
    if "current_tab" not in st.session_state:
        # fall back to first tab if default_key is not provided or invalid
        valid_keys = [k for _, k in tabs]
        st.session_state.current_tab = default_key if default_key in valid_keys else valid_keys[0]

    # Build mappings
    label_to_key = {label: key for label, key in tabs}
    key_to_label = {key: label for label, key in tabs}

    # Build list of labels in order
    labels = [label for label, _ in tabs]

    # Determine initial index
    current_label = key_to_label[st.session_state.current_tab]
    start_index = labels.index(current_label)

    # Render the horizontal radio bar
    selected_label = st.radio(
        label="",
        options=labels,
        index=start_index,
        horizontal=True,
        key=radio_key,
    )

    # Update session state
    st.session_state.current_tab = label_to_key[selected_label]

    return st.session_state.current_tab
