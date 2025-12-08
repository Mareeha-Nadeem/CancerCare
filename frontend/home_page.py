# # frontend/Home.py
# import streamlit as st

# def show():
#     # ---------- GLOBAL STYLING ----------
#     st.markdown("""
#         <style>
#         /* Full blue background */
#         [data-testid="stAppViewContainer"] {
#             background-color: #5EC2FF;
#         }
#         [data-testid="stHeader"] {
#             background: rgba(0,0,0,0);
#         }

#         /* Centered banner card */
#         .hero-wrapper {
#             display: flex;
#             justify-content: center;
#             padding: 3rem 0 4rem 0;
#         }
#         .hero-card {
#             background: #7ED5FF;
#             border-radius: 24px;
#             box-shadow: 0 18px 40px rgba(0,0,0,0.18);
#             padding: 2.5rem 3.5rem 3rem 3.5rem;
#             width: 100%;
#             max-width: 1150px;
#             position: relative;
#         }

#         /* Top title & subtitle */
#         .hero-top-title {
#             text-align: center;
#             font-weight: 800;
#             letter-spacing: 0.14em;
#             font-size: 0.95rem;
#             margin-bottom: 0.1rem;
#         }
#         .hero-top-subtitle {
#             text-align: center;
#             font-size: 1.1rem;
#             margin-bottom: 1.3rem;
#         }

#         /* Navigation row */
#         .hero-nav {
#             display: flex;
#             justify-content: center;
#             gap: 2.5rem;
#             font-size: 0.9rem;
#             margin-bottom: 1.8rem;
#         }
#         .hero-nav a {
#             text-decoration: none;
#             color: #0076D6;
#             font-weight: 600;
#         }
#         .hero-nav a.active {
#             color: #FF6B1A;
#         }

#         /* Social icons at right */
#         # .hero-socials {
#         #     position: absolute;
#         #     right: 2.5rem;
#         #     top: 4.9rem;
#         #     display: flex;
#         #     flex-direction: column;
#         #     gap: 0.6rem;
#         #     font-size: 0.8rem;
#         #     color: #0050A3;
#         # }
#         # .hero-social-circle {
#         #     width: 30px;
#         #     height: 30px;
#         #     border-radius: 50%;
#         #     border: 2px solid #0050A3;
#         #     display: flex;
#         #     align-items: center;
#         #     justify-content: center;
#         #     font-size: 0.7rem;
#         #     background: #7ED5FF;
#         # }

#         /* Main horizontal layout: lungs left, text right */
#         .hero-main {
#             display: flex;
#             align-items: center;
#             gap: 3rem;
#         }
#         .hero-left {
#             flex: 1.15;
#         }
#         .hero-right {
#             flex: 1;
#         }

#         .hero-heading {
#             font-size: 2.8rem;
#             font-weight: 900;
#             color: #0050A3;
#             line-height: 1.1;
#             margin-bottom: 0.7rem;
#         }
#         .hero-subheading {
#             font-weight: 700;
#             color: #FF6B1A;
#             margin-bottom: 0.8rem;
#         }
#         .hero-body {
#             color: #00447A;
#             font-size: 0.95rem;
#             margin-bottom: 0.5rem;
#         }
#         .hero-deadline {
#             color: #0050A3;
#             font-weight: 700;
#             margin-bottom: 1.4rem;
#         }

#         .hero-arrow {
#             text-align: center;
#             font-size: 1.4rem;
#             color: #0050A3;
#             margin-top: 1.3rem;
#         }

#         /* Make CTA button look like orange banner button */
#         div.stButton > button:first-child {
#             background-color: #FF6B1A;
#             color: white;
#             font-weight: 700;
#             border-radius: 999px;
#             padding: 0.6rem 1.9rem;
#             border: none;
#             font-size: 0.9rem;
#         }
#         div.stButton > button:first-child:hover {
#             background-color: #ff8745;
#         }

#         /* Remove Streamlit default padding at top */
#         section.main > div {
#             padding-top: 0rem;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # # ---------- OUTER CARD ----------
#     # st.markdown('<div class="hero-wrapper"><div class="hero-card">', unsafe_allow_html=True)

#     # st.markdown('<div class="hero-top-title">BANNER TEMPLATE</div>', unsafe_allow_html=True)
#     # st.markdown('<div class="hero-top-subtitle">Medical</div>', unsafe_allow_html=True)

#     # nav row (just cosmetic)
#     st.markdown(
#     """
#     <div class="hero-nav">
#         <a href="?page=home">HOME</a>
#         <a href="?page=about">ABOUT</a>
#         <a href="?page=search">SEARCH</a>
#         <a href="?page=service">SERVICE</a>
#         <a href="?page=contact">CONTACT</a>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )
# # --------- ROUTING BASED ON URL QUERY PARAMS ----------
# page = st.query_params.get("page", "home")

# # if user clicked ABOUT / SEARCH / SERVICE / CONTACT → show those pages
# if page == "about":
#     from frontend import about_page
#     about_page.show()
#     st.stop()

# elif page == "search":
#     from frontend import search_page
#     search_page.show()
#     st.stop()

# elif page == "service":
#     from frontend import service_page
#     service_page.show()
#     st.stop()

# elif page == "contact":
#     from frontend import contact_page
#     contact_page.show()
#     st.stop()

# # if none matched → continue and show HOME hero section below  


#     # # social icons on right
#     # st.markdown(
#     #     """
#     #     <div class="hero-socials">
#     #         <div class="hero-social-circle">T</div>
#     #         <div class="hero-social-circle">F</div>
#     #         <div class="hero-social-circle">X</div>
#     #         <div class="hero-social-circle">I</div>
#     #     </div>
#     #     """,
#     #     unsafe_allow_html=True,
#     # )

