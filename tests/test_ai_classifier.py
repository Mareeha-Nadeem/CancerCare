"""
Test AI Image Classifier - Day 2
Tests the MedicalImageClassifier with sample images
"""
from core.ml.image_classifier import medical_image_classifier
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path

def create_test_image(filename: str, add_anomaly: bool = False):
    """Create a test medical image"""
    # Create a grayscale image
    img = Image.new('RGB', (512, 512), color='black')
    draw = ImageDraw.Draw(img)
    
    # Draw some basic structure
    draw.rectangle([50, 50, 462, 462], fill='gray', outline='white')
    
    if add_anomaly:
        # Add a bright spot (simulating abnormality)
        draw.ellipse([200, 200, 312, 312], fill='white')
    
    # Save image
    test_dir = Path('uploads/medical_images/test')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = test_dir / filename
    img.save(filepath)
    
    return str(filepath)

def test_image_classifier():
    print("\n" + "="*70)
    print("   TESTING AI IMAGE CLASSIFIER - Day 2")
    print("="*70 + "\n")
    
    # Test 1: Create and analyze normal image
    print("Test 1: Analyzing NORMAL image...")
    normal_image = create_test_image('test_normal.jpg', add_anomaly=False)
    result = medical_image_classifier.analyze_image(normal_image)
    
    print(f"   File: {normal_image}")
    print(f"   Classification: {result.get('classification', 'Unknown')}")
    print(f"   Tumor Detected: {result.get('tumor_detected', False)}")
    print(f"   Confidence: {result.get('confidence_score', 0):.2%}")
    
    print("\n" + "-"*70 + "\n")
    
    # Test 2: Create and analyze abnormal image
    print("Test 2: Analyzing ABNORMAL image...")
    abnormal_image = create_test_image('test_abnormal.jpg', add_anomaly=True)
    result = medical_image_classifier.detect_abnormalities(abnormal_image)
    
    print(f"   File: {abnormal_image}")
    print(f"   Classification: {result.get('classification', 'Unknown')}")
    print(f"   Tumor Detected: {result.get('tumor_detected', False)}")
    print(f"   Confidence: {result.get('confidence_score', 0):.2%}")
    print(f"   Tumor Count: {result.get('tumor_count', 0)}")
    print(f"   Largest Size: {result.get('largest_tumor_size', 0):.1f} mm")
    
    print("\n" + "-"*70 + "\n")
    
    # Test 3: Compare images
    print("Test 3: Comparing before/after images...")
    comparison = medical_image_classifier.compare_images(abnormal_image, normal_image)
    
    print(f"   Before: {comparison.get('before', {}).get('classification', 'Unknown')}")
    print(f"   After: {comparison.get('after', {}).get('classification', 'Unknown')}")
    print(f"   Change: {comparison.get('change', 0):.3f}")
    print(f"   Result: {comparison.get('improvement', 'Unknown')}")
    
    print("\n" + "="*70)
    print("   AI CLASSIFIER TESTS COMPLETE!")
    print(f"="*70 + "\n")

if __name__ == "__main__":
    test_image_classifier()
