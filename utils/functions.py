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
    button_html = f"""
        <div style="position: fixed; top: 100px; right: 30px; z-index: 1000;">
            <form action="#" method="post">
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

    if st.button("🏠 Retour à l'accueil", key="WIP.py"):
        st.switch_page(key)


