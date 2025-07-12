import streamlit as st

def render_page_links(pages: list[tuple[str, str]], *, container_style: str = ""):
    st.markdown(
        f"""
        <style>
        .pill-container {{
            {container_style}
            margin-bottom: 1rem;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .pill-button {{
            background-color: #8B0000; /* Dark red */
            color: white;
            padding: 10px 22px;
            border-radius: 20px;
            font-weight: 600;
            text-decoration: none;
            transition: background-color .2s, transform .2s;
        }}
        .pill-button:hover {{
            background-color: #a30000;
            transform: scale(1.05);
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
