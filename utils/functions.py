import streamlit as st

def go_home_():
    """Creates a high-energy CrossFit-styled button for navigation."""
    col1, col2, col3 = st.columns([1, 6, 1])

    with col3:  # Anchoring the button to the right
        st.markdown("""
            <style>
                .crossfit-button {
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
                }

                .crossfit-button:hover {
                    transform: scale(1.05);
                    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
                    background-color: #a50021; /* Slightly darker on hover */
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🔥 Retour au Menu Principal 🏋️"):
            st.switch_page("WIP.py")


def go_home():
    """Creates a high-energy CrossFit-styled button for navigation."""
    col1, col2, col3 = st.columns([1, 6, 1])

    with col3:  # Anchoring the button to the right
        st.markdown("""
            <style>
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
                }

                .crossfit-button:hover {
                    transform: scale(1.05);
                    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
                    background-color: #a50021; /* Slightly darker on hover */
                }
            </style>

            <a href="/WIP">
                <button class="crossfit-button">🔥 Retour au Menu Principal 🏋️</button>
            </a>
        """, unsafe_allow_html=True)
