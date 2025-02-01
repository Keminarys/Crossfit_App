import streamlit as st

def load_profil(profil_name):
    # Dummy function to represent profile loading
    st.write(f"Profile {profil_name} loaded!")

def display_card(page_name):
    st.markdown(f"""
    <a href='/{page_name}' style='text-decoration: none;'>
    <div style='background-color: lightblue; padding: 10px; margin: 10px; border-radius: 5px;'>
    <h2>{page_name}</h2>
    </div>
    </a>
    """, unsafe_allow_html=True)

def main():
    st.title("Crossfit App Hub")

    profil_options = ["Profil 1", "Profil 2", "Profil 3"]
    selected_profil = st.selectbox("Select a Profil", profil_options)
    load_profil(selected_profil)

    st.header("Pages")
    pages = ["Page 1", "Page 2", "Page 3"]
    for page in pages:
        display_card(page)

if __name__ == "__main__":
    main()
