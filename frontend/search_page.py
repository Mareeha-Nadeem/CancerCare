# import streamlit as st

# def show():
#       # ------- TOP NAV BAR (same as Home page) -------
#     st.markdown("""
#         <style>
#         .hero-nav {
#             display: flex;
#             justify-content: center;
#             gap: 2.5rem;
#             font-size: 0.9rem;
#             margin-bottom: 2.5rem;
#             margin-top: 1rem;
#         }
#         .hero-nav a {
#             text-decoration: none;
#             color: #0076D6;
#             font-weight: 600;
#         }
#         .hero-nav a:hover {
#             color: #FF6B1A;
#         }
#         .hero-nav a.active {
#             color: #FF6B1A;
#         }
#         </style>
#         <div class="hero-nav">
#             <a href="?page=home">HOME</a>
#             <a href="?page=about">ABOUT</a>
#             <a href="?page=search">SEARCH</a>
#             <a href="?page=service">SERVICE</a>
#             <a href="?page=contact">CONTACT</a>
#         </div>
#     """, unsafe_allow_html=True)
#     st.title("Search Page")


# # frontend/search_page.py

# import pandas as pd

# from dsa.patient_dsa import (
#     filter_patients,
#     order_by_priority,
#     order_by_fifo,
#     order_by_lifo,
#     build_id_index,
#     build_age_bst,
# )

# # NOTE:
# # Baad mein yahan backend/database se real patients aayenge.
# # Abhi ke liye ek dummy list rakhi hai taa-ke UI/test ho sake.

# DUMMY_PATIENTS = [
#     {
#         "id": 1,
#         "name": "Ali Raza",
#         "age": 65,
#         "risk_level": "HIGH",
#         "risk_score": 0.92,
#         "created_at": "2025-12-01T10:00:00",
#     },
#     {
#         "id": 2,
#         "name": "Fatima Noor",
#         "age": 45,
#         "risk_level": "MEDIUM",
#         "risk_score": 0.65,
#         "created_at": "2025-12-02T11:15:00",
#     },
#     {
#         "id": 3,
#         "name": "Hamza Khan",
#         "age": 55,
#         "risk_level": "HIGH",
#         "risk_score": 0.88,
#         "created_at": "2025-12-02T09:40:00",
#     },
#     {
#         "id": 4,
#         "name": "Ayesha Malik",
#         "age": 32,
#         "risk_level": "LOW",
#         "risk_score": 0.30,
#         "created_at": "2025-12-01T16:20:00",
#     },
# ]


# def get_all_patients():
#     """
#     Future:
#         - read from database / API.
#     For now:
#         - return dummy list.
#     """
#     return DUMMY_PATIENTS


# def show():
#     # ---------- TOP NAV (same style as others, SEARCH active) ----------
#     st.markdown(
#         """
#         <div class="hero-nav" style="display:flex;justify-content:center;gap:2.5rem;
#              font-size:0.9rem;margin-bottom:2rem;margin-top:1rem;">
#             <a href="?page=home" style="text-decoration:none;color:#0076D6;font-weight:600;">HOME</a>
#             <a href="?page=about" style="text-decoration:none;color:#0076D6;font-weight:600;">ABOUT</a>
#             <a href="?page=search" style="text-decoration:none;color:#FF6B1A;font-weight:600;">SEARCH</a>
#             <a href="?page=service" style="text-decoration:none;color:#0076D6;font-weight:600;">SERVICE</a>
#             <a href="?page=contact" style="text-decoration:none;color:#0076D6;font-weight:600;">CONTACT</a>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.title("Search Patients (DSA Powered)")

#     patients = get_all_patients()
#     if not patients:
#         st.info("No patients yet. They will appear here after ML prediction.")
#         return

#     ages = [int(p["age"]) for p in patients]
#     min_age, max_age = min(ages), max(ages)

#     # ---------- FILTERS ----------

#     col1, col2 = st.columns(2)

#     with col1:
#         age_range = st.slider(
#             "Age range",
#             min_value=min_age,
#             max_value=max_age,
#             value=(min_age, max_age),
#             step=1,
#         )

#         risk_levels = st.multiselect(
#             "Risk levels",
#             ["HIGH", "MEDIUM", "LOW"],
#             default=["HIGH", "MEDIUM", "LOW"],
#         )

#     with col2:
#         name_query = st.text_input("Search by patient name", "")
#         order_mode = st.selectbox(
#             "Order by (which DSA?)",
#             [
#                 "Triage priority (Priority Queue)",
#                 "Arrival time (FIFO Queue)",
#                 "Recently added (LIFO Stack)",
#             ],
#         )

#     # Extra: show which DSAs are being used (for teacher)
#     with st.expander("Which DSA is used here?"):
#         if order_mode.startswith("Triage"):
#             st.markdown(
#                 "- **Priority Queue (max-heap)** is used to keep HIGH risk and older "
#                 "patients at the top."
#             )
#         elif order_mode.startswith("Arrival"):
#             st.markdown(
#                 "- **Queue (FIFO)** behaviour: first predicted, first in the worklist."
#             )
#         else:
#             st.markdown(
#                 "- **Stack (LIFO)** behaviour: recently added / predicted patients come first."
#             )
#         st.markdown(
#             "- Filtering uses simple iterations, but we also build a **BST** index "
#             "for age-based analytics and a **hash map** for O(1) lookup by ID."
#         )

#     # ---------- APPLY FILTER + ORDER WHEN BUTTON CLICKED ----------

#     if st.button("Search"):
#         # 1) Filter
#         filtered = filter_patients(
#             patients=patients,
#             age_range=age_range,
#             allowed_risks={r.upper() for r in risk_levels},
#             name_query=name_query,
#         )

