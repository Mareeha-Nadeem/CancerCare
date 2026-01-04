"""
CancerCare - Advanced Search Page (Using DSA Algorithms)
Demonstrates real-world application of Data Structures and Algorithms
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
import json
from datetime import datetime

# Import DSA algorithms
sys.path.insert(0, str(Path(__file__).parent.parent / "dsa"))
from patient_dsa import (
    filter_patients,
    order_by_priority,
    order_by_fifo,
    order_by_lifo,
    build_age_bst,
)
from linearsearch import linear_search, binary_search
from sorting import merge_sort

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        
        .search-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d9ff;
            margin-bottom: 2rem;
        }
        
        .page-title {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00d9ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .patient-card {
            background: linear-gradient(135deg, #2a2a3e 0%, #1a1a2e 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #00d9ff;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .patient-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.4);
        }
        
        .dsa-badge {
            background: linear-gradient(135deg, #ff006e 0%, #ffbe0b 100%);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            color: white;
            font-weight: bold;
            display: inline-block;
            margin: 0.2rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #00d9ff 0%, #00ff88 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="search-header">
            <h1 class="page-title"> Advanced Patient Search</h1>
            <p style="color: #b0b0b0;">Using Data Structures & Algorithms for Efficient Search</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get all patients with their latest predictions
    try:
        all_patients = patient_service.get_all_patients()
        
        # Convert to dict format for DSA functions
        patients_data = []
        for patient in all_patients:
            predictions = prediction_service.get_patient_predictions(patient.id)
            
            risk_level = "UNKNOWN"
            confidence = 0.0
            
            if predictions:
                latest = predictions[0]
                risk_level = latest.risk_level.upper()
                confidence = latest.confidence
            
            patients_data.append({
                'id': patient.id,
                'name': patient.name,
                'mrn': patient.mrn,
                'age': patient.age,
                'gender': patient.gender,
                'contact': patient.contact or "",
                'email': patient.email or "",
                'created_at': patient.created_at.isoformat() if patient.created_at else "",
                'risk_level': risk_level,
                'confidence': confidence
            })
        
        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <h3>{len(patients_data)}</h3>
                    <p>Total Patients</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            high_risk = len([p for p in patients_data if p['risk_level'] == 'HIGH'])
            st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, #ff006e 0%, #ff4d4d 100%);">
                    <h3>{high_risk}</h3>
                    <p>High Risk</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            medium_risk = len([p for p in patients_data if p['risk_level'] == 'MEDIUM'])
            st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, #ffbe0b 0%, #ffd60a 100%);">
                    <h3>{medium_risk}</h3>
                    <p>Medium Risk</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            low_risk = len([p for p in patients_data if p['risk_level'] == 'LOW'])
            st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, #00ff88 0%, #00d9ff 100%);">
                    <h3>{low_risk}</h3>
                    <p>Low Risk</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Search and Filter Section
        st.subheader(" Search & Filter Options")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            " Smart Filters", 
            " Direct Search", 
            " Sort & Order", 
            " Advanced (BST)"
        ])
        
        with tab1:
            st.markdown("### Filter Patients (Using DSA Filter Algorithm)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name_query = st.text_input(" Search by Name", placeholder="Enter name...")
                min_age, max_age = st.slider(" Age Range", 0, 120, (0, 120))
            
            with col2:
                risk_options = st.multiselect(
                    " Risk Levels",
                    ["HIGH", "MEDIUM", "LOW", "UNKNOWN"],
                    default=["HIGH", "MEDIUM", "LOW", "UNKNOWN"]
                )
                gender_filter = st.selectbox(" Gender", ["All", "M", "F"])
            
            if st.button(" Apply Filters", type="primary"):
                # Use DSA filter function
                filtered = filter_patients(
                    patients_data,
                    age_range=(min_age, max_age),
                    allowed_risks=set(risk_options),
                    name_query=name_query
                )
                
                # Additional gender filter
                if gender_filter != "All":
                    filtered = [p for p in filtered if p['gender'] == gender_filter]
                
                st.markdown(f"""
                    <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                        <span class="dsa-badge">DSA: Linear Filtering</span>
                        <h4 style="color: #00d9ff;">Found {len(filtered)} patients</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                display_patients(filtered)
        
        with tab2:
            st.markdown("### Direct Search (Binary & Linear Search)")
            
            search_type = st.radio("Search Algorithm", ["Linear Search", "Binary Search (Sorted)"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                search_field = st.selectbox("Search Field", ["name", "mrn", "email"])
            
            with col2:
                search_value = st.text_input("Search Value", placeholder="Enter value...")
            
            if st.button(" Search", type="primary"):
                if search_type == "Linear Search":
                    # Linear search
                    idx, result = linear_search(patients_data, search_field, search_value)
                    
                    if result:
                        st.markdown(f"""
                            <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                                <span class="dsa-badge">DSA: Linear Search O(n)</span>
                                <h4 style="color: #00d9ff;">Found at index: {idx}</h4>
                            </div>
                        """, unsafe_allow_html=True)
                        display_patients([result])
                    else:
                        st.warning("No patient found!")
                
                else:
                    # Binary search (needs sorted array)
                    sorted_patients = sorted(patients_data, key=lambda p: str(p.get(search_field, "")))
                    idx, result = binary_search(sorted_patients, search_field, search_value)
                    
                    if result:
                        st.markdown(f"""
                            <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                                <span class="dsa-badge">DSA: Binary Search O(log n)</span>
                                <h4 style="color: #00d9ff;">Found at index: {idx} (sorted array)</h4>
                            </div>
                        """, unsafe_allow_html=True)
                        display_patients([result])
                    else:
                        st.warning("No patient found!")
        
        with tab3:
            st.markdown("### Sort & Order Patients")
            
            sort_option = st.selectbox(
                "Order By",
                [
                    " Priority (High Risk + Older First)",
                    "⏰ FIFO (First In, First Out)",
                    " LIFO (Last In, First Out)",
                    " Name (Merge Sort)",
                    " Age (Merge Sort)"
                ]
            )
            
            if st.button(" Apply Sorting", type="primary"):
                if "Priority" in sort_option:
                    # Priority Queue (Heap)
                    ordered = order_by_priority(patients_data)
                    st.markdown("""
                        <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                            <span class="dsa-badge">DSA: Priority Queue (Max-Heap)</span>
                            <h4 style="color: #00d9ff;">Patients Ordered by Priority</h4>
                            <p style="color: #888;">High risk + older patients appear first for urgent care</p>
                        </div>
                    """, unsafe_allow_html=True)
                    display_patients(ordered)
                
                elif "FIFO" in sort_option:
                    # FIFO Queue
                    ordered = order_by_fifo(patients_data)
                    st.markdown("""
                        <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                            <span class="dsa-badge">DSA: FIFO Queue</span>
                            <h4 style="color: #00d9ff;">First Predicted, First Seen</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    display_patients(ordered)
                
                elif "LIFO" in sort_option:
                    # LIFO Stack
                    ordered = order_by_lifo(patients_data)
                    st.markdown("""
                        <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                            <span class="dsa-badge">DSA: LIFO Stack</span>
                            <h4 style="color: #00d9ff;">Recently Added Patients First</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    display_patients(ordered)
                
                elif "Name" in sort_option:
                    # Merge Sort by name
                    ordered = merge_sort(patients_data, 'name')
                    st.markdown("""
                        <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                            <span class="dsa-badge">DSA: Merge Sort O(n log n)</span>
                            <h4 style="color: #00d9ff;">Sorted Alphabetically by Name</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    display_patients(ordered)
                
                else:
                    # Merge Sort by age
                    ordered = merge_sort(patients_data, 'age')
                    st.markdown("""
                        <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                            <span class="dsa-badge">DSA: Merge Sort O(n log n)</span>
                            <h4 style="color: #00d9ff;">Sorted by Age</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    display_patients(ordered)
        
        with tab4:
            st.markdown("### Binary Search Tree (Age-Based Query)")
            st.info("BST provides efficient range queries for age-based searches")
            
            col1, col2 = st.columns(2)
            
            with col1:
                bst_min_age = st.number_input("Minimum Age", 0, 120, 40)
            
            with col2:
                bst_max_age = st.number_input("Maximum Age", 0, 120, 70)
            
            if st.button(" Search BST", type="primary"):
                # Build BST and query
                bst = build_age_bst(patients_data)
                results = bst.range_query(bst_min_age, bst_max_age)
                
                st.markdown(f"""
                    <div style="padding: 1rem; background: #1a1a2e; border-radius: 10px; margin: 1rem 0;">
                        <span class="dsa-badge">DSA: Binary Search Tree</span>
                        <h4 style="color: #00d9ff;">Found {len(results)} patients (Age {bst_min_age}-{bst_max_age})</h4>
                        <p style="color: #888;">BST provides O(log n) average-case search complexity</p>
                    </div>
                """, unsafe_allow_html=True)
                
                display_patients(results)
    
    except Exception as e:
        st.error(f"Error loading patients: {e}")
    
    # Back button
    st.markdown("---")
    if st.button(" Back to Dashboard"):
        st.query_params.page = "lab_dashboard"
        st.rerun()


def display_patients(patients):
    """Display patient cards"""
    if not patients:
        st.info("No patients found")
        return
    
    for patient in patients:
        risk_color = {
            'HIGH': '',
            'MEDIUM': '🟡',
            'LOW': '🟢',
            'UNKNOWN': ''
        }
        
        risk_emoji = risk_color.get(patient['risk_level'], '')
        
        with st.expander(f"{risk_emoji} {patient['name']} (MRN: {patient['mrn']}) - {patient['risk_level']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**ID:** {patient['id']}")
                st.write(f"**Age:** {patient['age']}")
                st.write(f"**Gender:** {patient['gender']}")
            
            with col2:
                st.write(f"**Contact:** {patient['contact'] or 'N/A'}")
                st.write(f"**Email:** {patient['email'] or 'N/A'}")
                st.write(f"**Risk:** {patient['risk_level']}")
            
            with col3:
                if patient['confidence'] > 0:
                    st.write(f"**Confidence:** {patient['confidence']:.1%}")
                st.write(f"**Registered:** {patient['created_at'][:10] if patient['created_at'] else 'N/A'}")
