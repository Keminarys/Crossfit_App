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
    button_html = """
        <style>
            .fixed-button {
                position: fixed;
                top: 100px;
                right: 30px;
                z-index: 1000;
            }
            .fixed-button button {
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
            .fixed-button button:hover {
                background: linear-gradient(45deg, #C70039, #900D0D);
                box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
                transform: scale(1.05);
            }
        </style>
        <div class="fixed-button">
            <button onclick="document.getElementById('switch_page_trigger').click()">🏠 Retour à l'accueil</button>
        </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)
    
    if st.button("Invisible Trigger", key="switch_page_trigger"):
        st.switch_page("WIP.py")


