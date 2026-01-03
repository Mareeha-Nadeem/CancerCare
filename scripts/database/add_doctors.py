"""
Quick script to add sample doctors to database
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.services.doctor_service import doctor_service

def add_doctors():
    """Add sample doctors"""
    print("Adding sample doctors...\n")
    
    doctors = [
        {
            "name": "Dr. Sarah Wilson",
            "email": "sarah.wilson@hospital.com",
            "specialization": "Oncology",
            "phone": "555-0201"
        },
        {
            "name": "Dr. Michael Chen",
            "email": "michael.chen@hospital.com",
            "specialization": "Pulmonology",
            "phone": "555-0202"
        },
        {
            "name": "Dr. Emily Rodriguez",
            "email": "emily.rodriguez@hospital.com",
            "specialization": "Radiology",
            "phone": "555-0203"
        },
        {
            "name": "Dr. James Anderson",
            "email": "james.anderson@hospital.com",
            "specialization": "Thoracic Surgery",
            "phone": "555-0204"
        },
        {
            "name": "Dr. Lisa Thompson",
            "email": "lisa.thompson@hospital.com",
            "specialization": "Internal Medicine",
            "phone": "555-0205"
        }
    ]
    
    for doctor_data in doctors:
        doctor, error = doctor_service.create_doctor(doctor_data)
        if error:
            print(f" Error adding {doctor_data['name']}: {error}")
        else:
            print(f" Added: {doctor_data['name']} - {doctor_data['specialization']}")
    
    print("\n All doctors added successfully!")
    print("\nYou can now:")
    print("  - Schedule appointments")
    print("  - View doctors in Doctors page")
    print("  - Refresh your browser to see the changes")

if __name__ == "__main__":
    add_doctors()
