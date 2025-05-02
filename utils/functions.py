import streamlit as st

def go_home_old():
    button_html = """
        <div style="position: fixed; top: 100px; right: 30px; z-index: 1000;">
            <st.switch_page("WIP.py")>
                <button type="submit"
                    style="background: linear-gradient(45deg, #D62828, #E63946);
                    color: white; font-size: 18px; font-weight: bold;
                    padding: 10px 20px; border-radius: 10px; border: none;
                    cursor: pointer; box-shadow: 0px 5px 10px rgba(0,0,0,0.3);">
                    🏠 Retour à l'accueil
                </button>
            </form>
        </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)

def go_home():
    button_style = """
        <style>
            div.stButton > button {
                background: linear-gradient(45deg, #D62828, #E63946);
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                box-shadow: 0px 5px 10px rgba(0,0,0,0.3);
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background: linear-gradient(45deg, #C70039, #900D0D);
                box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
                transform: scale(1.05);
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    if st.button("🏠 Retour à l'accueil", key="home"):
        st.switch_page("WIP.py")

