import streamlit as st
from urllib.parse import urlencode

def render_nav_bar(tabs, default_key):
    """
    tabs: list of (label, key)
    default_key: the key to pick if no ?_page=… param is present
    Returns the currently selected key.
    """
    
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
      #MainMenu, header, footer { visibility: hidden; }
      .nav-bar {
        display: flex;
        justify-content: center;
        gap: 1rem;
        background: #121212;
        padding: 0.75rem 0;
        margin-bottom: 1.5rem;
      }
      .nav-bar a {
        color: #ddd;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        transition: background 0.15s, color 0.15s;
      }
      .nav-bar a:hover {
        background: rgba(255,255,255,0.1);
      }
      .nav-bar a.active {
        background: #D62828;
        color: #fff !important;
      }
    </style>
    """, unsafe_allow_html=True)

   
    raw_qp = st.query_params
    params = {k: v[:] for k, v in raw_qp.items()}

    
    current = params.get("_page", [default_key])[0]

   
    links = []
    for label, key in tabs:
        new_params = params.copy()
        new_params["_page"] = [key]
        href = f"./?{urlencode(new_params, doseq=True)}"
        cls  = "active" if key == current else ""
        links.append(f"<a class='{cls}' href='{href}' target='_self'>{label}</a>")

    
    st.markdown(f"<div class='nav-bar'>{''.join(links)}</div>", unsafe_allow_html=True)

    
    if st.query_params.get("_page", [None])[0] != current:
        st.rerun()

    return current
