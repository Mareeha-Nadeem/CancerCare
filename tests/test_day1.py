"""
Test script for Day 1 post-diagnosis functionality
Tests database models and services
"""
from core.services.post_diagnosis_service import post_diagnosis_service
from core.services.tumor_marker_service import tumor_marker_service
from datetime import datetime

def test_day1():
    print("\n" + "="*60)
    print("  Testing Day 1 - Post-Diagnosis Backend")
    print("="*60 + "\n")
    
    # Test 1: Create diagnosis
    print("Test 1: Creating diagnosis record...")
    diagnosis_data = {
        'diagnosis_date': datetime.utcnow(),
        'cancer_type': 'Lung Cancer',
        'stage': 'Stage II',
        'tumor_size_mm': 25.5,
        'lymph_nodes_affected': 2,
        'metastasis_status': 'None',
        'treatment_plan': 'Chemotherapy + Radiation',
        'notes': 'Test diagnosis for Day 1'
    }
    
    diagnosis, error = post_diagnosis_service.create_diagnosis(
        patient_id=1,  # Assuming patient ID 1 exists
        data=diagnosis_data
    )
    
    if error:
        print(f"    Error: {error}")
    else:
        print(f"    Diagnosis created: ID {diagnosis.id}")
    
    # Test 2: Record tumor marker
    print("\nTest 2: Recording tumor marker...")
    marker_data = {
        'marker_name': 'CEA',
        'value': 4.5,
        'test_date': datetime.utcnow(),
        'lab_name': 'Test Lab'
    }
    
    marker, error = tumor_marker_service.record_marker(
        patient_id=1,
        marker_data=marker_data
    )
    
    if error:
        print(f"    Error: {error}")
    else:
        print(f"    Marker recorded: {marker.marker_name} = {marker.value} {marker.unit}")
        print(f"      Abnormal: {marker.is_abnormal}")
    
    # Test 3: Get reference ranges
    print("\nTest 3: Getting reference ranges...")
    ranges = tumor_marker_service.get_reference_ranges()
    print("    Available markers:")
    for name, ref in ranges.items():
        print(f"      - {name}: {ref['min']}-{ref['max']} {ref['unit']}")
    
    print("\n" + "="*60)
    print("  Day 1 Testing Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_day1()
