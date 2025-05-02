import streamlit as st

def go_home():
    """Creates a high-energy CrossFit-styled button that redirects to an external app."""
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
                background-color: #d90429; /* Bold Red */
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 8px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                border: 3px solid #ffcc00; /* Yellow Border for a strong vibe */
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
            }

            .crossfit-button:hover {
                transform: scale(1.05);
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
                background-color: #a50021; /* Slightly darker on hover */
            }
        </style>

        <div class="fixed-container">
            <a href="https://crossfitapp-5pz3rvpmqbp5nfmo6pkuaq.streamlit.app/" target="_self">
                <button class="crossfit-button">🔥 Retour au Menu Principal 🏋️</button>
            </a>
        </div>
    """, unsafe_allow_html=True)
