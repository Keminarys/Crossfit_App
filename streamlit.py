import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa

PAGES = {
    "Profile": profiles_page,
    "Progession": progress,
    "Ressources Technique": ressources,
    "Prog de la semaine": scheduleResa
}

### Setting up the page 

st.set_page_config(layout="wide")
### Function 
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas

def display_card(page_name):
    st.markdown(f"""
    <a href='/{page_name}' style='text-decoration: none;'>
    <div style='background-color: lightblue; padding: 10px; margin: 10px; border-radius: 5px;'>
    <h2>{page_name}</h2>
    </div>
    </a>
    """, unsafe_allow_html=True)

def main():

    df_name = get_df("Profils")
    df_name = df_name[['Name']].dropna()
    
    st.title('Crossfit83 Le Beausset')
    st.divider()
    st.header("Pages")
    pages = PAGES.keys()
    for page in pages:
        display_card(page)

if __name__ == "__main__":
    main()