#         if not filtered:
#             st.warning("No patients match your filters.")
#             return

#         # 2) Order using selected DSA
#         if order_mode.startswith("Triage"):
#             ordered = order_by_priority(filtered)
#         elif order_mode.startswith("Arrival"):
#             ordered = order_by_fifo(filtered)
#         else:
#             ordered = order_by_lifo(filtered)

#         # 3) Show table
#         st.subheader("Matching patients")
#         df = pd.DataFrame(ordered)
#         st.dataframe(df, use_container_width=True)

#         # 4) Extra: use hash map index for O(1) lookup by ID
#         st.subheader("Fast lookup by ID (Hashing concept)")
#         id_index = build_id_index(ordered)
#         pid = st.number_input(
#             "Enter a patient ID from the table above:",
#             min_value=min(p["id"] for p in ordered),
#             max_value=max(p["id"] for p in ordered),
#             step=1,
#         )
#         selected = id_index.get(pid)

#         if selected:
#             st.write(f"**Name:** {selected['name']}")
#             st.write(f"**Age:** {selected['age']}")
#             st.write(f"**Risk:** {selected['risk_level']} (score: {selected['risk_score']})")

#             st.info(
#                 "Here we can later show ML-based test & doctor recommendations.\n\n"
#                 "Current version focuses on DSA logic only."
#             )

#         # 5) Extra: Age BST analytics demo
#         st.subheader("Age-wise analytics using BST (demo)")
#         bst = build_age_bst(patients)
#         min_q, max_q = st.slider(
#             "Show count of patients in age range (BST range query)",
#             min_value=min_age,
#             max_value=max_age,
#             value=(50, 70),
#             step=1,
#         )
#         bst_patients = bst.range_query(min_q, max_q)
#         st.write(f"Patients between ages {min_q} and {max_q}: **{len(bst_patients)}**")
# frontend/search_page.py

# import streamlit as st
# import pandas as pd

# # Import DSA helpers from dsa/patient_dsa.py
# from dsa.patient_dsa import (
#     filter_patients,
#     order_by_priority,
#     order_by_fifo,
#     order_by_lifo,
#     build_id_index,
#     build_age_bst,
# )

# # -------------------------------------------------------------------
# # TEMP DATA SOURCE
# # -------------------------------------------------------------------
# # Later you will replace this with real data coming from your database
# # or backend. For now, we keep a dummy list so the page is functional.

# DUMMY_PATIENTS = [
#     {
#         "id": 1,
#         "first_name": "Ali",
#         "last_name": "Raza",
#         "name": "Ali Raza",             # used by filter_patients()
#         "age": 65,
#         "gender": "Male",
#         "risk_level": "HIGH",
#         "risk_score": 0.92,
#         "created_at": "2025-12-01T10:00:00",
#     },
#     {
#         "id": 2,
#         "first_name": "Fatima",
#         "last_name": "Noor",
#         "name": "Fatima Noor",
#         "age": 45,
#         "gender": "Female",
#         "risk_level": "MEDIUM",
#         "risk_score": 0.65,
#         "created_at": "2025-12-02T11:15:00",
#     },
#     {
#         "id": 3,
#         "first_name": "Hamza",
#         "last_name": "Khan",
#         "name": "Hamza Khan",
#         "age": 55,
#         "gender": "Male",
#         "risk_level": "HIGH",
#         "risk_score": 0.88,
#         "created_at": "2025-12-02T09:40:00",
#     },
#     {
#         "id": 4,
#         "first_name": "Ayesha",
#         "last_name": "Malik",
#         "name": "Ayesha Malik",
#         "age": 32,
#         "gender": "Female",
#         "risk_level": "LOW",
#         "risk_score": 0.30,
#         "created_at": "2025-12-01T16:20:00",
#     },
# ]


# def get_all_patients():
#     """
#     Wrapper to get all patients.

#     Later you can connect this to your DB:
#         - read from patients.json
#         - or call an API
#     For now we just return the dummy list above.
#     """
#     return DUMMY_PATIENTS


# # -------------------------------------------------------------------
# # UI: Filter chip row (small cosmetic helper)
# # -------------------------------------------------------------------

# def render_filter_chips(active_filters: dict):
#     """
#     Renders small "chips" showing which filters are currently active,
#     similar to the UI in your screenshot.

#     active_filters example:
#         {
#             "Risk": ["HIGH", "MEDIUM"],
#             "Gender": ["Female"],
#             "Age": "40–70",
#             "Name": "Ali",
#         }
#     """
#     chips_html = []
#     for label, value in active_filters.items():
#         if value is None:
#             continue
#         # value can be list or string
#         if isinstance(value, list):
#             text = ", ".join(map(str, value))
#         else:
#             text = str(value)

#         chip = f"""
#         <span style="
#             display:inline-flex;
#             align-items:center;
#             padding:4px 10px;
#             margin:4px 4px 0 0;
#             background-color:#111827;
#             color:white;
#             border-radius:16px;
#             font-size:11px;
#         ">
#             {label}: {text}
#         </span>
#         """
#         chips_html.append(chip)

#     if chips_html:
#         st.markdown(
#             "<div style='margin-bottom:8px;'>" + "".join(chips_html) + "</div>",
#             unsafe_allow_html=True,
#         )
#     else:
#         st.caption("No filters applied (showing all patients).")


# # -------------------------------------------------------------------
# # MAIN PAGE FUNCTION
# # -------------------------------------------------------------------

