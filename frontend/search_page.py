import streamlit as st

def show():
      # ------- TOP NAV BAR (same as Home page) -------
    st.markdown("""
        <style>
        .hero-nav {
            display: flex;
            justify-content: center;
            gap: 2.5rem;
            font-size: 0.9rem;
            margin-bottom: 2.5rem;
            margin-top: 1rem;
        }
        .hero-nav a {
            text-decoration: none;
            color: #0076D6;
            font-weight: 600;
        }
        .hero-nav a:hover {
            color: #FF6B1A;
        }
        .hero-nav a.active {
            color: #FF6B1A;
        }
        </style>
        <div class="hero-nav">
            <a href="?page=home">HOME</a>
            <a href="?page=about">ABOUT</a>
            <a href="?page=search">SEARCH</a>
            <a href="?page=service">SERVICE</a>
            <a href="?page=contact">CONTACT</a>
        </div>
    """, unsafe_allow_html=True)
    st.title("Search Page")
