import streamlit as st
from pages import profile_page, page1, page2, page3

PAGES = {
    "Profile": profile_page,
    "Page 1": page1,
    "Page 2": page2,
    "Page 3": page3
}

def load_profil(profil_name):
    st.sidebar.write(f"Profile {profil_name} loaded!")

def display_card(page_name):
    st.markdown(f"""
    <a href='/{page_name}' style='text-decoration: none;'>
    <div style='background-color: lightblue; padding: 10px; margin: 10px; border-radius: 5px;'>
    <h2>{page_name}</h2>
    </div>
    </a>
    """, unsafe_allow_html=True)

def main():
    st.sidebar.title("Crossfit App Hub")

    profil_options = ["Profil 1", "Profil 2", "Profil 3"]
    selected_profil = st.sidebar.selectbox("Select a Profil", profil_options)
    load_profil(selected_profil)

    st.sidebar.title("Pages")
    selection = st.sidebar.selectbox("Choose Page", list(PAGES.keys()))

    page = PAGES[selection]
    page.show()

if __name__ == "__main__":
    main()
