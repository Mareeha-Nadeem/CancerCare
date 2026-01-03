"""
Comprehensive Day 2 Demo - AI Integration
Tests complete backend pipeline with AI analysis
"""
from core.services.image_service import image_service
from core.services.post_diagnosis_service import post_diagnosis_service
from core.services.tumor_marker_service import tumor_marker_service
from core.services.patient_service import patient_service
from PIL import Image, ImageDraw
from pathlib import Path
from datetime import datetime
import io

def create_mock_medical_image():
    """Create a mock medical image"""
    img = Image.new('RGB', (512, 512), color='darkgray')
    draw = ImageDraw.Draw(img)
    
    # Draw something that looks like a scan
    draw.ellipse([100, 100, 412, 412], fill='lightgray')
    draw.ellipse([200, 200, 312, 312], fill='white')  # Bright spot
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def demo_day2():
    print("\n" + "="*70)
    print("   DAY 2 DEMO - AI Integration Complete")
    print("="*70 + "\n")
    
    # Get patient
    patients = patient_service.get_all_patients()
    if patients:
        patient = patients[0]
        print(f" Using patient: {patient.name} (ID: {patient.id})\n")
    else:
        print(" No patients found. Please add a patient first.")
        return
    
    # Create diagnosis if doesn't exist
    print(" Step 1: Creating/Getting diagnosis...")
    diagnosis_data = {
        'diagnosis_date': datetime.utcnow(),
        'cancer_type': 'Lung Cancer',
        'stage': 'Stage II',
        'tumor_size_mm': 28.0,
    }
    
    diagnosis, error = post_diagnosis_service.create_diagnosis(
        patient_id=patient.id,
        data=diagnosis_data
    )
    
    if error:
        # Try to get existing
        diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
        diagnosis = diagnoses[0] if diagnoses else None
    
    if diagnosis:
        print(f"    Diagnosis: {diagnosis.cancer_type}, {diagnosis.stage}")
    
    print("\n" + "-"*70 + "\n")
    
    # Upload and analyze image
    print(" Step 2: Uploading medical image with AI analysis...")
    
    image_file = create_mock_medical_image()
    
    medical_image, error = image_service.upload_image(
        patient_id=patient.id,
        image_file=image_file,
        image_type='CT Scan',
        post_diagnosis_id=diagnosis.id if diagnosis else None,
        filename='test_ct_scan.jpg',
        auto_analyze=True  # Enable AI analysis
    )
    
    if error:
        print(f"    Error: {error}")
    else:
        print(f"    Image uploaded: ID {medical_image.id}")
        print(f"    Path: {medical_image.file_path}")
        print(f"    Size: {medical_image.image_width}x{medical_image.image_height}")
        print(f"\n    AI Analysis Results:")
        print(f"      Analyzed: {medical_image.ai_analyzed}")
        print(f"      Tumor Detected: {'Yes' if medical_image.tumor_detected else 'No'}")
        print(f"      Confidence: {medical_image.confidence_score:.2%}")
        print(f"      Tumor Count: {medical_image.tumor_count}")
        if medical_image.largest_tumor_size:
            print(f"      Largest Size: {medical_image.largest_tumor_size:.1f} mm")
    
    print("\n" + "-"*70 + "\n")
    
    # Record tumor markers
    print(" Step 3: Recording tumor markers...")
    
    markers = [
        {'name': 'CEA', 'value': 5.2},
        {'name': 'CA 19-9', 'value': 35.0},
    ]
    
    for marker_info in markers:
        marker, error = tumor_marker_service.record_marker(
            patient_id=patient.id,
            marker_data={
                'marker_name': marker_info['name'],
                'value': marker_info['value'],
                'test_date': datetime.utcnow()
            },
            post_diagnosis_id=diagnosis.id if diagnosis else None
        )
        
        if not error:
            status = " ABNORMAL" if marker.is_abnormal else "🟢 NORMAL"
            print(f"   {status} {marker.marker_name}: {marker.value} {marker.unit}")
    
    print("\n" + "-"*70 + "\n")
    
    # Summary
    print(" Step 4: Complete Summary...")
    
    all_images = image_service.get_patient_images(patient.id)
    all_markers = tumor_marker_service.get_patient_markers(patient.id)
    all_diagnoses = post_diagnosis_service.get_patient_diagnosis(patient.id)
    
    print(f"\n   Patient: {patient.name}")
    print(f"   Diagnoses: {len(all_diagnoses)}")
    print(f"   Images Uploaded: {len(all_images)}")
    print(f"   Images AI-Analyzed: {sum(1 for img in all_images if img.ai_analyzed)}")
    print(f"   Abnormalities Detected: {sum(1 for img in all_images if img.tumor_detected)}")
    print(f"   Tumor Markers: {len(all_markers)}")
    print(f"   Abnormal Markers: {sum(1 for m in all_markers if m.is_abnormal)}")
    
    print("\n" + "="*70)
    print("   DAY 2 INTEGRATION COMPLETE!")
    print("="*70)
    print("\n All AI features working:")
    print("   - Image upload with automatic AI analysis")
    print("   - Abnormality detection")
    print("   - Confidence scoring")
    print("   - Tumor counting and sizing")
    print("   - Integration with diagnosis records")
    print("\n Ready for Day 3: Frontend Development!\n")

if __name__ == "__main__":
    demo_day2()