# def show():
#     # ---------- TOP NAV (same style, SEARCH active) ----------
#     st.markdown(
#         """
#         <div class="hero-nav" style="display:flex;justify-content:center;gap:2.5rem;
#              font-size:0.9rem;margin-bottom:2rem;margin-top:1rem;">
#             <a href="?page=home" style="text-decoration:none;color:#0076D6;font-weight:600;">HOME</a>
#             <a href="?page=about" style="text-decoration:none;color:#0076D6;font-weight:600;">ABOUT</a>
#             <a href="?page=search" style="text-decoration:none;color:#FF6B1A;font-weight:600;">SEARCH</a>
#             <a href="?page=service" style="text-decoration:none;color:#0076D6;font-weight:600;">SERVICE</a>
#             <a href="?page=contact" style="text-decoration:none;color:#0076D6;font-weight:600;">CONTACT</a>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.title("Patients Search & Filters (DSA Powered)")

#     patients = get_all_patients()
#     if not patients:
#         st.info("No patients yet. They will appear here after predictions are stored.")
#         return

#     # Basic stats
#     st.caption(f"Total patients in system: **{len(patients)}**")

#     ages = [int(p["age"]) for p in patients]
#     min_age, max_age = min(ages), max(ages)

#     # -------------------------------------------------------------------
#     # FILTERS AREA (like top section in your screenshot)
#     # -------------------------------------------------------------------

#     with st.container():
#         c1, c2 = st.columns([3, 2])

#         with c1:
#             st.subheader("Filters")

#             # --- Quick search by ID, first name, last name ---
#             id_input = st.text_input("Patient ID", placeholder="e.g. 101, 202 ...")
#             first_name_input = st.text_input("First name", placeholder="e.g. Ali")
#             last_name_input = st.text_input("Last name", placeholder="e.g. Raza")

#             # --- Risk level filter (multiselect) ---
#             risk_levels = st.multiselect(
#                 "Risk level",
#                 ["HIGH", "MEDIUM", "LOW"],
#                 default=["HIGH", "MEDIUM", "LOW"],  # default = show all
#             )

#             # --- Gender filter ---
#             genders = st.multiselect(
#                 "Gender",
#                 ["Male", "Female", "Other"],
#                 default=["Male", "Female", "Other"],
#             )

#             # --- Age range slider ---
#             age_range = st.slider(
#                 "Age range",
#                 min_value=min_age,
#                 max_value=max_age,
#                 value=(min_age, max_age),
#                 step=1,
#             )

#             # Clear filters button (resets text inputs only)
#             if st.button("Clear name / ID filters"):
#                 # NOTE: Streamlit cannot directly clear text inputs, this is just
#                 # a UI label. In a real app you might use session_state.
#                 st.info("To clear text fields, delete text manually for now.")

#         with c2:
#             st.subheader("Sort / Ordering")

#             # --- Ordering mode -> which DSA is used ---
#             order_mode = st.selectbox(
#                 "Order by (DSA)",
#                 [
#                     "Triage priority (Priority Queue – High risk first)",
#                     "Arrival time (FIFO Queue – first predicted first)",
#                     "Recently added (LIFO Stack – latest first)",
#                 ],
#             )

#             # Optional small explanation
#             with st.expander("Which data structures are used?"):
#                 if order_mode.startswith("Triage"):
#                     st.markdown(
#                         "- Uses a **max-heap priority queue** based on risk level, age, and time."
#                     )
#                 elif order_mode.startswith("Arrival"):
#                     st.markdown(
#                         "- Behaves like a **FIFO queue**, ordered by prediction time."
#                     )
#                 else:
#                     st.markdown(
#                         "- Behaves like a **LIFO stack**, showing most recently added patients first."
#                     )
#                 st.markdown(
#                     "- Filtering also uses a **hash map** for ID lookup and a **BST** "
#                     "for age-based analytics (see bottom of the page)."
#                 )

#     # -------------------------------------------------------------------
#     # APPLY FILTERS + DSA ORDERING
#     # -------------------------------------------------------------------

#     # 1) Start with all patients
#     filtered = patients

#     # 2) Apply gender filter first (simple Python filter)
#     gender_set = set(genders)
#     if gender_set:
#         filtered = [p for p in filtered if p.get("gender") in gender_set]

#     # 3) Use DSA helper to filter age + risk + generic name
#     #    For generic name, we combine first and last names.
#     #    This lets you search e.g. "Ali" or "Raza" as free text.
#     combined_name_query = ""
#     if first_name_input or last_name_input:
#         combined_name_query = (first_name_input + " " + last_name_input).strip()

#     filtered = filter_patients(
#         patients=filtered,
#         age_range=age_range,
#         allowed_risks={r.upper() for r in risk_levels},
#         name_query=combined_name_query,
#     )

#     # 4) Optional: filter by exact ID (using simple check)
#     if id_input.strip():
#         try:
#             pid = int(id_input.strip())
#             filtered = [p for p in filtered if int(p.get("id")) == pid]
#         except ValueError:
#             st.warning("Patient ID must be an integer. Ignoring ID filter.")

#     # 5) Now apply ordering using DSA helpers
#     if order_mode.startswith("Triage"):
#         ordered = order_by_priority(filtered)
#     elif order_mode.startswith("Arrival"):
#         ordered = order_by_fifo(filtered)
#     else:
#         ordered = order_by_lifo(filtered)

#     # -------------------------------------------------------------------
#     # ACTIVE FILTER CHIPS (visual summary)
#     # -------------------------------------------------------------------

