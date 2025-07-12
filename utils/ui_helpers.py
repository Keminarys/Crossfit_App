import streamlit as st

def render_navbar(pages: list[tuple[str, str]]):
    """
    Renders:
      • A fixed, transparent navbar with centered logo
      • Pill-style horizontal links
      • A “Jump to Top” button that scrolls smoothly
    """
    logo_url = (
        "https://raw.githubusercontent.com/"
        "Keminarys/Crossfit_App/main/LogoCrossfit.jpg"
    )

    # Build link HTML
    links_html = "".join(
        f'<a class="nav-link" href="/{path}" target="_self">{label}</a>'
        for label, path in pages
    )

    st.markdown(
        f'''
        <style>
        /* Ensure app content sits below navbar */
        .block-container {{
            padding-top: 120px;  /* adjust if your logo/nav is taller */
        }}

        /* Fixed, transparent navbar */
        .navbar {{
            position: fixed !important;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: transparent !important;
            padding: 0.5rem 1rem 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: none;
        }}

        /* Logo styling */
        .navbar-logo {{
            height: 80px;
            object-fit: contain;
            margin-bottom: 0.5rem;
        }}

        /* Horizontal pill links */
        .nav-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
        }}
        .nav-link {{
            padding: 8px 20px;
            border-radius: 50px;
            background: #8B0000;
            color: #fff !important;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.2s, transform 0.2s;
        }}
        .nav-link:hover {{
            background: #aa0000;
            transform: scale(1.05);
        }}

        /* Jump-to-top button */
        .jump-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #8B0000;
            color: #fff;
            border: none;
            padding: 10px 14px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 14px;
            opacity: 0.7;
            transition: opacity 0.2s;
            z-index: 999;
        }}
        .jump-top:hover {{
            opacity: 1;
        }}
        </style>

        <!-- Anchor at top -->
        <div id="top"></div>

        <!-- Navbar -->
        <div class="navbar">
          <img src="{logo_url}" class="navbar-logo" alt="Crossfit Logo">
          <div class="nav-links">{links_html}</div>
        </div>

        <!-- Jump to top -->
        <a href="#top" class="jump-top">↑ Top</a>
        ''',
        unsafe_allow_html=True,
    )



# import streamlit as st

# def render_page_links(pages: list[tuple[str, str]]):
#     st.markdown(
#         """
#         <style>
#         /* Reset default margins */
#         .topbar-wrapper {
#             margin: 0;
#             padding: 0;
#         }

#         /* Navbar container */
#         .navbar {
#             background-color: #1f1f1f;
#             padding: 10px 20px;
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             box-shadow: 0 4px 8px rgba(0,0,0,0.3);
#             margin-bottom: 2rem;
#             border-bottom: 2px solid #8B0000;
#         }

#         /* Logo styling */
#         .navbar-logo {
#             max-height: 90px;
#             margin-bottom: 10px;
#         }

#         /* Pills container in row */
#         .nav-links {
#             display: flex;
#             gap: 18px;
#             flex-wrap: wrap;
#             justify-content: center;
#         }

#         /* Stylish pill buttons */
#         .nav-button {
#             background-color: #8B0000;
#             color: white;
#             padding: 10px 24px;
#             border-radius: 999px;
#             font-weight: bold;
#             text-decoration: none;
#             font-size: 16px;
#             transition: all 0.2s ease-in-out;
#         }

#         .nav-button:hover {
#             background-color: #aa0000;
#             transform: scale(1.05);
#         }
#         </style>

#         <div class="navbar">
#             <img src="https://raw.githubusercontent.com/Keminarys/Crossfit_App/main/LogoCrossfit.jpg" class="navbar-logo" alt="Crossfit Logo">
#             <div class="nav-links">
#         """,
#         unsafe_allow_html=True,
#     )

#     for label, page_path in pages:
#         st.markdown(
#             f'<a class="nav-button" href="/{page_path}" target="_self">{label}</a>',
#             unsafe_allow_html=True
#         )

#     st.markdown("</div></div>", unsafe_allow_html=True)
