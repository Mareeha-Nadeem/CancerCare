# # app.py
# import streamlit as st
# from frontend import home_page, prediction_page, patients_page, doctors_page

# st.set_page_config(page_title="CancerCare - Lung Cancer Risk", layout="wide")

# PAGES = {
#     " Home": home_page.show,
#     " Prediction": prediction_page.show,
#     "‍ Patients": patients_page.show,
#     " Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = " Home"

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
#     " Home": home_page.show,
#     " Prediction": prediction_page.show,
#     "‍ Patients": patients_page.show,
#     " Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = " Home"

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
#     " Home": home_page.show,
#     " Prediction": prediction_page.show,
#     "‍ Patients": patients_page.show,
#     " Doctors": doctors_page.show,
# }

# if "current_page" not in st.session_state:
#     st.session_state["current_page"] = " Home"

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
# CRITICAL: Add data_science path BEFORE any other imports
# This allows the ML model to import the feature_engineer module
# import sys
# from pathlib import Path
# PROJECT_ROOT = Path(__file__).parent
# DS_PATH = PROJECT_ROOT / "data_science" / "model_1"
# if str(DS_PATH) not in sys.path:
#     sys.path.insert(0, str(DS_PATH))

# import streamlit as st
# from frontend import home_page, prediction_page, patients_page, doctors_page
# from frontend import about_page, search_page, service_page, contact_page
# from frontend import dashboard_page, lab_tech_page, notifications_page, messaging_page
# from frontend import lab_dashboard, batch_processing, patient_history, reports_page
# from frontend import post_diagnosis_page  # NEW post-diagnosis page
# from frontend import landing_page, auth_page, dashboard_home  # NEW authentication pages
# from core.db_config import init_database
# init_database()

# st.set_page_config(page_title="CancerCare - Lab Technician System", layout="wide")

# # All pages including top-nav pages
# ALL_PAGES = {
#     "landing": landing_page.show,  # NEW: Landing page
#     "auth": auth_page.show,  # NEW: Login/Signup page
#     "dashboard_home": dashboard_home.show,  # NEW: Dashboard home after login
#     "lab_dashboard": lab_dashboard.show,  # Primary page for lab technicians
#     "home": home_page.show,
#     "prediction": prediction_page.show,
#     "batch_processing": batch_processing.show,
#     "patient_history": patient_history.show,
#     "reports": reports_page.show,
#     "patients": patients_page.show,
#     "doctors": doctors_page.show,
#     "dashboard": dashboard_page.show,
#     "lab_tech": lab_tech_page.show,
#     "notifications": notifications_page.show,
#     "messaging": messaging_page.show,
#     "about": about_page.show,
#     "search": search_page.show,
#     "service": service_page.show,
#     "contact": contact_page.show,
#     # "post_diagnosis": post_diagnosis_page.show,  # NEW
# }

# # Only sidebar navigation pages - Lab-focused
# SIDEBAR_PAGES = {
#     "Lab Dashboard": "lab_dashboard",
#     "Single Analysis": "prediction",
#     "Batch Processing": "batch_processing",
#     "Patient History": "patient_history",
#     "Reports & Export": "reports",
#     "Appointments": "lab_tech",
#     "Patient Records": "patients",
#     "Doctors": "doctors",
#     "Search": "search",  # DSA-powered search
   
#     "Analytics": "dashboard",
#     "Notifications": "notifications",
#     "Messages": "messaging",
# }

# def set_page(page_name: str):
#     st.query_params.page = page_name
#     st.rerun()

# def main():
#     # Initialize session state for authentication if not exists
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
    
#     # Check authentication status
#     if not st.session_state.authenticated:
#         # User not authenticated - show landing or auth page
#         current_page = st.session_state.get("page", "landing")
        
#         if current_page in ["landing", "auth"]:
#             try:
#                 ALL_PAGES[current_page]()
#             except Exception as e:
#                 st.error(f"Error loading page: {e}")
#                 # Fallback to landing
#                 st.session_state.page = "landing"
#                 ALL_PAGES["landing"]()
#         else:
#             # Trying to access protected page without auth - redirect to landing
#             st.session_state.page = "landing"
#             ALL_PAGES["landing"]()
#         return
    
#     # User is authenticated - show full application
#     # Default to lab_dashboard for authenticated users
#     current_page = st.query_params.get("page", st.session_state.get("page", "lab_dashboard"))

#     st.sidebar.title("CancerCare Lab")
    
#     # Show user info in sidebar
#     username = st.session_state.get('username', 'User')
#     st.sidebar.success(f"Logged in as: **{username}**")
#     st.sidebar.markdown("---")

#     # Show sidebar navigation
#     if current_page in SIDEBAR_PAGES.values():
#         labels = list(SIDEBAR_PAGES.keys())
#         values = list(SIDEBAR_PAGES.values())

#         # Select current page
#         try:
#             current_index = values.index(current_page)
#         except ValueError:
#             current_index = 0

#         choice = st.sidebar.radio(
#             "Navigation",
#             labels,
#             index=current_index
#         )

#         selected_page = SIDEBAR_PAGES[choice]

#         # If user changed page
#         if selected_page != current_page:
#             set_page(selected_page)
#             return

#     else:
#         # For other pages
#         st.sidebar.write("Use the top navigation to switch sections.")