#     active_filters = {
#         "Risk": risk_levels if len(risk_levels) != 3 else None,
#         "Gender": genders if len(genders) != 3 else None,
#         "Age": f"{age_range[0]}–{age_range[1]}" if age_range != (min_age, max_age) else None,
#         "ID": id_input or None,
#         "Name": combined_name_query or None,
#     }
#     render_filter_chips(active_filters)

#     # -------------------------------------------------------------------
#     # RESULTS TABLE
#     # -------------------------------------------------------------------

#     st.subheader("Patients list")

#     if not ordered:
#         st.warning("No patients match the current filters.")
#         return

#     # Show all patients (filtered + ordered) in a table
#     df = pd.DataFrame(ordered)
#     # Re-order some columns for nicer display (if they exist)
#     col_order = ["id", "first_name", "last_name", "age", "gender",
#                  "risk_level", "risk_score", "created_at"]
#     df = df[[c for c in col_order if c in df.columns]]
#     st.dataframe(df, use_container_width=True)

#     # -------------------------------------------------------------------
#     # FAST LOOKUP BY ID (Hash map)
#     # -------------------------------------------------------------------

#     st.subheader("Quick details by ID (Hash map lookup)")

#     id_index = build_id_index(ordered)
#     min_id = min(p["id"] for p in ordered)
#     max_id = max(p["id"] for p in ordered)

#     lookup_id = st.number_input(
#         "Enter a patient ID from the table above:",
#         min_value=min_id,
#         max_value=max_id,
#         step=1,
#         value=min_id,
#     )

#     patient = id_index.get(lookup_id)
#     if patient:
#         st.write(f"**Name:** {patient['first_name']} {patient['last_name']}")
#         st.write(f"**Age:** {patient['age']}  |  **Gender:** {patient.get('gender', '-')}")
#         st.write(f"**Risk:** {patient['risk_level']}  (score: {patient['risk_score']})")
#         st.info(
#             "Later we can attach ML-based test & doctor recommendations here.\n"
#             "For now this section demonstrates hash map based O(1) lookup."
#         )

#     # -------------------------------------------------------------------
#     # AGE ANALYTICS (BST DEMO)
#     # -------------------------------------------------------------------

#     st.subheader("Age analytics using BST (extra DSA feature)")

#     bst = build_age_bst(patients)
#     age_q = st.slider(
#         "Show how many patients lie in this age range (BST range query)",
#         min_value=min_age,
#         max_value=max_age,
#         value=(50, 70),
#         step=1,
#     )
#     bst_patients = bst.range_query(age_q[0], age_q[1])
#     st.write(
#         f"Number of patients with age between {age_q[0]} and {age_q[1]} "
#         f"(inclusive): **{len(bst_patients)}**"
#     )
# import streamlit as st

# # ----------------- Dummy data (replace with DB later) -----------------
# PATIENTS = [
#     {
#         "id": 1,
#         "first_name": "Ali",
#         "last_name": "Raza",
#         "age": 65,
#         "gender": "Male",
#         "risk_level": "HIGH",
#         "risk_score": 0.92,
#         "last_prediction": "10-12-2025",
#     },
#     {
#         "id": 2,
#         "first_name": "Fatima",
#         "last_name": "Noor",
#         "age": 45,
#         "gender": "Female",
#         "risk_level": "MEDIUM",
#         "risk_score": 0.65,
#         "last_prediction": "09-12-2025",
#     },
#     {
#         "id": 3,
#         "first_name": "Hamza",
#         "last_name": "Khan",
#         "age": 55,
#         "gender": "Male",
#         "risk_level": "HIGH",
#         "risk_score": 0.88,
#         "last_prediction": "08-12-2025",
#     },
#     {
#         "id": 4,
#         "first_name": "Ayesha",
#         "last_name": "Malik",
#         "age": 32,
#         "gender": "Female",
#         "risk_level": "LOW",
#         "risk_score": 0.30,
#         "last_prediction": "05-12-2025",
#     },
#     {
#         "id": 5,
#         "first_name": "Imran",
#         "last_name": "Sheikh",
#         "age": 60,
#         "gender": "Male",
#         "risk_level": "MEDIUM",
#         "risk_score": 0.71,
#         "last_prediction": "04-12-2025",
#     },
# ]


# def risk_to_status(risk: str):
#     """Map HIGH/MEDIUM/LOW to pill text + css class."""
#     r = (risk or "").upper()
#     if r == "HIGH":
#         return "Critical", "pill-critical"
#     if r == "MEDIUM":
#         return "Moderate", "pill-moderate"
#     return "Stable", "pill-stable"


# def show():
#     pts = PATIENTS
#     total_patients = len(pts)
#     high_count = sum(p["risk_level"].upper() == "HIGH" for p in pts)
#     med_count = sum(p["risk_level"].upper() == "MEDIUM" for p in pts)
#     low_count = sum(p["risk_level"].upper() == "LOW" for p in pts)

#     # ----------------- GLOBAL STYLES (exact dashboard feel) -----------------
#     st.markdown(
#         """
#         <style>
#         [data-testid="stAppViewContainer"] {
#             background-color: #E7EFF5;
#         }
#         section.main > div {
#             padding-top: 0.5rem;
#         }

#         .search-wrapper {
#             max-width: 1050px;
#             margin: 1.5rem auto 2rem auto;
#         }

#         .search-card {
#             background-color: #FFFFFF;
#             border-radius: 18px;
#             padding: 1.4rem 1.6rem 1.6rem 1.6rem;
#             box-shadow: 0 14px 30px rgba(15,23,42,0.10);
#         }

