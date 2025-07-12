# utils/ui_helpers.py
import streamlit as st

def render_navbar(pages: list[tuple[str, str]]):
    """
    Renders a sticky top navbar with:
      - Crossfit logo (centered)
      - One-row pill navigation links
      - Jump-to-top button
    pages: list of (label, page_path) tuples, where page_path is
           the name of your Streamlit page (without .py)
    """
    # Raw GitHub URL for your logo
    logo_url = (
        "https://raw.githubusercontent.com/"
        "Keminarys/Crossfit_App/main/LogoCrossfit.jpg"
    )

    # Build the HTML for the nav links
    links_html = "".join(
        f'<a class="nav-link" href="/{path}" target="_self">{label}</a>'
        for label, path in pages
    )

    # Inject CSS + HTML
    st.markdown(
        f'''
        <style>
        /* ─── Navbar Container ───────────────────────────────────────── */
        .streamlit-container {{
            padding-top: 0 !important;  /* remove Streamlit default gap */
        }}
        .navbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 0.5rem 1rem 1.5rem;
        }}
        
        /* ─── Logo ────────────────────────────────────────────────────── */
        .navbar-logo {{
            display: block;
            margin: 0 auto 0.5rem;
            height: 80px;
            object-fit: contain;
        }}

        /* ─── Links Row ───────────────────────────────────────────────── */
        .nav-links {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
        }}
        .nav-link {{
            display: inline-block;
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

        /* ─── Jump to Top Button ─────────────────────────────────────── */
        .jump-top {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #8B0000;
            color: #fff;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            opacity: 0.7;
            transition: opacity 0.2s;
            z-index: 200;
        }}
        .jump-top:hover {{
            opacity: 1;
        }}
        </style>

        <div class="navbar">
          <img class="navbar-logo" src="{logo_url}" alt="Crossfit Logo">
          <div class="nav-links">
            {links_html}
          </div>
        </div>

        <!-- Jump to Top Button -->
        <button class="jump-top"
                onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
            ↑ Top
        </button>
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
