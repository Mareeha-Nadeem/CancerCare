# # app.py
# import streamlit as st
# from frontend import home_page, prediction_page, patients_page, doctors_page

# st.set_page_config(page_title="CancerCare - Lung Cancer Risk", layout="wide")

# PAGES = {
#     "🏠 Home": home_page.show,
#     "🧪 Prediction": prediction_page.show,
#     "👨‍⚕️ Patients": patients_page.show,
#     "🏥 Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = "🏠 Home"

# def main():
#     st.sidebar.title("CancerCare")
#     choice = st.sidebar.radio(
#         "Navigation",
#         list(PAGES.keys()),
#         index=list(PAGES.keys()).index(st.session_state["current_page"])
#     )
#     st.session_state["current_page"] = choice
#     PAGES[choice]()

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from frontend import home_page, prediction_page, patients_page, doctors_page
# from frontend import about_page, search_page, service_page, contact_page

# st.set_page_config(page_title="CancerCare - Lung Cancer Risk", layout="wide")

# # Pages NOT shown in sidebar
# HIDDEN_PAGES = {
#     "About": about_page.show,
#     "Search": search_page.show,
#     "Service": service_page.show,
#     "Contact": contact_page.show,
# }

# # Main sidebar pages only
# PAGES = {
#     "🏠 Home": home_page.show,
#     "🧪 Prediction": prediction_page.show,
#     "👨‍⚕️ Patients": patients_page.show,
#     "🏥 Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = "🏠 Home"

# def main():
#     # Sidebar for main pages only
#     st.sidebar.title("CancerCare")
#     choice = st.sidebar.radio(
#         "Navigation",
#         list(PAGES.keys()),
#         index=list(PAGES.keys()).index(st.session_state["current_page"])
#     )

#     st.session_state["current_page"] = choice

#     # Render selected main page
#     PAGES[choice]()

#     # Render hidden pages only when directly selected from banner buttons
#     if st.session_state["current_page"] in HIDDEN_PAGES:
#         HIDDEN_PAGES[st.session_state["current_page"]]()

# if __name__ == "__main__":
#     main()
# app.py
# import streamlit as st
# from frontend import home_page, prediction_page, patients_page, doctors_page

# st.set_page_config(page_title="CancerCare - Lung Cancer Risk", layout="wide")

# PAGES = {
#     "🏠 Home": home_page.show,
#     "🧪 Prediction": prediction_page.show,
#     "👨‍⚕️ Patients": patients_page.show,
#     "🏥 Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = "🏠 Home"

# def main():
#     st.sidebar.title("CancerCare")
#     choice = st.sidebar.radio(
#         "Navigation",
#         list(PAGES.keys()),
#         index=list(PAGES.keys()).index(st.session_state["current_page"])
#     )
#     st.session_state["current_page"] = choice
#     PAGES[choice]()   # call selected page's show()

# if __name__ == "__main__":
#     main()
# app.py
import streamlit as st
from frontend import home_page, prediction_page, patients_page, doctors_page
from frontend import about_page, search_page, service_page, contact_page

st.set_page_config(page_title="CancerCare - Lung Cancer Risk", layout="wide")

# All pages including top-nav pages
ALL_PAGES = {
    "home": home_page.show,
    "prediction": prediction_page.show,
    "patients": patients_page.show,
    "doctors": doctors_page.show,
    "about": about_page.show,
    "search": search_page.show,
    "service": service_page.show,
    "contact": contact_page.show,
}

# Only sidebar navigation pages
SIDEBAR_PAGES = {
    "🏠 Home": "home",
    "🧪 Prediction": "prediction",
    "👨‍⚕️ Patients": "patients",
    "🏥 Doctors": "doctors",
}

def set_page(page_name: str):
    st.query_params.page = page_name
    st.rerun()

def main():
    # abhi current page URL se lo
    current_page = st.query_params.get("page", "home")

    st.sidebar.title("CancerCare")

    # sirf uss waqt sidebar radio chalay jab page sidebar waalon mein se ho
    if current_page in SIDEBAR_PAGES.values():
        labels = list(SIDEBAR_PAGES.keys())
        values = list(SIDEBAR_PAGES.values())

        # jis page pe ho, ussi ko default select karo
        current_index = values.index(current_page)

        choice = st.sidebar.radio(
            "Navigation",
            labels,
            index=current_index
        )

        selected_page = SIDEBAR_PAGES[choice]

        # agar user ne sidebar se page change kiya ho
        if selected_page != current_page:
            set_page(selected_page)
            return  # yahan se rerun hoga

    else:
        # jab ABOUT / SEARCH / SERVICE / CONTACT pe ho,
        # sidebar sirf info show kare, route na badlay
        st.sidebar.write("Use the top navigation above to switch sections.")

    # yahan final page render karo
    ALL_PAGES[current_page]()

if __name__ == "__main__":
    main()