#         .header-row {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             margin-bottom: 1rem;
#         }
#         .header-title {
#             font-size: 0.80rem;
#             text-transform: uppercase;
#             letter-spacing: 0.12em;
#             color: #9CA3AF;
#         }
#         .header-subtitle {
#             font-size: 1.05rem;
#             font-weight: 600;
#             color: #111827;
#         }
#         .header-right {
#             display: flex;
#             align-items: center;
#             gap: 0.75rem;
#             font-size: 0.8rem;
#             color: #6B7280;
#         }
#         .avatar-circle {
#             width: 28px;
#             height: 28px;
#             border-radius: 999px;
#             background: linear-gradient(135deg, #7C3AED, #2563EB);
#         }

#         .stats-row {
#             display: grid;
#             grid-template-columns: repeat(4, minmax(0, 1fr));
#             gap: 0.9rem;
#             margin-bottom: 1.1rem;
#         }
#         .stat-card {
#             background-color: #F9FAFB;
#             border-radius: 12px;
#             padding: 0.65rem 0.8rem;
#             border: 1px solid #E5E7EB;
#         }
#         .stat-label {
#             font-size: 0.7rem;
#             color: #9CA3AF;
#             margin-bottom: 0.25rem;
#         }
#         .stat-value {
#             font-size: 1.3rem;
#             font-weight: 700;
#         }
#         .stat-pill {
#             margin-top: 0.1rem;
#             font-size: 0.7rem;
#             padding: 0.1rem 0.45rem;
#             border-radius: 999px;
#             background-color: #EFF6FF;
#             color: #1D4ED8;
#             display: inline-block;
#         }

#         .toolbar {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             margin: 0.8rem 0 0.6rem 0;
#         }
#         .toolbar-left {
#             display: flex;
#             align-items: center;
#             gap: 0.45rem;
#             flex: 1;
#         }
#         .toolbar-right {
#             display: flex;
#             align-items: center;
#             gap: 0.45rem;
#         }

#         /* Make Streamlit widgets look like toolbar controls */
#         div[data-testid="stTextInput"] {
#             width: 100%;
#         }
#         div[data-testid="stTextInput"] > label {
#             display: none;
#         }
#         div[data-testid="stSelectbox"] > label {
#             display: none;
#         }
#         div[data-testid="stSelectbox"] {
#             min-width: 120px;
#         }

#         .export-btn button {
#             background-color: #2563EB;
#             color: #FFFFFF;
#             border-radius: 999px;
#             padding: 0.35rem 0.9rem;
#             border: none;
#             font-size: 0.8rem;
#             font-weight: 500;
#         }
#         .export-btn button:hover {
#             background-color: #1D4ED8;
#         }

#         .patients-table-container {
#             border-radius: 12px;
#             border: 1px solid #E5E7EB;
#             overflow: hidden;
#         }
#         table.patients-table {
#             width: 100%;
#             border-collapse: collapse;
#             font-size: 0.8rem;
#         }
#         table.patients-table thead {
#             background-color: #F3F4F6;
#         }
#         table.patients-table th,
#         table.patients-table td {
#             padding: 0.55rem 0.7rem;
#             text-align: left;
#             border-bottom: 1px solid #E5E7EB;
#         }
#         table.patients-table th {
#             font-weight: 600;
#             color: #6B7280;
#             font-size: 0.72rem;
#         }
#         table.patients-table tbody tr:hover td {
#             background-color: #F9FAFB;
#             text-color: #111827;
#         }

#         .status-pill {
#             padding: 0.15rem 0.6rem;
#             border-radius: 999px;
#             font-size: 0.7rem;
#             font-weight: 600;
#             display: inline-block;
#         }
#         .pill-stable {
#             background-color: #DCFCE7;
#             color: #166534;
#         }
#         .pill-moderate {
#             background-color: #FEF3C7;
#             color: #92400E;
#         }
#         .pill-critical {
#             background-color: #FEE2E2;
#             color: #B91C1C;
#         }

#         .table-footer {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding-top: 0.4rem;
#             font-size: 0.75rem;
#             color: #9CA3AF;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

#     # ----------------- OUTER WRAPPER + CARD -----------------
#     st.markdown('<div class="search-wrapper"><div class="search-card">', unsafe_allow_html=True)

#     # -------- Header ----------
#     st.markdown(
#         """
#         <div class="header-row">
#             <div>
#                 <div class="header-title">Consultation</div>
#                 <div class="header-subtitle">View and manage your lung cancer patients</div>
#             </div>
#             <div class="header-right">
#                 <span>Dr. Clara Rectified</span>
#                 <div class="avatar-circle"></div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # -------- Stats cards ----------
#     st.markdown(
#         f"""
#         <div class="stats-row">
#             <div class="stat-card">
#                 <div class="stat-label">Total patients</div>
#                 <div class="stat-value">{total_patients}</div>
#                 <div class="stat-pill">All risks</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-label">High-risk patients</div>
#                 <div class="stat-value">{high_count}</div>
#                 <div class="stat-pill">Critical</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-label">Medium-risk patients</div>
#                 <div class="stat-value">{med_count}</div>
#                 <div class="stat-pill">Moderate</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-label">Low-risk patients</div>
#                 <div class="stat-value">{low_count}</div>
#                 <div class="stat-pill">Stable</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # ----------------- TOOLBAR (real widgets) -----------------
#     st.markdown('<div class="toolbar">', unsafe_allow_html=True)

#     st.markdown('<div class="toolbar-left">', unsafe_allow_html=True)
#     search_name = st.text_input("Search patient…", "", key="search_input")
#     risk_filter = st.selectbox(
#         "Risk filter",
#         ["All risks", "High", "Medium", "Low"],
#         index=0,
#         key="risk_filter",
#     )
#     gender_filter = st.selectbox(
#         "Gender filter",
#         ["All genders", "Male", "Female"],
#         index=0,
#         key="gender_filter",
#     )
#     st.markdown("</div>", unsafe_allow_html=True)  # close toolbar-left

