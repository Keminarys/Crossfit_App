import streamlit as st
from urllib.parse import urlencode

def render_nav_bar():
    # 1) Wide layout + hide default menu/header/footer
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

    # 2) Your pages (label, script-filename)
    pages = [
        ("Votre Profil",  "pages/profiles_page.py"),
        ("Votre Progression",  "pages/progress.py"),
        ("Ressources Technique Crossfit", "pages/ressources.py"),
        ("Programmation",  "pages/scheduleResa.py"),
    ]

    # 3) Grab existing query params & current _script (default to first)
    params = st.query_params.copy()
    default_script = pages[0][1]
    current_script = params.get("_script", [default_script])[0]

    # 4) Build nav links, preserving all params but swapping _script
    links = []
    for label, script in pages:
        new_params = params.copy()
        new_params["_script"] = [script]
        qs = urlencode(new_params, doseq=True)
        cls = "active" if script == current_script else ""
        # add target="_self" to force same‐tab navigation
        href = f"./?{qs}"
        links.append(f"<a class='{cls}' href='{href}' target='_self'>{label}</a>")

    # 5) Render the nav bar
    st.markdown(f"<div class='nav-bar'>{''.join(links)}</div>", unsafe_allow_html=True)

    # 6) If _script changed, trigger a rerun
    if st.query_params.get("_script", [None])[0] != current_script:
        st.experimental_rerun()

