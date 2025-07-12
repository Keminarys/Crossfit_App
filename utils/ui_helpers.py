import streamlit as st

def display_card(page_name, page_key):
    button_style = """
        <style>
            div.stButton > button {
                background: linear-gradient(45deg, #D62828, #E63946); /* Fiery gradient */
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Bebas Neue', sans-serif; /* Strong athletic font */
                padding: 35px;
                border-radius: 15px;
                border: 2px solid black;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0px 5px 10px rgba(0,0,0,0.4);
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background: linear-gradient(45deg, #C70039, #900D0D); /* Darker punch effect */
                box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
                transform: scale(1.05);
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    if st.button(page_name, key=page_key):
        st.switch_page(page_key)

import streamlit as st

def render_nav_bar():
    # 1. Wide layout & hide default Streamlit chrome
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
            #MainMenu, header, footer { visibility: hidden; }
            .nav-bar {
              display: flex;
              justify-content: center;
              gap: 1.5rem;
              background: #f8f9fc;
              padding: 0.75rem 0;
              margin-bottom: 1.5rem;
            }
            .nav-bar a {
              color: #333;
              font-weight: 500;
              text-decoration: none;
              padding: 0.5rem 1rem;
              border-radius: 0.5rem;
              transition: background 0.15s, color 0.15s;
            }
            .nav-bar a:hover {
              background: #e2e6ea;
            }
            .nav-bar a.active {
              background: #1f77b4;
              color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. Define your pages (label, script-filename)
    pages = [
        ("Votre Profil",  "pages/profiles_page.py"),
        ("Votre Progression",  "pages/progress.py"),
        ("Ressources Technique Crossfit", "pages/ressources.py"),
        ("Programmation",  "pages/scheduleResa.py"),
    ]

    # 3. Read current _script from URL (defaults to first page)
    params = st.query_params
    default_script = pages[0][1]
    current_script = params.get("_script", default_script)

    # 4. Build nav links
    links = []
    for label, script in pages:
        cls = "active" if script == current_script else ""
        # Clicking this link reloads the app with ?_script=that_script
        href = f"?_script={script}"
        links.append(f"<a class='{cls}' href='{href}'>{label}</a>")

    # 5. Render the bar
    st.markdown(f"<div class='nav-bar'>{''.join(links)}</div>", unsafe_allow_html=True)

    # 6. Detect a change in ?_script and rerun
    new_script = st.query_params.get("_script")
    if new_script and new_script != current_script:
        st.experimental_rerun()
