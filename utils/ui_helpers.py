# import streamlit as st

# def render_page_links(pages: list[tuple[str, str]], *, container_style: str = ""):
#     st.markdown(
#         f"""
#         <style>
#         .pill-container {{
#             {container_style}
#             margin-bottom: 1rem;
#             display: flex;
#             flex-wrap: wrap;
#             gap: 10px;
#         }}
#         .pill-button {{
#             background-color: #8B0000; /* Dark red */
#             color: white;
#             padding: 10px 22px;
#             border-radius: 20px;
#             font-weight: 600;
#             text-decoration: none;
#             transition: background-color .2s, transform .2s;
#         }}
#         .pill-button:hover {{
#             background-color: #a30000;
#             transform: scale(1.05);
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown('<div class="pill-container">', unsafe_allow_html=True)
#     for label, page_path in pages:
#         st.markdown(
#             f'<a class="pill-button" href="/{page_path}" target="_self">{label}</a>',
#             unsafe_allow_html=True,
#         )
#     st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st

def render_page_links(pages: list[tuple[str, str]], *, container_style: str = ""):
    st.markdown(
        f"""
        <style>
        /* Navigation Bar Styling */
        .navbar {{
            background-color: #8B0000;
            padding: 10px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        }}

        /* Logo Styling */
        .navbar-logo {{
            width: 100px;
            height: auto;
            margin-bottom: 10px;
        }}

        /* Pills Container */
        .nav-links {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }}

        /* Buttons Styling */
        .nav-button {{
            background-color: #8B0000;
            color: white;
            padding: 10px 22px;
            border-radius: 20px;
            font-weight: 600;
            text-decoration: none;
            transition: background-color .2s, transform .2s;
        }}

        .nav-button:hover {{
            background-color: #a30000;
            transform: scale(1.05);
        }}
        </style>

        <div class="navbar">
            <img src="LogoCrossfit.jpg" class="navbar-logo" alt="Crossfit Logo">
            <div class="nav-links">
    """,
        unsafe_allow_html=True
    )

    for label, page_path in pages:
        st.markdown(
            f'<a class="nav-button" href="/{page_path}" target="_self">{label}</a>',
            unsafe_allow_html=True
        )

    st.markdown("</div></div>", unsafe_allow_html=True)
