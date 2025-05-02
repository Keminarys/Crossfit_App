import streamlit as st

def go_home():
    """Creates a top-right anchored button that links to WIP.py"""
    st.markdown("""
        <style>
            .top-right-container {
                position: fixed;
                top: 100px;
                right: 30px;
                z-index: 1000;
            }
            .top-right-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
                text-align: center;
                font-size: 16px;
            }
        </style>
        <div class="top-right-container">
            <a href="WIP.py">
                <button class="top-right-button">Retour au Menu Principal</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