#     st.markdown('<div class="toolbar-right export-btn">', unsafe_allow_html=True)
#     st.button("Export", key="export_btn")
#     st.markdown("</div>", unsafe_allow_html=True)  # close toolbar-right

#     st.markdown("</div>", unsafe_allow_html=True)  # close toolbar

#         # ----------------- FILTERING LOGIC -----------------
#     filtered = pts

#     if risk_filter != "All risks":
#         map_risk = {"High": "HIGH", "Medium": "MEDIUM", "Low": "LOW"}
#         target = map_risk[risk_filter]
#         filtered = [p for p in filtered if p["risk_level"].upper() == target]

#     if gender_filter != "All genders":
#         filtered = [p for p in filtered if p["gender"] == gender_filter]

#     q = search_name.lower().strip()
#     if q:
#         filtered = [
#             p
#             for p in filtered
#             if q in (p["first_name"] + " " + p["last_name"]).lower()
#         ]

#     # ----------------- TABLE -----------------
#     if not filtered:
#         st.info("No patients match current filters.")
#     else:
#         rows_html = []
#         for p in filtered:
#             full_name = f"{p['first_name']} {p['last_name']}"
#             status_text, status_class = risk_to_status(p["risk_level"])
#             rows_html.append(
#                 f"<tr>"
#                 f"<td>{p['id']}</td>"
#                 f"<td>{full_name}</td>"
#                 f"<td>{p['last_prediction']}</td>"
#                 f"<td>{p['age']}</td>"
#                 f"<td>{p['gender']}</td>"
#                 f"<td>{p['risk_level'].title()}</td>"
#                 f"<td>{p['risk_score']:.2f}</td>"
#                 f"<td><span class='status-pill {status_class}'>{status_text}</span></td>"
#                 f"</tr>"
#             )

#         table_html = """
# <div class="patients-table-container">
# <table class="patients-table">
#     <thead>
#         <tr>
#             <th>ID</th>
#             <th>Name</th>
#             <th>Last prediction</th>
#             <th>Age</th>
#             <th>Gender</th>
#             <th>Risk level</th>
#             <th>Risk score</th>
#             <th>Status</th>
#         </tr>
#     </thead>
#     <tbody>
# """ + "\n".join(rows_html) + """
#     </tbody>
# </table>
# </div>
# <div class="table-footer">
#     <span>Showing {shown} of {total} patients</span>
#     <span>1  2  3  …  Next ▸</span>
# </div>
# """.format(shown=len(filtered), total=total_patients)

#         st.markdown(table_html, unsafe_allow_html=True)
import streamlit as st
from typing import List, Dict
import sys
sys.path.append('.')  # Add current directory to path

# Import DSA functions
from dsa.patient_dsa import (
    filter_patients,
    order_by_priority,
    order_by_fifo,
    build_id_index,
    build_age_bst,
)

# ----------------- Dummy data (Lung Cancer Risk Prediction) -----------------
PATIENTS = [
    {
        "id": 1,
        "name": "Ali Raza",
        "first_name": "Ali",
        "last_name": "Raza",
        "age": 65,
        "gender": "Male",
        "risk_level": "HIGH",
        "risk_score": 0.92,
        "last_prediction": "10-04-2025",
        "created_at": "2025-04-10T10:30:00",
    },
    {
        "id": 2,
        "name": "Fatima Noor",
        "first_name": "Fatima",
        "last_name": "Noor",
        "age": 45,
        "gender": "Female",
        "risk_level": "MEDIUM",
        "risk_score": 0.65,
        "last_prediction": "09-04-2025",
        "created_at": "2025-04-09T14:20:00",
    },
    {
        "id": 3,
        "name": "Hamza Khan",
        "first_name": "Hamza",
        "last_name": "Khan",
        "age": 55,
        "gender": "Male",
        "risk_level": "HIGH",
        "risk_score": 0.88,
        "last_prediction": "08-04-2025",
        "created_at": "2025-04-08T09:15:00",
    },
    {
        "id": 4,
        "name": "Ayesha Malik",
        "first_name": "Ayesha",
        "last_name": "Malik",
        "age": 32,
        "gender": "Female",
        "risk_level": "LOW",
        "risk_score": 0.30,
        "last_prediction": "05-04-2025",
        "created_at": "2025-04-05T16:45:00",
    },
    {
        "id": 5,
        "name": "Imran Sheikh",
        "first_name": "Imran",
        "last_name": "Sheikh",
        "age": 60,
        "gender": "Male",
        "risk_level": "MEDIUM",
        "risk_score": 0.71,
        "last_prediction": "04-04-2025",
        "created_at": "2025-04-04T11:00:00",
    },
    {
        "id": 6,
        "name": "Zainab Ahmed",
        "first_name": "Zainab",
        "last_name": "Ahmed",
        "age": 48,
        "gender": "Female",
        "risk_level": "LOW",
        "risk_score": 0.28,
        "last_prediction": "03-04-2025",
        "created_at": "2025-04-03T08:30:00",
    },
    {
        "id": 7,
        "name": "Usman Ali",
        "first_name": "Usman",
        "last_name": "Ali",
        "age": 58,
        "gender": "Male",
        "risk_level": "HIGH",
        "risk_score": 0.85,
        "last_prediction": "02-04-2025",
        "created_at": "2025-04-02T13:20:00",
    },
    {
        "id": 8,
        "name": "Sara Khan",
        "first_name": "Sara",
        "last_name": "Khan",
        "age": 42,
        "gender": "Female",
        "risk_level": "MEDIUM",
        "risk_score": 0.58,
        "last_prediction": "01-04-2025",
        "created_at": "2025-04-01T15:10:00",
    },
    {
        "id": 9,
        "name": "Ahmed Hassan",
        "first_name": "Ahmed",
        "last_name": "Hassan",
        "age": 67,
        "gender": "Male",
        "risk_level": "HIGH",
        "risk_score": 0.94,
        "last_prediction": "30-03-2025",
        "created_at": "2025-03-30T10:00:00",
    },
    {
        "id": 10,
        "name": "Maryam Yousaf",
        "first_name": "Maryam",
        "last_name": "Yousaf",
        "age": 38,
        "gender": "Female",
        "risk_level": "LOW",
        "risk_score": 0.25,
        "last_prediction": "29-03-2025",
        "created_at": "2025-03-29T12:30:00",
    },
    {
        "id": 11,
        "name": "Maryam Yousaf",
        "first_name": "Maryam",
        "last_name": "Yousaf",
        "age": 38,
        "gender": "Female",
        "risk_level": "LOW",
        "risk_score": 0.25,
        "last_prediction": "28-03-2025",
        "created_at": "2025-03-28T18:30:00",
    },
]


