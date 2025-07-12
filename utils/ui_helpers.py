import streamlit as st
from typing import List, Tuple

def render_nav_bar(
    tabs: List[Tuple[str, str]],
    default_key: str = None,
    *,
    param_name: str = "tab"
) -> str:
    """
    Renders a horizontal nav bar of red pills via HTML <a> links,
    tracks selection through ?tab=<key> in the URL, and returns
    the current key.

    Args:
      tabs: list of (label, key)
      default_key: which key to pick if none in session or URL
      param_name: query‐string parameter name
    """
    # 1) Parse incoming query‐params
    qp = st.experimental_get_query_params()
    requested = qp.get(param_name, [None])[0]

    # 2) Validate keys
    valid_keys = [key for _, key in tabs]
    if requested in valid_keys:
        st.session_state.current_tab = requested
    elif "current_tab" not in st.session_state:
        st.session_state.current_tab = (
            default_key if default_key in valid_keys else valid_keys[0]
        )

    current = st.session_state.current_tab

    # 3) CSS for our pills
    st.markdown(
        f"""
        <style>
          .navlink {{
            display: inline-block;
            margin-right: 8px;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 500;
            text-decoration: none;
            transition: background-color .2s, color .2s;
          }}
          .navlink.inactive {{
            background-color: #fedcdc;
            color: #9b2226;
          }}
          .navlink.active {{
            background-color: #9b2226;
            color: #ffffff;
          }}
          .navlink:hover {{
            opacity: 0.9;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 4) Build the HTML links
    links = []
    for label, key in tabs:
        cls = "navlink active" if key == current else "navlink inactive"
        links.append(f'<a href="?{param_name}={key}" class="{cls}">{label}</a>')

    # 5) Render them in one line
    st.markdown("".join(links), unsafe_allow_html=True)

    return current
