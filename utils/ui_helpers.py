# utils/ui_helpers.py

import streamlit as st
from typing import List, Tuple

def render_nav_bar(
    tabs: List[Tuple[str, str]],
    default_key: str = None,
    *,
    radio_key: str = "nav_radio"
) -> str:
    """
    Display a styled horizontal navigation bar using st.radio,
    store the current tab in session_state['current_tab'],
    and return the selected key.
    
    Args:
      tabs: list of (label, key)
      default_key: initial key on first load
      radio_key: unique widget key
    """
    # 1) Inject CSS for pill-style tabs
    st.markdown(
        """
        <style>
          /* Container tweaks */
          div[data-baseweb="radio"] {
            padding: 0;
            margin-bottom: 1rem;
          }
          /* Unselected tab */
          div[data-baseweb="radio"] > label {
            display: inline-block !important;
            margin-right: 12px !important;
            background-color: #f4f1de !important;
            color: #3d405b !important;
            padding: 6px 16px !important;
            border-radius: 20px !important;
            font-weight: 500 !important;
            cursor: pointer;
            transition: background-color .2s, color .2s;
          }
          /* Selected tab */
          div[data-baseweb="radio"] > label[data-state="active"] {
            background-color: #e07a5f !important;
            color: white !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2) Initialize session_state
    if "current_tab" not in st.session_state:
        valid_keys = [k for _, k in tabs]
        st.session_state.current_tab = (
            default_key if default_key in valid_keys else valid_keys[0]
        )

    # 3) Build quick lookup
    label_to_key = {lbl: key for lbl, key in tabs}
    key_to_label = {key: lbl for lbl, key in tabs}
    labels = [lbl for lbl, _ in tabs]

    # 4) Compute starting index
    current_label = key_to_label.get(st.session_state.current_tab, labels[0])
    start_index = labels.index(current_label)

    # 5) Render the radio and capture selection
    selected_label = st.radio(
        label="",
        options=labels,
        index=start_index,
        horizontal=True,
        key=radio_key,
    )

    # 6) Update state & return
    st.session_state.current_tab = label_to_key[selected_label]
    return st.session_state.current_tab