def risk_to_status(risk: str):
    """Map HIGH/MEDIUM/LOW to display status."""
    r = (risk or "").upper()
    if r == "HIGH":
        return "Critical", "status-critical"
    if r == "MEDIUM":
        return "Mild", "status-mild"
    return "Stable", "status-stable"


def apply_dsa_filters(
    patients: List[Dict],
    search_query: str,
    risk_filter: str,
    gender_filter: str,
    age_min: int,
    age_max: int,
    sort_order: str,
) -> List[Dict]:
    """Apply DSA-based filtering and sorting."""
    
    # Build allowed risks set
    if risk_filter == "All Status":
        allowed_risks = {"HIGH", "MEDIUM", "LOW"}
    else:
        risk_map = {"Stable": "LOW", "Mild": "MEDIUM", "Critical": "HIGH"}
        allowed_risks = {risk_map[risk_filter]}
    
    # Use DSA filter_patients function
    filtered = filter_patients(
        patients=patients,
        age_range=(age_min, age_max),
        allowed_risks=allowed_risks,
        name_query=search_query,
    )
    
    # Filter by gender manually (add to DSA later if needed)
    if gender_filter != "All Gender":
        filtered = [p for p in filtered if p["gender"] == gender_filter]
    
    # Apply sorting using DSA functions
    if sort_order == "Priority (High Risk First)":
        filtered = order_by_priority(filtered)
    elif sort_order == "Oldest First (FIFO)":
        filtered = order_by_fifo(filtered)
    elif sort_order == "Newest First (LIFO)":
        from dsa.patient_dsa import order_by_lifo
        filtered = order_by_lifo(filtered)
    
    return filtered


def search_by_id(patient_id: str) -> Dict:
    """Search patient by ID using hash map (O(1))."""
    if not patient_id:
        return None
    try:
        pid = int(patient_id)
        id_index = build_id_index(PATIENTS)
        return id_index.get(pid)
    except:
        return None


