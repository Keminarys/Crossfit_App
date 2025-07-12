import streamlit as st

def fab_selector():
    st.markdown("""
        <style>
            .fab-container {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .fab-button {
                width: 55px;
                height: 55px;
                border-radius: 50%;
                background: linear-gradient(135deg, #FF6B6B, #F06543);
                color: white;
                font-size: 24px;
                font-weight: bold;
                border: none;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .fab-button:hover {
                transform: scale(1.1);
                box-shadow: 0px 6px 12px rgba(0,0,0,0.4);
            }
        </style>
    """, unsafe_allow_html=True)

    fab_area = st.container()
    with fab_area:
        st.markdown('<div class="fab-container">', unsafe_allow_html=True)
        if st.button("👤", key="fab_profile"):
            st.switch_page(page_key[0])
        if st.button("📊", key="fab_progress"):
            st.switch_page(page_key[1])
        if st.button("📚", key="fab_ressources"):
            st.switch_page(page_key[2])
        if st.button("📅", key="fab_schedule"):
            st.switch_page(page_key[3])
        st.markdown("</div>", unsafe_allow_html=True)



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
