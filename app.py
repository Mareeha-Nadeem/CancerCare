# app.py
# CRITICAL: Add data_science path BEFORE any other imports
import sys
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
from frontend import post_diagnosis_page
from frontend import landing_page, auth_page, dashboard_home
from frontend.modern_styles import MODERN_CSS

# MUST be the VERY FIRST Streamlit command
st.set_page_config(page_title="CancerCare - Lab Technician System", layout="wide")

# Apply design system
st.markdown(MODERN_CSS, unsafe_allow_html=True)

ALL_PAGES = {
    "landing":        landing_page.show,
    "auth":           auth_page.show,
    "dashboard_home": dashboard_home.show,
    "lab_dashboard":  lab_dashboard.show,
    "home":           home_page.show,
    "prediction":     prediction_page.show,
    "batch_processing": batch_processing.show,
    "patient_history":  patient_history.show,
    "reports":        reports_page.show,
    "patients":       patients_page.show,
    "doctors":        doctors_page.show,
    "dashboard":      dashboard_page.show,
    "lab_tech":       lab_tech_page.show,
    "notifications":  notifications_page.show,
    "messaging":      messaging_page.show,
    "about":          about_page.show,
    "search":         search_page.show,
    "service":        service_page.show,
    "contact":        contact_page.show,
    "post_diagnosis": post_diagnosis_page.show,
}

SIDEBAR_PAGES = {
    "Lab Dashboard":    "lab_dashboard",
    "Single Analysis":  "prediction",
    "Batch Processing": "batch_processing",
    "Patient History":  "patient_history",
    "Reports & Export": "reports",
    "Appointments":     "lab_tech",
    "Patient Records":  "patients",
    "Doctors":          "doctors",
    "Search":           "search",
    "Post-Diagnosis":   "post_diagnosis",
    "Analytics":        "dashboard",
    "Notifications":    "notifications",
    "Messages":         "messaging",
}

def set_page(page_name: str):
    st.session_state.page = page_name
    st.rerun()

def main():
    # Initialise session state defaults
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    # ── Unauthenticated flow ──────────────────────────────────────
    if not st.session_state.authenticated:
        current_page = st.session_state.get("page", "landing")
        if current_page not in ("landing", "auth"):
            st.session_state.page = "landing"
            current_page = "landing"
        try:
            ALL_PAGES[current_page]()
        except Exception as e:
            st.error(f"Error loading page: {e}")
            st.session_state.page = "landing"
            ALL_PAGES["landing"]()
        return

    # ── Authenticated flow ────────────────────────────────────────
    current_page = st.session_state.get("page", "lab_dashboard")

    # Sidebar — logo
    try:
        st.sidebar.image("assets/logo.png", width=100)
    except Exception:
        pass

    st.sidebar.title("CancerCare Lab")

    # User info
    username = st.session_state.get("username", "User")
    role     = st.session_state.get("user_role", "user")
    st.sidebar.success(f"Logged in as: **{username}**")
    st.sidebar.caption(f"Role: {role.title()}")
    st.sidebar.markdown("---")

    # Navigation radio
    if current_page in SIDEBAR_PAGES.values():
        labels = list(SIDEBAR_PAGES.keys())
        values = list(SIDEBAR_PAGES.values())
        try:
            current_index = values.index(current_page)
        except ValueError:
            current_index = 0

        choice = st.sidebar.radio("Navigation", labels, index=current_index)
        selected_page = SIDEBAR_PAGES[choice]

        if selected_page != current_page:
            set_page(selected_page)
            return
    else:
        st.sidebar.info("Use in-page navigation to move between sections.")

    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # Render page
    try:
        ALL_PAGES[current_page]()
    except KeyError:
        st.error(f"Page '{current_page}' not found. Redirecting…")
        set_page("lab_dashboard")
    except Exception as e:
        st.error(f"Error loading page: {e}")
        try:
            ALL_PAGES["dashboard_home"]()
        except Exception:
            st.error("Could not load any page. Please check your installation.")

if __name__ == "__main__":
    main()
