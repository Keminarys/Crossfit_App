import streamlit as st
from urllib.parse import urlencode

def render_nav_bar():

    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
      #MainMenu, header, footer { visibility: hidden; }
      .nav-bar {
        display: flex;
        justify-content: center;
        gap: 1rem;
        background: #121212;
        padding: .75rem 0;
        margin-bottom: 1.5rem;
      }
      .nav-bar a {
        color: #ddd;
        text-decoration: none;
        font-weight: 500;
        padding: .5rem 1rem;
        border-radius: .5rem;
        transition: background .15s, color .15s;
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


    pages = [
        ("Votre Profil",  "pages/profiles_page.py"),
        ("Votre Progression",  "pages/progress.py"),
        ("Ressources Technique Crossfit", "pages/ressources.py"),
        ("Programmation",  "pages/scheduleResa.py"),
    ]


    raw_qp = st.query_params
    params = {k: v[:] for k, v in raw_qp.items()}
    
    default_script = pages[0][1]
    current_script = params.get("_script", [default_script])[0]


    links = []
    for label, script in pages:
        new_params = params.copy()
        new_params["_script"] = [script]
        qs = urlencode(new_params, doseq=True)
        cls = "active" if script == current_script else ""
        # add target="_self" to force same‐tab navigation
        href = f"./?{qs}"
        links.append(f"<a class='{cls}' href='{href}' target='_self'>{label}</a>")


    st.markdown(f"<div class='nav-bar'>{''.join(links)}</div>", unsafe_allow_html=True)


    if st.query_params.get("_script", [None])[0] != current_script:
        st.rerun()

