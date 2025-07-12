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

def render_page_links(pages: list[tuple[str, str]]):
    st.markdown(
        """
        <style>
        /* Reset default margins */
        .topbar-wrapper {
            margin: 0;
            padding: 0;
        }

        /* Navbar container */
        .navbar {
            background-color: #1f1f1f;
            padding: 10px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-bottom: 2rem;
            border-bottom: 2px solid #8B0000;
        }

        /* Logo styling */
        .navbar-logo {
            max-height: 90px;
            margin-bottom: 10px;
        }

        /* Pills container in row */
        .nav-links {
            display: flex;
            gap: 18px;
            flex-wrap: wrap;
            justify-content: center;
        }

        /* Stylish pill buttons */
        .nav-button {
            background-color: #8B0000;
            color: white;
            padding: 10px 24px;
            border-radius: 999px;
            font-weight: bold;
            text-decoration: none;
            font-size: 16px;
            transition: all 0.2s ease-in-out;
        }

        .nav-button:hover {
            background-color: #aa0000;
            transform: scale(1.05);
        }
        </style>

        <div class="navbar">
            <img src="https://raw.githubusercontent.com/Keminarys/Crossfit_App/main/LogoCrossfit.jpg" class="navbar-logo" alt="Crossfit Logo">
            <div class="nav-links">
        """,
        unsafe_allow_html=True,
    )

    for label, page_path in pages:
        st.markdown(
            f'<a class="nav-button" href="/{page_path}" target="_self">{label}</a>',
            unsafe_allow_html=True
        )

    st.markdown("</div></div>", unsafe_allow_html=True)
