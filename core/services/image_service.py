"""
Image Service
Handles medical image upload, storage, and management
"""
from core.models import MedicalImage
from core.db_config import get_db_session
from core.ml.image_classifier import medical_image_classifier
from typing import List, Optional, Dict, BinaryIO
from pathlib import Path
from datetime import datetime
import os
import uuid

# Configuration
UPLOAD_DIR = Path("uploads/medical_images")
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.dcm', '.dicom'}
MAX_FILE_SIZE_MB = 50

class ImageService:
    
    @staticmethod
    def upload_image(
        patient_id: int,
        image_file: BinaryIO,
        image_type: str,
        post_diagnosis_id: Optional[int] = None,
        filename: Optional[str] = None,
        auto_analyze: bool = True
    ) -> tuple[Optional[MedicalImage], Optional[str]]:
        """
        Upload and store medical image
        
        Args:
            patient_id: Patient ID
            image_file: File object
            image_type: Type of image (MRI, CT, X-Ray, etc.)
            post_diagnosis_id: Optional link to diagnosis
            filename: Original filename
            
        Returns:
            Tuple of (MedicalImage object, error message)
        """
        try:
            # Validate file extension
            if filename:
                ext = Path(filename).suffix.lower()
                if ext not in ALLOWED_EXTENSIONS:
                    return None, f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
            
            # Create patient-specific directory
            patient_dir = UPLOAD_DIR / str(patient_id)
            patient_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            unique_name = f"{uuid.uuid4().hex}_{filename}" if filename else f"{uuid.uuid4().hex}.jpg"
            file_path = patient_dir / unique_name
            
            # Save file
            with open(file_path, 'wb') as f:
                content = image_file.read()
                
                # Check file size
                size_mb = len(content) / (1024 * 1024)
                if size_mb > MAX_FILE_SIZE_MB:
                    return None, f"File too large ({size_mb:.1f}MB). Max: {MAX_FILE_SIZE_MB}MB"
                
                f.write(content)
            
            # Get image dimensions (if possible)
            width, height = ImageService._get_image_dimensions(file_path)
            
            # Create database record
            db = get_db_session()
            
            try:
                medical_image = MedicalImage(
                    patient_id=patient_id,
                    post_diagnosis_id=post_diagnosis_id,
                    image_type=image_type,
                    file_path=str(file_path),
                    image_width=width,
                    image_height=height,
                    file_size_kb=int(len(content) / 1024),
                    upload_date=datetime.utcnow()
                )
                
                db.add(medical_image)
                db.commit()
                db.refresh(medical_image)
                
                # Automatically analyze image with AI if requested
                if auto_analyze:
                    try:
                        analysis_result = medical_image_classifier.detect_abnormalities(str(file_path))
                        # Update image with AI results
                        medical_image.ai_analyzed = True
                        medical_image.tumor_detected = analysis_result.get('tumor_detected', False)
                        medical_image.confidence_score = analysis_result.get('confidence_score', 0.0)
                        medical_image.tumor_count = analysis_result.get('tumor_count', 0)
                        medical_image.largest_tumor_size = analysis_result.get('largest_tumor_size', 0.0)
                        medical_image.analysis_summary = analysis_result.get('analysis_summary', '')
                        db.commit()
                        print(f" AI Analysis complete: {'Abnormal' if analysis_result.get('tumor_detected') else 'Normal'}")
                    except Exception as ai_error:
                        print(f" AI analysis failed: {ai_error}")
                        # Continue anyway - image is uploaded
                
                return medical_image, None
            except Exception as e:
                db.rollback()
                # Delete file if database save fails
                if file_path.exists():
                    os.remove(file_path)
                return None, str(e)
            finally:
                db.close()
                
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def _get_image_dimensions(file_path: Path) -> tuple[Optional[int], Optional[int]]:
        """Get image width and height"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return img.size
        except:
            return None, None
    
    @staticmethod
    def get_patient_images(patient_id: int) -> List[MedicalImage]:
        """Get all images for a patient"""
        db = get_db_session()
        try:
            return db.query(MedicalImage).filter_by(
                patient_id=patient_id
            ).order_by(MedicalImage.upload_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_diagnosis_images(post_diagnosis_id: int) -> List[MedicalImage]:
        """Get all images for a specific diagnosis"""
        db = get_db_session()
        try:
            return db.query(MedicalImage).filter_by(
                post_diagnosis_id=post_diagnosis_id
            ).order_by(MedicalImage.upload_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def delete_image(image_id: int) -> tuple[bool, Optional[str]]:
        """Delete an image (file and database record)"""
        db = get_db_session()
        
        try:
            image = db.query(MedicalImage).filter_by(id=image_id).first()
            if not image:
                return False, "Image not found"
            
            # Delete file from disk
            file_path = Path(image.file_path)
            if file_path.exists():
                os.remove(file_path)
            
            # Delete database record
            db.delete(image)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()
    
    @staticmethod
    def update_ai_analysis(
        image_id: int,
        analysis_data: Dict
    ) -> tuple[Optional[MedicalImage], Optional[str]]:
        """Update image with AI analysis results"""
        db = get_db_session()
        
        try:
            image = db.query(MedicalImage).filter_by(id=image_id).first()
            if not image:
                return None, "Image not found"
            
            image.ai_analyzed = True
            image.tumor_detected = analysis_data.get('tumor_detected', False)
            image.confidence_score = analysis_data.get('confidence_score', 0.0)
            image.tumor_count = analysis_data.get('tumor_count', 0)
            image.largest_tumor_size = analysis_data.get('largest_tumor_size', 0.0)
            image.analysis_summary = analysis_data.get('analysis_summary', '')
            
            db.commit()
            db.refresh(image)
            
            return image, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()

# Global service instance
image_service = ImageService()
