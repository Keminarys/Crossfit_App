import streamlit as st
import streamlit.components.v1 as components

def go_home():
    """Creates a top-right anchored button that links to WIP.py"""
    html_code = """
        <style>
            .top-right-button {
                position: fixed;
                top: 100px;
                right: 30px;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
                text-align: center;
            }
        </style>
        <a href="WIP.py">
            <button class="top-right-button">🏠 Retour à l'accueil</button>
        </a>
    """
    components.html(html_code, height=50)

# Call the function in your Streamlit app
go_home()
