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

    # Add links for pages in the 'pages/' subfolder
    links_html = "".join(
        f'<a class="nav-link" href="/pages/{path}" target="_self">{label}</a>'
        for label, path in pages
    )

    st.markdown(
        f'''
        <style>
        /* Fixed, transparent navbar */
        .navbar {{
            position: static !important;
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
            height: 110px;
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
            bottom: 60px;
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