#     # ---------- MAIN CONTENT: LUNGS LEFT, TEXT RIGHT ----------
#     # we wrap Streamlit columns in a div to keep horizontal layout like the design
#     st.markdown('<div class="hero-main">', unsafe_allow_html=True)
#     col1, col2 = st.columns([1.15, 1])

#     with col1:
#         # lungs placement exactly on left
#         st.image("static/lung.png", use_container_width=True)

#     with col2:
#         st.markdown(
#             '<div class="hero-heading">Stay healthy<br>and strong!</div>',
#             unsafe_allow_html=True,
#         )
#         st.markdown(
#             "<div class='hero-subheading'>It's time to book your specialist visit!</div>",
#             unsafe_allow_html=True,
#         )
#         st.markdown(
#             """
#             <div class='hero-body'>
#             Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
#             tempor incididunt ut labore et dolore magna aliqua.
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         st.markdown(
#             "<div class='hero-deadline'>You have time until 31<sup>st</sup> December</div>",
#             unsafe_allow_html=True,
#         )

#         if st.button("CANCER RISK PREDICTION"):
#             st.session_state["current_page"] = "🧪 Prediction"
#             st.rerun()

#     st.markdown('</div>', unsafe_allow_html=True)  # close hero-main
#     st.markdown('<div class="hero-arrow">⌄</div>', unsafe_allow_html=True)

#     st.markdown('</div></div>', unsafe_allow_html=True)  # close hero-card & wrapper
import streamlit as st

def show():
    # ---------- GLOBAL STYLING ----------
    st.markdown("""
        <style>
        /* Full blue background */
        [data-testid="stAppViewContainer"] {
            background-color: #5EC2FF;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        /* Centered banner card */
        .hero-wrapper {
            display: flex;
            justify-content: center;
            padding: 3rem 0 4rem 0;
        }
        .hero-card {
            background: #7ED5FF;
            border-radius: 24px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.18);
            padding: 2.5rem 3.5rem 3rem 3.5rem;
            width: 100%;
            max-width: 1150px;
            position: relative;
        }

        /* Top title & subtitle */
        .hero-top-title {
            text-align: center;
            font-weight: 800;
            letter-spacing: 0.14em;
            font-size: 0.95rem;
            margin-bottom: 0.1rem;
        }
        .hero-top-subtitle {
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 1.3rem;
        }

        /* Navigation row */
        .hero-nav {
            display: flex;
            justify-content: center;
            gap: 2.5rem;
            font-size: 0.9rem;
            margin-bottom: 1.8rem;
        }
        .hero-nav a {
            text-decoration: none;
            color: #0076D6;
            font-weight: 600;
        }
        .hero-nav a.active {
            color: #FF6B1A;
        }

        /* Main horizontal layout: lungs left, text right */
        .hero-main {
            display: flex;
            align-items: center;
            gap: 3rem;
        }
        .hero-left {
            flex: 1.15;
        }
        .hero-right {
            flex: 1;
        }

        .hero-heading {
            font-size: 2.8rem;
            font-weight: 900;
            color: #0050A3;
            line-height: 1.1;
            margin-bottom: 0.7rem;
        }
        .hero-subheading {
            font-weight: 700;
            color: #FF6B1A;
            margin-bottom: 0.8rem;
        }
        .hero-body {
            color: #00447A;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }
        .hero-deadline {
            color: #0050A3;
            font-weight: 700;
            margin-bottom: 1.4rem;
        }

        .hero-arrow {
            text-align: center;
            font-size: 1.4rem;
            color: #0050A3;
            margin-top: 1.3rem;
        }

        /* Make CTA button look like orange banner button */
        div.stButton > button:first-child {
            background-color: #FF6B1A;
            color: white;
            font-weight: 700;
            border-radius: 999px;
            padding: 0.6rem 1.9rem;
            border: none;
            font-size: 0.9rem;
        }
        div.stButton > button:first-child:hover {
            background-color: #ff8745;
        }

        /* Remove Streamlit default padding at top */
        section.main > div {
            padding-top: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- TOP NAV (same UI) ----------
    st.markdown(
        """
        <div class="hero-nav">
            <a href="?page=home">HOME</a>
            <a href="?page=about">ABOUT</a>
            <a href="?page=search">SEARCH</a>
            <a href="?page=service">SERVICE</a>
            <a href="?page=contact">CONTACT</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- ROUTING BASED ON URL QUERY PARAMS ----------
    page = st.query_params.get("page", "home")

    if page == "about":
        from frontend import about_page
        about_page.show()
        st.stop()

    elif page == "search":
        from frontend import search_page
        search_page.show()
        st.stop()

    elif page == "service":
        from frontend import service_page
        service_page.show()
        st.stop()

    elif page == "contact":
        from frontend import contact_page
        contact_page.show()
        st.stop()

    # Agar upar wali conditions nahi chalin → HOME hero dikhao

    # ---------- MAIN CONTENT: LUNGS LEFT, TEXT RIGHT ----------
    st.markdown('<div class="hero-main">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.15, 1])

    with col1:
        st.image("static/lung.png", use_container_width=True)

    with col2:
        st.markdown(
            '<div class="hero-heading">Stay healthy<br>and strong!</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='hero-subheading'>It's time to book your specialist visit!</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class='hero-body'>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
            tempor incididunt ut labore et dolore magna aliqua.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='hero-deadline'>You have time until 31<sup>st</sup> December</div>",
            unsafe_allow_html=True,
        )

        # 👉 Better: button bhi query param se prediction page khol de
        if st.button("CANCER RISK PREDICTION"):
            st.query_params.page = "prediction"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # close hero-main
    st.markdown('<div class="hero-arrow">⌄</div>', unsafe_allow_html=True)
