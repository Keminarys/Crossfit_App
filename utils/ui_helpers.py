import streamlit as st

def render_page_links(pages: list[tuple[str, str]], *, container_style: str = ""):
    """
    Renders stylish red pill-style page navigation using HTML <a> links.

    Args:
      pages: List of (label, page_path) tuples.
      container_style: Optional CSS for layout container.
    """
    st.markdown(
        f"""
        <style>
        .pill-container {{
            {container_style}
            margin-bottom: 1rem;
        }}
        .pill-button {{
            display: inline-block;
            margin-right: 8px;
            background-color: #fedcdc;
            color: #9b2226;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 500;
            text-decoration: none;
            transition: background-color .2s, color .2s;
        }}
        .pill-button:hover {{
            background-color: #9b2226;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pill-container">', unsafe_allow_html=True)
    for label, page_path in pages:
        st.markdown(
            f'<a class="pill-button" href="/{page_path}" target="_self">{label}</a>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