def show():
    # Calculate stats from actual data
    total_patients = 10  # Full database
    high_count = sum(p["risk_level"] == "HIGH" for p in PATIENTS)
    medium_count = sum(p["risk_level"] == "MEDIUM" for p in PATIENTS)
    low_count = sum(p["risk_level"] == "LOW" for p in PATIENTS)

    # ----------------- GLOBAL STYLES -----------------
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #E8EBF0;
        }
        section.main > div {
            padding: 2rem 3rem;
        }

        /* Stats cards */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border-left: 4px solid #E5E7EB;
            position: relative;
        }
        .stat-card.mild {
            border-left-color: #10B981;
        }
        .stat-card.stable {
            border-left-color: #3B82F6;
        }
        .stat-card.critical {
            border-left-color: #EF4444;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.25rem;
        }
        .stat-label {
            font-size: 0.875rem;
            color: #6B7280;
            font-weight: 500;
        }
        .stat-icon {
            position: absolute;
            right: 1.5rem;
            top: 1.5rem;
            font-size: 1.5rem;
            opacity: 0.15;
        }

        /* Main card */
        .main-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }

        /* Toolbar */
        .toolbar {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            align-items: center;
        }

        /* Custom input styling */
        div[data-testid="stTextInput"] > label,
        div[data-testid="stSelectbox"] > label,
        div[data-testid="stNumberInput"] > label {
            display: none;
        }
        
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background-color: #1F2937 !important;
            color: white !important;
            border: 1px solid #374151 !important;
            border-radius: 6px !important;
            padding: 0.6rem 1rem !important;
            font-size: 0.875rem !important;
        }
        
        div[data-testid="stTextInput"] input::placeholder {
            color: #9CA3AF !important;
        }
        
        div[data-testid="stSelectbox"] > div {
            background-color: #1F2937 !important;
            color: white !important;
            border: 1px solid #374151 !important;
            border-radius: 6px !important;
        }
        
        div[data-testid="stSelectbox"] svg {
            fill: white !important;
        }

        /* Settings icon button */
        .settings-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border: 1px solid #D1D5DB;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            color: #6B7280;
            font-size: 1.2rem;
        }

        /* Table */
        .patients-table-wrapper {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 1rem;
        }
        .patients-table {
            width: 100%;
            border-collapse: collapse;
        }
        .patients-table thead {
            background-color: #F9FAFB;
        }
        .patients-table th {
            padding: 0.875rem 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 600;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid #E5E7EB;
        }
        .patients-table td {
            padding: 1rem;
            border-bottom: 1px solid #F3F4F6;
            font-size: 0.875rem;
            color: #374151;
        }
        .patients-table tbody tr:hover {
            background-color: #F9FAFB;
        }

        /* Patient name with avatar */
        .patient-name {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .patient-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.875rem;
            font-weight: 600;
        }

        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.85rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .status-stable {
            background-color: #DBEAFE;
            color: #1E40AF;
        }
        .status-mild {
            background-color: #FEF3C7;
            color: #92400E;
        }
        .status-critical {
            background-color: #FEE2E2;
            color: #991B1B;
        }

        /* Table footer */
        .table-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: #F9FAFB;
            font-size: 0.875rem;
            color: #6B7280;
        }
        .pagination {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------------- STATS CARDS -----------------
    st.markdown(
        f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-number">{total_patients}</div>
                <div class="stat-label">Total patients</div>
            </div>
            <div class="stat-card mild">
                <div class="stat-icon">✓</div>
                <div class="stat-number">{medium_count}</div>
                <div class="stat-label">Mild patients</div>
            </div>
            <div class="stat-card stable">
                <div class="stat-icon">↻</div>
                <div class="stat-number">{low_count}</div>
                <div class="stat-label">Stable patients</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-icon">⚠</div>
                <div class="stat-number">{high_count}</div>
                <div class="stat-label">Critical patients</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------- MAIN CARD -----------------
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # ----------------- TOOLBAR -----------------
    st.markdown('<div class="toolbar">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 0.3])
    
    with col1:
        search_query = st.text_input("", placeholder="🔍 Search patient...", key="search")
    
    with col2:
        status_filter = st.selectbox(
            "", 
            ["All Status", "Stable", "Mild", "Critical"], 
            key="status"
        )
    
    with col3:
        gender_filter = st.selectbox(
            "", 
            ["All Gender", "Male", "Female"], 
            key="gender"
        )
    
    with col4:
        st.markdown('<div class="settings-icon">⚙</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Advanced filters in expander
    with st.expander("🔧 Advanced Filters (DSA Features)"):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            age_min = st.number_input("Min Age", min_value=0, max_value=120, value=0, key="age_min")
            age_max = st.number_input("Max Age", min_value=0, max_value=120, value=120, key="age_max")
        
        with col_b:
            patient_id = st.text_input("Search by ID (Hash Map - O(1))", placeholder="Enter patient ID", key="search_id")
            if patient_id:
                found = search_by_id(patient_id)
                if found:
                    st.success(f"✅ Found: {found['name']} (Age: {found['age']}, Risk: {found['risk_level']})")
                else:
                    st.error("❌ Patient ID not found")
        
        with col_c:
            sort_order = st.selectbox(
                "Sort Order (DSA)",
                ["Priority (High Risk First)", "Oldest First (FIFO)", "Newest First (LIFO)"],
                key="sort"
            )

    # ----------------- APPLY DSA FILTERS -----------------
    filtered = apply_dsa_filters(
        patients=PATIENTS,
        search_query=search_query,
        risk_filter=status_filter,
        gender_filter=gender_filter,
        age_min=age_min,
        age_max=age_max,
        sort_order=sort_order,
    )

    # ----------------- TABLE -----------------
    if not filtered:
        st.info("🔍 No patients match current filters.")
    else:
        rows_html = []
        for p in filtered:
            full_name = p["name"]
            initials = f"{p['first_name'][0]}{p['last_name'][0]}"
            status_text, status_class = risk_to_status(p["risk_level"])
            
            row = f"""<tr>
    <td>
        <div class="patient-name">
            <div class="patient-avatar">{initials}</div>
            <span><strong>{full_name}</strong></span>
        </div>
    </td>
    <td>{p['last_prediction']}</td>
    <td>{p['age']}</td>
    <td>{p['gender']}</td>
    <td>{p['risk_level'].title()}</td>
    <td><strong>{p['risk_score']:.2f}</strong></td>
    <td><span class="status-badge {status_class}">{status_text}</span></td>
    <td style="text-align: center; color: #9CA3AF; cursor: pointer;">⋮</td>
</tr>"""
            rows_html.append(row)

        table_html = f"""<div class="patients-table-wrapper">
<table class="patients-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Last prediction</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Risk level</th>
            <th>Risk score</th>
            <th>Status</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
{''.join(rows_html)}
    </tbody>
</table>
<div class="table-footer">
    <span>Showing 1 to {len(filtered)} of {total_patients} entries</span>
    <div class="pagination">
        <span style="cursor: pointer;">Previous</span>
        <span style="font-weight: 600; color: #2563EB; cursor: pointer;">1</span>
        <span style="cursor: pointer;">2</span>
        <span style="cursor: pointer;">3</span>
        <span>...</span>
        <span style="cursor: pointer;">32</span>
        <span style="cursor: pointer;">Next ▸</span>
    </div>
</div>
</div>"""

        st.markdown(table_html, unsafe_allow_html=True)
        
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Show DSA info footer
    st.markdown("---")
    st.caption("🔬 **DSA Features Active:** Priority Queue (Heap) | Hash Map (O(1) ID Lookup) | BST Age Range | FIFO/LIFO Queues")


if __name__ == "__main__":
    st.set_page_config(
        page_title="CancerCare - Lung Cancer Risk Prediction", 
        layout="wide",
        page_icon="🫁"
    )
    show()
