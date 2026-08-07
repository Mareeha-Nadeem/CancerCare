"""
Doctors Directory - Advanced with Add/Edit
"""
import streamlit as st
from datetime import datetime
import json
from pathlib import Path


# Simple storage for doctors (you can replace with database)
DOCTORS_FILE = Path("data/doctors.json")
DOCTORS_FILE.parent.mkdir(exist_ok=True)


def load_doctors():
    """Load doctors from file"""
    if DOCTORS_FILE.exists():
        with open(DOCTORS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_doctors(doctors):
    """Save doctors to file"""
    with open(DOCTORS_FILE, 'w') as f:
        json.dump(doctors, f, indent=2)


def show():
    st.markdown("""
        <style>
        /* FORCE HIDE THE ICON TEXT */
        /* This targets the span that contains the icon name and makes it transparent */
        [data-testid="stExpander"] svg + span, 
        .st-ae span {
            font-size: 0 !important;
            visibility: hidden !important;
            display: none !important;
        }

        /* ENSURE THE ACTUAL SVG ICON REMAINS VISIBLE */
        [data-testid="stExpander"] svg {
            visibility: visible !important;
            display: block !important;
        }

        /* Your existing styling */
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .doctor-card {
            background: var(--bg-surface-elevated); border-radius: 12px; padding: 20px; margin: 12px 0;
            border: 1px solid #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)

    
    
    st.markdown("""
        <div class="page-header">
            <h1 style="font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Doctors Directory
            </h1>
            <p style="color: var(--text-muted); margin-top: 8px;">Manage medical staff and specialists</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load doctors
    doctors = load_doctors()
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["👨‍All Doctors", "➕ Add Doctor"])
    
    with tab1:
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("Search doctors", placeholder="Name or specialty...")
        with col2:
            specialty_filter = st.selectbox("Filter by Specialty", 
                                          ["All"] + list(set(d.get('specialty', 'General') for d in doctors)))
        
        # Filter doctors
        filtered_doctors = doctors
        if search:
            filtered_doctors = [d for d in filtered_doctors 
                              if search.lower() in d.get('name', '').lower() or 
                                 search.lower() in d.get('specialty', '').lower()]
        
        if specialty_filter != "All":
            filtered_doctors = [d for d in filtered_doctors 
                              if d.get('specialty') == specialty_filter]
        
        st.info(f"👨‍**{len(filtered_doctors)} doctors** found")
        
        # Display doctors
        if filtered_doctors:
            for idx, doctor in enumerate(filtered_doctors):
                with st.expander(f"👨‍{doctor.get('name', 'Unknown')} - {doctor.get('specialty', 'General')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                            **Name:** {doctor.get('name', 'N/A')}  
                            **Specialty:** {doctor.get('specialty', 'N/A')}  
                            **Experience:** {doctor.get('experience', 'N/A')} years  
                            **Contact:** {doctor.get('contact', 'N/A')}  
                            **Email:** {doctor.get('email', 'N/A')}  
                            **License:** {doctor.get('license', 'N/A')}  
                        """)
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{idx}"):
                            doctors.remove(doctor)
                            save_doctors(doctors)
                            st.rerun()
        else:
            st.warning("No doctors found")
    
    with tab2:
        st.subheader("Add New Doctor")
        
        with st.form("add_doctor"):
            name = st.text_input("Full Name *", placeholder="Dr. John Smith")
            
            col1, col2 = st.columns(2)
            with col1:
                specialty = st.selectbox("Specialty *", 
                    ["Oncology", "Radiology", "Pulmonology", "Pathology", 
                     "Surgery", "Internal Medicine", "General Practice", "Other"])
                experience = st.number_input("Years of Experience *", 0, 50, 5)
            
            with col2:
                license_no = st.text_input("License Number *", placeholder="MED12345")
                contact = st.text_input("Contact Number", placeholder="+1-234-567-8900")
            
            email = st.text_input("Email", placeholder="doctor@hospital.com")
            
            col1, col2 = st.columns(2)
            with col1:
                qualifications = st.text_area("Qualifications", placeholder="MD, PhD in Oncology...")
            with col2:
                notes = st.text_area("Additional Notes", placeholder="Available Mon-Fri...")
            
            submitted = st.form_submit_button("➕ Add Doctor", use_container_width=True)
            
            if submitted:
                if not name or not specialty or not license_no:
                    st.error("Please fill all required fields (*)")
                else:
                    new_doctor = {
                        'id': len(doctors) + 1,
                        'name': name,
                        'specialty': specialty,
                        'experience': experience,
                        'license': license_no,
                        'contact': contact,
                        'email': email,
                        'qualifications': qualifications,
                        'notes': notes,
                        'added_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    doctors.append(new_doctor)
                    save_doctors(doctors)
                    st.success(f"Dr. {name} added successfully!")
                    st.rerun()
    
    # Statistics
    if doctors:
        st.markdown("---")
        st.subheader("Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Doctors", len(doctors))
        
        with col2:
            specialties = set(d.get('specialty', 'Unknown') for d in doctors)
            st.metric("Specialties", len(specialties))
        
        with col3:
            avg_exp = sum(d.get('experience', 0) for d in doctors) / len(doctors)
            st.metric("Avg Experience", f"{avg_exp:.1f} years")
