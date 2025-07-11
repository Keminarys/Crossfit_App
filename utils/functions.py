import streamlit as st

def go_home():
    """Creates an anchored, high-energy CrossFit-styled button for navigation."""
    st.markdown("""
        <style>
            .fixed-container {
                position: fixed;
                top: 100px;
                right: 30px;
                z-index: 1000;
            }

            .crossfit-button {
                display: inline-block;
                background: linear-gradient(45deg, #D62828, #E63946); /* Fiery gradient */
                color: white;
                font-size: 12px; /* Made it smaller */
                font-weight: bold;
                font-family: 'Bebas Neue', sans-serif; /* Strong athletic font */
                padding: 7px 16px; /* Adjusted padding */
                border-radius: 5px;
                border: 2px solid black;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
            }

            .crossfit-button:hover {
                background: linear-gradient(45deg, #C70039, #900D0D); /* Darker punch effect */
                box-shadow: 0px 6px 12px rgba(0,0,0,0.5);
                transform: scale(1.05);
            }
        </style>

        <div class="fixed-container">
            <a href="https://https://cflebeausset83.streamlit.app//" target="_self">
                <button class="crossfit-button">🔥 Retour au Menu Principal 🏋️</button>
            </a>
        </div>
    """, unsafe_allow_html=True)
