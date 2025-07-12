import streamlit as st
from typing import List, Tuple

def render_nav_bar(
    tabs: List[Tuple[str, str]],
    default_key: str = None,
    *,
    radio_key: str = "nav_radio"
) -> str:
    """
    Renders a styled horizontal nav bar as red pills using st.radio,
    persists selection in st.session_state.current_tab, and returns it.
    
    Args:
      tabs: list of (label, key)
      default_key: initial key on first load
      radio_key: streamlit widget key
    """
    # 1) Inject CSS to style the radio into red pills
    st.markdown(
        """
        <style>
        /* Container tweaks */
        div[data-baseweb="radio"] {
          padding: 0;
          margin-bottom: 1rem;
        }
        /* Hide the actual circle, only keep the label text */
        div[data-baseweb="radio"] label > span:first-child {
          display: none !important;
        }
        /* Unselected pills */
        div[data-baseweb="radio"] > label {
          display: inline-block !important;
          margin-right: 8px !important;
          background-color: #fedcdc !important;
          color: #9b2226 !important;
          padding: 8px 20px !important;
          border-radius: 4px !important;
          font-weight: 500 !important;
          cursor: pointer;
          transition: background-color .2s, color .2s;
        }
        /* Active pill */
        div[data-baseweb="radio"] > label[data-state="active"] {
          background-color: #9b2226 !important;
          color: #ffffff !important;
        }
        /* Remove focus outline */
        div[data-baseweb="radio"] > label:focus {
          box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2) Initialize session state
    valid_keys = [k for _, k in tabs]
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = (
            default_key if default_key in valid_keys else valid_keys[0]
        )

    # 3) Helpers to map between labels & keys
    label_to_key = {lbl: key for lbl, key in tabs}
    key_to_label = {key: lbl for lbl, key in tabs}
    labels = [lbl for lbl, _ in tabs]

    # 4) Compute the default index
    current_label = key_to_label.get(st.session_state.current_tab, labels[0])
    start_idx = labels.index(current_label)

    # 5) Render horizontal radio and capture selection
    selected_label = st.radio(
        label="",
        options=labels,
        index=start_idx,
        horizontal=True,
        key=radio_key,
    )

    # 6) Update session state & return
    st.session_state.current_tab = label_to_key[selected_label]
    return st.session_state.current_tab
