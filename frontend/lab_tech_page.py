"""
Appointments Page — schedules and displays real appointments from the database
"""
import streamlit as st
from datetime import datetime, date, time
from core.services.appointment_service import appointment_service
from core.services.patient_service import patient_service
from core.services.doctor_service import doctor_service


def show():
    st.markdown("""
        <style>
        .stApp {background: linear-gradient(135deg, #F0FDFA 0%, #F0F9FF 100%) !important;}
        .page-header {
            background: rgba(255,255,255,0.7); backdrop-filter: blur(16px);
            border-radius: 16px; padding: 32px; margin-bottom: 24px;
        }
        .appt-card {
            background: var(--bg-surface-elevated); border-radius: 12px; padding: 16px;
            margin: 8px 0; border-left: 4px solid #14B8A6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="page-header">
            <h1 style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#14B8A6,#0D9488);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">
                Appointments
            </h1>
            <p style="color:#64748B;margin-top:8px;">Schedule and manage patient appointments</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Schedule New", "View All"])

    # ── Tab 1: Schedule ────────────────────────────────────────────
    with tab1:
        patients = patient_service.get_all_patients()
        doctors  = doctor_service.get_all_doctors() if hasattr(doctor_service, "get_all_doctors") else []

        if not patients:
            st.warning("No patients in the system. Add patients first via Patient Records.")
            return

        with st.form("schedule_appointment"):
            col1, col2 = st.columns(2)

            with col1:
                patient_options = {f"{p.name} (MRN: {p.mrn})": p.id for p in patients}
                selected_patient_label = st.selectbox("Patient", list(patient_options.keys()))
                patient_id = patient_options[selected_patient_label]

                appt_date = st.date_input("Date", min_value=date.today())
                appt_time = st.time_input("Time", value=time(9, 0))

            with col2:
                if doctors:
                    doctor_options = {f"Dr. {d.name} ({d.specialization or 'General'})": d.id for d in doctors}
                    selected_doctor_label = st.selectbox("Doctor", list(doctor_options.keys()))
                    doctor_id = doctor_options[selected_doctor_label]
                else:
                    st.info("No doctors registered. Doctor field will be optional.")
                    doctor_id = None

                appt_type = st.selectbox("Type", ["Consultation", "Follow-up", "Screening", "Emergency"])
                priority  = st.selectbox("Priority", ["Normal (1)", "High (2)", "Urgent (3)"])
                priority_val = int(priority.split("(")[1].replace(")", ""))

            reason = st.text_area("Reason / Notes", placeholder="Brief description of visit…")

            submitted = st.form_submit_button("Schedule Appointment", use_container_width=True)

        if submitted:
            appt_datetime = datetime.combine(appt_date, appt_time)
            appt_data = {
                "patient_id":        patient_id,
                "doctor_id":         doctor_id,
                "appointment_date":  appt_datetime,
                "reason":            f"[{appt_type}] {reason}",
                "status":            "scheduled",
                "priority":          priority_val,
                "notes":             reason,
            }
            appt, error = appointment_service.create_appointment(appt_data)
            if error:
                st.error(f"Failed to schedule: {error}")
            else:
                st.success(f"Appointment scheduled for **{appt_date}** at **{appt_time.strftime('%H:%M')}**")
                st.balloons()

    # ── Tab 2: View All ────────────────────────────────────────────
    with tab2:
        stats = appointment_service.get_appointment_stats()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total",     stats.get("total", 0))
        c2.metric("Scheduled", stats.get("scheduled", 0))
        c3.metric("Completed", stats.get("completed", 0))
        c4.metric("Cancelled", stats.get("cancelled", 0))

        st.markdown("---")

        appointments = appointment_service.get_all_appointments()
        if not appointments:
            st.info("No appointments yet.")
            return

        for appt in appointments:
            status_color = {
                "scheduled": "#14B8A6",
                "completed": "#10B981",
                "cancelled": "#EF4444",
            }.get(appt.status, "#94A3B8")

            # Safe access to related objects
            patient_name = appt.patient.name if appt.patient else f"Patient #{appt.patient_id}"
            doctor_name  = f"Dr. {appt.doctor.name}" if appt.doctor else "Unassigned"

            st.markdown(f"""
                <div class="appt-card" style="border-left-color:{status_color};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#1F2937;">{patient_name}</strong>
                            <span style="color:#64748B;font-size:14px;margin-left:12px;">{doctor_name}</span>
                        </div>
                        <span style="background:{status_color};color:white;padding:4px 12px;
                              border-radius:99px;font-size:12px;font-weight:600;">
                            {appt.status.upper()}
                        </span>
                    </div>
                    <div style="color:#64748B;font-size:14px;margin-top:8px;">
                        {appt.appointment_date.strftime('%B %d, %Y at %H:%M') if appt.appointment_date else 'N/A'}
                        &nbsp;&nbsp;|&nbsp;&nbsp; Priority: {appt.priority or 1}
                        &nbsp;&nbsp;|&nbsp;&nbsp; {appt.reason or ''}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col_a, col_b, _ = st.columns([1, 1, 5])
            if appt.status == "scheduled":
                if col_a.button("Complete", key=f"complete_{appt.id}"):
                    appointment_service.complete_appointment(appt.id)
                    st.rerun()
                if col_b.button("Cancel", key=f"cancel_{appt.id}"):
                    appointment_service.cancel_appointment(appt.id)
                    st.rerun()
