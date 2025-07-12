# utils/ui_helpers.py

import streamlit as st
from typing import List, Tuple

def render_nav_bar(
    tabs: List[Tuple[str, str]],
    default_key: str = None
) -> str:
    """
    Renders a horizontal nav bar as red rectangles using st.tabs,
    keeps selection in `st.session_state.current_tab`, and returns it.
    
    Args:
      tabs: list of (label, key) for each tab
      default_key: which key to pick on first load
    """
    # 1) Initialize session state
    if "current_tab" not in st.session_state:
        valid_keys = [k for _, k in tabs]
        st.session_state.current_tab = (
            default_key if default_key in valid_keys else valid_keys[0]
        )

    # 2) Inject CSS to turn the default tabs into red pills
    st.markdown(
        """
        <style>
        /* Make all tabs red pills */
        [data-baseweb="tab-list"] button {
          border-radius: 4px !important;
          background-color: #e63946 !important;
          color: white !important;
          padding: 8px 16px !important;
          margin-right: 4px !important;
          font-weight: 500 !important;
        }
        /* Darken the active tab slightly */
        [data-baseweb="tab-list"] button[aria-selected="true"] {
          background-color: #d62828 !important;
        }
        /* Remove that little outline on focus */
        [data-baseweb="tab-list"] button:focus {
          box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 3) Build labels list and render tabs
    labels = [label for label, _ in tabs]
    tab_containers = st.tabs(labels)

    # 4) Only the active tab's block will run—use that to set `current_tab`
    for container, (_, key) in zip(tab_containers, tabs):
        with container:
            st.session_state.current_tab = key

    return st.session_state.current_tab
