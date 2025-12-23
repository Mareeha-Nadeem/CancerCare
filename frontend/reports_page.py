"""
Reports Generator - PDF and Data Export
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.services.patient_service import patient_service
from core.services.prediction_service import prediction_service
from core.services.doctor_service import doctor_service
from core.services.appointment_service import appointment_service
import json

def show():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Reports & Data Export")
    
    # Tabs for different report types
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Summary Reports", "📋 Detailed Export", "📊 Statistics", "⚙️ Custom Report"])
    
    with tab1:
        st.subheader("Generate Summary Reports")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["All Predictions Summary", "High-Risk Patients", "Today's Activity", "Weekly Summary"]
        )
        
        if st.button("📄 Generate Report", type="primary"):
            try:
                predictions = prediction_service.get_all_predictions(limit=1000)
                patients = patient_service.get_all_patients(limit=1000)
                
                if report_type == "All Predictions Summary":
                    data = []
                    for pred in predictions:
                        patient = patient_service.get_patient_by_id(pred.patient_id)
                        if patient:
                            probs = json.loads(pred.probabilities)
                            data.append({
                                'MRN': patient.mrn,
                                'Patient Name': patient.name,
                                'Age': patient.age,
                                'Gender': patient.gender,
                                'Risk Level': pred.risk_level,
                                'Confidence': f"{pred.confidence:.1%}",
                                'Low Risk %': f"{probs.get('Low', 0):.1%}",
                                'Medium Risk %': f"{probs.get('Medium', 0):.1%}",
                                'High Risk %': f"{probs.get('High', 0):.1%}",
                                'Test Date': pred.created_at.strftime('%Y-%m-%d %H:%M')
                            })
                    
                    df = pd.DataFrame(data)
                    
                elif report_type == "High-Risk Patients":
                    data = []
                    for pred in predictions:
                        if pred.risk_level == "High":
                            patient = patient_service.get_patient_by_id(pred.patient_id)
                            if patient:
                                data.append({
                                    'MRN': patient.mrn,
                                    'Name': patient.name,
                                    'Age': patient.age,
                                    'Contact': patient.contact,
                                    'Confidence': f"{pred.confidence:.1%}",
                                    'Test Date': pred.created_at.strftime('%Y-%m-%d')
                                })
                    
                    df = pd.DataFrame(data)
                
                elif report_type == "Today's Activity":
                    today = datetime.now().date()
                    today_preds = [p for p in predictions if p.created_at.date() == today]
                    
                    data = []
                    for pred in today_preds:
                        patient = patient_service.get_patient_by_id(pred.patient_id)
                        if patient:
                            data.append({
                                'Time': pred.created_at.strftime('%H:%M'),
                                'MRN': patient.mrn,
                                'Patient': patient.name,
                                'Risk': pred.risk_level,
                                'Confidence': f"{pred.confidence:.1%}"
                            })
                    
                    df = pd.DataFrame(data)
                
                else:  # Weekly Summary
                    from datetime import timedelta
                    week_ago = datetime.now() - timedelta(days=7)
                    weekly_preds = [p for p in predictions if p.created_at >= week_ago]
                    
                    data = []
                    for pred in weekly_preds:
                        patient = patient_service.get_patient_by_id(pred.patient_id)
                        if patient:
                            data.append({
                                'Date': pred.created_at.strftime('%Y-%m-%d'),
                                'MRN': patient.mrn,
                                'Patient': patient.name,
                                'Risk': pred.risk_level,
                                'Confidence': f"{pred.confidence:.1%}"
                            })
                    
                    df = pd.DataFrame(data)
                
                # Display preview
                st.success(f"✅ Report generated: {len(df)} records")
                st.dataframe(df, use_container_width=True)
                
                # Download options
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "💾 Download CSV",
                        csv,
                        f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    # Excel download requires openpyxl, but we can use CSV as alternative
                    st.download_button(
                        "📊 Download Excel (CSV)",
                        csv,
                        f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        "text/csv",
                        use_container_width=True
                    )
            
            except Exception as e:
                st.error(f"Error generating report: {e}")
    
    with tab2:
        st.subheader("Detailed Data Export")
        
        export_type = st.multiselect(
            "Select Data to Export",
            ["Patients", "Predictions", "Doctors", "Appointments"]
        )
        
        if st.button("📥 Export Selected Data"):
            try:
                all_data = {}
                
                if "Patients" in export_type:
                    patients = patient_service.get_all_patients(limit=10000)
                    all_data['Patients'] = pd.DataFrame([{
                        'ID': p.id,
                        'MRN': p.mrn,
                        'Name': p.name,
                        'Age': p.age,
                        'Gender': p.gender,
                        'Contact': p.contact,
                        'Created': p.created_at.strftime('%Y-%m-%d')
                    } for p in patients])
                
                if "Predictions" in export_type:
                    predictions = prediction_service.get_all_predictions(limit=10000)
                    all_data['Predictions'] = pd.DataFrame([{
                        'ID': p.id,
                        'Patient ID': p.patient_id,
                        'Risk Level': p.risk_level,
                        'Confidence': p.confidence,
                        'Date': p.created_at.strftime('%Y-%m-%d %H:%M')
                    } for p in predictions])
                
                if "Doctors" in export_type:
                    doctors = doctor_service.get_all_doctors()
                    all_data['Doctors'] = pd.DataFrame([{
                        'ID': d.id,
                        'Name': d.name,
                        'Email': d.email,
                        'Specialization': d.specialization,
                        'Phone': d.phone
                    } for d in doctors])
                
                if "Appointments" in export_type:
                    appointments = appointment_service.get_all_appointments(limit=10000)
                    all_data['Appointments'] = pd.DataFrame([{
                        'ID': a.id,
                        'Patient ID': a.patient_id,
                        'Doctor ID': a.doctor_id,
                        'Date': a.appointment_date.strftime('%Y-%m-%d %H:%M'),
                        'Status': a.status,
                        'Priority': a.priority
                    } for a in appointments])
                
                # Show preview of each dataset
                for name, df in all_data.items():
                    st.write(f"**{name}:** {len(df)} records")
                    with st.expander(f"Preview {name}"):
                        st.dataframe(df.head(10), use_container_width=True)
                
                # Combined CSV download
                if all_data:
                    combined_csv = ""
                    for name, df in all_data.items():
                        combined_csv += f"\n\n=== {name} ===\n"
                        combined_csv += df.to_csv(index=False)
                    
                    st.download_button(
                        "💾 Download All Data (CSV)",
                        combined_csv,
                        f"cancercare_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            except Exception as e:
                st.error(f"Export error: {e}")
    
    with tab3:
        st.subheader("System Statistics")
        
        try:
            patients = patient_service.get_all_patients(limit=10000)
            predictions = prediction_service.get_all_predictions(limit=10000)
            risk_dist = prediction_service.get_risk_distribution()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Patients", len(patients))
                st.metric("Total Predictions", len(predictions))
                st.metric("High Risk Cases", risk_dist['counts']['High'])
            
            with col2:
                if predictions:
                    avg_conf = sum(p.confidence for p in predictions) / len(predictions)
                    st.metric("Average Confidence", f"{avg_conf:.1%}")
                
                completion_rate = (len(predictions) / len(patients) * 100) if patients else 0
                st.metric("Completion Rate", f"{completion_rate:.1f}%")
            
            # Risk distribution table
            st.markdown("### Risk Distribution")
            risk_df = pd.DataFrame({
                'Risk Level': list(risk_dist['counts'].keys()),
                'Count': list(risk_dist['counts'].values()),
                'Percentage': [f"{pct}%" for pct in risk_dist['percentages'].values()]
            })
            st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"Error loading statistics: {e}")
    
    with tab4:
        st.subheader("Custom Report Builder")
        
        st.write("Build your own custom report:")
        
        # Date range
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", datetime.now().date())
        
        with col2:
            end_date = st.date_input("End Date", datetime.now().date())
        
        # Filters
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"]
        )
        
        min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.0, 0.05)
        
        if st.button("🔍 Build Custom Report"):
            try:
                predictions = prediction_service.get_all_predictions(limit=10000)
                
                # Apply filters
                filtered = []
                for pred in predictions:
                    # Date filter
                    if not (start_date <= pred.created_at.date() <= end_date):
                        continue
                    
                    # Risk filter
                    if pred.risk_level not in risk_filter:
                        continue
                    
                    # Confidence filter
                    if pred.confidence < min_confidence:
                        continue
                    
                    patient = patient_service.get_patient_by_id(pred.patient_id)
                    if patient:
                        filtered.append({
                            'Date': pred.created_at.strftime('%Y-%m-%d'),
                            'MRN': patient.mrn,
                            'Patient': patient.name,
                            'Age': patient.age,
                            'Risk': pred.risk_level,
                            'Confidence': f"{pred.confidence:.1%}"
                        })
                
                if filtered:
                    df = pd.DataFrame(filtered)
                    st.success(f"✅ Found {len(df)} matching records")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "💾 Download Custom Report",
                        csv,
                        f"custom_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No records match your filters")
            
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Back button
    st.markdown("---")
    if st.button("⬅️ Back to Lab Dashboard"):
        st.query_params.page = "lab_dashboard"
        st.rerun()