#     # Render the current page
#     try:
#         ALL_PAGES[current_page]()
#     except Exception as e:
#         st.error(f"Error loading page: {e}")
#         st.write("Trying to load Dashboard Home...")
#         try:
#             ALL_PAGES["dashboard_home"]()
#         except:
#             st.error("Could not load any page. Please check your installation.")

# if __name__ == "__main__":
#     main()

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DS_PATH = PROJECT_ROOT / "data_science" / "model_1"
if str(DS_PATH) not in sys.path:
    sys.path.insert(0, str(DS_PATH))

import streamlit as st
from frontend import home_page, prediction_page, patients_page, doctors_page
from frontend import about_page, search_page, service_page, contact_page
from frontend import dashboard_page, lab_tech_page, notifications_page, messaging_page
from frontend import lab_dashboard, batch_processing, patient_history, reports_page
from frontend import post_diagnosis_page  # NEW post-diagnosis page
from frontend import landing_page, auth_page, dashboard_home  # NEW authentication pages
from core.db_config import init_database
from core.network_logger import network_logger  # ✅ ADDED

init_database()

st.set_page_config(page_title="CancerCare - Lab Technician System", layout="wide")

# All pages including top-nav pages
ALL_PAGES = {
    "landing": landing_page.show,  # NEW: Landing page
    "auth": auth_page.show,  # NEW: Login/Signup page
    "dashboard_home": dashboard_home.show,  # NEW: Dashboard home after login
    "lab_dashboard": lab_dashboard.show,  # Primary page for lab technicians
    "home": home_page.show,
    "prediction": prediction_page.show,
    "batch_processing": batch_processing.show,
    "patient_history": patient_history.show,
    "reports": reports_page.show,
    "patients": patients_page.show,
    "doctors": doctors_page.show,
    "dashboard": dashboard_page.show,
    "lab_tech": lab_tech_page.show,
    "notifications": notifications_page.show,
    "messaging": messaging_page.show,
    "about": about_page.show,
    "search": search_page.show,
    "service": service_page.show,
    "contact": contact_page.show,
    # "post_diagnosis": post_diagnosis_page.show,  # NEW
}

# Only sidebar navigation pages - Lab-focused
SIDEBAR_PAGES = {
    "Lab Dashboard": "lab_dashboard",
    "Single Analysis": "prediction",
    "Batch Processing": "batch_processing",
    "Patient History": "patient_history",
    "Reports & Export": "reports",
    "Appointments": "lab_tech",
    "Patient Records": "patients",
    "Doctors": "doctors",
    "Search": "search",  # DSA-powered search
    "Analytics": "dashboard",
    "Notifications": "notifications",
    "Messages": "messaging",
}

def set_page(page_name: str):
    st.query_params.page = page_name
    st.rerun()

def main():
    # Initialize session state for authentication if not exists
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Check authentication status
    if not st.session_state.authenticated:
        # User not authenticated - show landing or auth page
        current_page = st.session_state.get("page", "landing")

        if current_page in ["landing", "auth"]:
            try:
                ALL_PAGES[current_page]()
            except Exception as e:
                st.error(f"Error loading page: {e}")
                # Fallback to landing
                st.session_state.page = "landing"
                ALL_PAGES["landing"]()
        else:
            # Trying to access protected page without auth - redirect to landing
            st.session_state.page = "landing"
            ALL_PAGES["landing"]()
        return

    # User is authenticated - show full application
    # Default to lab_dashboard for authenticated users
    current_page = st.query_params.get("page", st.session_state.get("page", "lab_dashboard"))

    st.sidebar.title("CancerCare Lab")

    # Show user info in sidebar
    username = st.session_state.get('username', 'User')
    st.sidebar.success(f"Logged in as: **{username}**")
    st.sidebar.markdown("---")

    # Show sidebar navigation
    if current_page in SIDEBAR_PAGES.values():
        labels = list(SIDEBAR_PAGES.keys())
        values = list(SIDEBAR_PAGES.values())

        # Select current page
        try:
            current_index = values.index(current_page)
        except ValueError:
            current_index = 0

        choice = st.sidebar.radio(
            "Navigation",
            labels,
            index=current_index
        )

        selected_page = SIDEBAR_PAGES[choice]

        # If user changed page
        if selected_page != current_page:
            set_page(selected_page)
            return
    else:
        # For other pages
        st.sidebar.write("Use the top navigation to switch sections.")

    # ✅ Render the current page (with Network Logger stats)
    try:
        start = time.time()

        # Log "request" (simulated for Streamlit pages)
        request_id = network_logger.log_request(
            method="GET",
            endpoint=f"/?page={current_page}",
            client_ip="localhost",
            user_agent="streamlit-client",
            request_size=0
        )

        ALL_PAGES[current_page]()

        # Log success response
        response_time_ms = (time.time() - start) * 1000
        network_logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=0,
            response_time_ms=response_time_ms
        )

    except Exception as e:
        # Log failure response
        try:
            response_time_ms = (time.time() - start) * 1000 if 'start' in locals() else 0
            network_logger.log_response(
                request_id=request_id if 'request_id' in locals() else "REQ-ERROR",
                status_code=500,
                response_size=0,
                response_time_ms=response_time_ms
            )
        except:
            pass

        st.error(f"Error loading page: {e}")
        st.write("Trying to load Dashboard Home...")
        try:
            ALL_PAGES["dashboard_home"]()
        except:
            st.error("Could not load any page. Please check your installation.")

if __name__ == "__main__":
    main()
