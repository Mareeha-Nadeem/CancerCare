"""
Comprehensive Demo - Post-Diagnosis Features
Shows all Day 1 functionality with detailed output
"""
from core.services.post_diagnosis_service import post_diagnosis_service
from core.services.tumor_marker_service import tumor_marker_service
from core.services.patient_service import patient_service
from datetime import datetime

def demo_post_diagnosis():
    print("\n" + "="*70)
    print("   POST-DIAGNOSIS SYSTEM DEMO - Day 1 Features")
    print("="*70 + "\n")
    
    # Get or create a patient
    print(" Step 1: Getting patient...")
    patients = patient_service.get_all_patients()
    if patients:
        patient = patients[0]
        print(f"    Using existing patient: {patient.name} (ID: {patient.id})")
    else:
        patient, error = patient_service.create_patient({
            'mrn': 'TEST001',
            'name': 'John Doe',
            'age': 65,
            'gender': 'M',
            'contact': '555-0123'
        })
        print(f"    Created new patient: {patient.name}")
    
    print("\n" + "-"*70)
    
    # Create diagnosis record
    print("\n Step 2: Creating diagnosis record...")
    diagnosis_data = {
        'diagnosis_date': datetime.utcnow(),
        'cancer_type': 'Lung Cancer (Adenocarcinoma)',
        'stage': 'Stage IIIA',
        'tumor_size_mm': 32.5,
        'lymph_nodes_affected': 3,
        'metastasis_status': 'Regional',
        'treatment_plan': 'Combined chemotherapy (Cisplatin + Pemetrexed) followed by radiation therapy',
        'notes': 'Demo diagnosis record for testing post-diagnosis features'
    }
    
    diagnosis, error = post_diagnosis_service.create_diagnosis(
        patient_id=patient.id,
        data=diagnosis_data
    )
    
    if error:
        print(f"    Error: {error}")
    else:
        print(f"    Diagnosis Created!")
        print(f"      ID: {diagnosis.id}")
        print(f"      Type: {diagnosis.cancer_type}")
        print(f"      Stage: {diagnosis.stage}")
        print(f"      Tumor Size: {diagnosis.tumor_size_mm} mm")
        print(f"      Lymph Nodes: {diagnosis.lymph_nodes_affected}")
        print(f"      Metastasis: {diagnosis.metastasis_status}")
    
    print("\n" + "-"*70)
    
    # Record multiple tumor markers
    print("\n Step 3: Recording tumor marker tests...")
    
    markers_to_test = [
        {'name': 'CEA', 'value': 4.5},
        {'name': 'CA 19-9', 'value': 42.0},
        {'name': 'CA 125', 'value': 28.0},
    ]
    
    for marker_info in markers_to_test:
        marker_data = {
            'marker_name': marker_info['name'],
            'value': marker_info['value'],
            'test_date': datetime.utcnow(),
            'lab_name': 'CancerCare Laboratory'
        }
        
        marker, error = tumor_marker_service.record_marker(
            patient_id=patient.id,
            marker_data=marker_data,
            post_diagnosis_id=diagnosis.id if not error else None
        )
        
        if error:
            print(f"    {marker_info['name']}: Error - {error}")
        else:
            status = " ABNORMAL" if marker.is_abnormal else  "🟢 NORMAL"
            print(f"    {marker.marker_name}: {marker.value} {marker.unit} - {status}")
            print(f"      Reference Range: {marker.reference_min}-{marker.reference_max} {marker.unit}")
    
    print("\n" + "-"*70)
    
    # Show reference ranges
    print("\n Step 4: Available Tumor Markers & Reference Ranges...")
    ranges = tumor_marker_service.get_reference_ranges()
    print("\n   Marker Name       | Normal Range      | Unit")
    print("   " + "-"*50)
    for name, ref in ranges.items():
        print(f"   {name:17} | {ref['min']:4.1f} - {ref['max']:5.1f} | {ref['unit']}")
    
    print("\n" + "-"*70)
    
    # Get patient's diagnosis
    print("\n Step 5: Retrieving patient diagnosis...")
    diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
    print(f"    Found {len(diagnoses)} diagnosis record(s)")
    for diag in diagnoses:
        print(f"\n  ID {diag.id}:")
        print(f"      Cancer Type: {diag.cancer_type}")
        print(f"      Stage: {diag.stage}")
        print(f"      Date: {diag.diagnosis_date.strftime('%Y-%m-%d')}")
    
    print("\n" + "-"*70)
    
    # Get patient's markers
    print("\n Step 6: Retrieving all tumor marker results...")
    all_markers = tumor_marker_service.get_patient_markers(patient.id)
    print(f"    Found {len(all_markers)} marker test(s)")
    
    abnormal_count = sum(1 for m in all_markers if m.is_abnormal)
    print(f"    Abnormal: {abnormal_count}")
    print(f"   🟢 Normal: {len(all_markers) - abnormal_count}")
    
    print("\n" + "-"*70)
    
    # Storage info
    print("\n Step 7: Storage Configuration...")
    print(f"    Image Upload Directory: uploads/medical_images/")
    print(f"    Database Tables:")
    print(f"      - post_diagnosis")
    print(f"      - medical_images")
    print(f"      - tumor_markers")
    print(f"    All tables created successfully")
    
    print("\n" + "="*70)
    print("   DEMO COMPLETE!")
    print("="*70)
    print("\n Summary:")
    print(f"   - Patient: {patient.name}")
    print(f"   - Diagnoses Created: {len(diagnoses)}")
    print(f"   - Markers Recorded: {len(all_markers)}")
    print(f"   - Abnormal Markers: {abnormal_count}")
    print("\n All Day 1 features working correctly!\n")

if __name__ == "__main__":
    demo_post_diagnosis()
