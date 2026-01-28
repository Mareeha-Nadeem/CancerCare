"""
Create test data for notifications and messaging system
"""
from core.notification_service import notification_service
from core.services.message_service import message_service
from core.db_config import get_session
from core.models import User
from datetime import datetime, timedelta
import random


def create_test_users():
    """Create test users if they don't exist"""
    session = get_session()
    try:
        # Check if users exist
        existing = session.query(User).count()
        if existing >= 3:
            print(f"✓ Found {existing} existing users")
            return
        
        users = [
            {'username': 'admin', 'email': 'admin@cancercare.com', 'password_hash': 'hashed123', 'role': 'admin'},
            {'username': 'dr_smith', 'email': 'smith@cancercare.com', 'password_hash': 'hashed123', 'role': 'doctor'},
            {'username': 'lab_tech', 'email': 'tech@cancercare.com', 'password_hash': 'hashed123', 'role': 'patient'},
        ]
        
        for user_data in users:
            # Check if user already exists
            existing_user = session.query(User).filter(User.username == user_data['username']).first()
            if not existing_user:
                user = User(**user_data)
                session.add(user)
        
        session.commit()
        print("✓ Created test users")
    finally:
        session.close()


def create_test_notifications():
    """Create sample notifications with different priorities"""
    print("\n📊 Creating test notifications...")
    
    notifications_data = [
        {
            'user_id': 1,
            'title': 'High-Risk Patient Alert',
            'message': 'Patient John Doe (MRN: 12345) has a high-risk prediction of 92.3%. Immediate review recommended.',
            'type': 'warning',
            'priority': 'urgent',
            'related_type': 'prediction',
            'related_id': 1
        },
        {
            'user_id': 1,
            'title': 'New Prediction Completed',
            'message': 'Lung cancer risk prediction for patient Jane Smith has been completed. Risk Level: Medium (65.2%)',
            'type': 'success',
            'priority': 'high',
            'related_type': 'prediction',
            'related_id': 2
        },
        {
            'user_id': 1,
            'title': 'System Update',
            'message': 'ML model has been updated to version 2.1. Improved accuracy by 3.2%.',
            'type': 'info',
            'priority': 'normal',
        },
        {
            'user_id': 1,
            'title': 'Appointment Reminder',
            'message': 'Patient consultation scheduled for tomorrow at 10:00 AM with Dr. Smith',
            'type': 'info',
            'priority': 'high',
            'related_type': 'appointment',
            'related_id': 1
        },
        {
            'user_id': 1,
            'title': 'Database Backup Complete',
            'message': 'Weekly database backup completed successfully. 156 records backed up.',
            'type': 'success',
            'priority': 'low',
        },
        {
            'user_id': 1,
            'title': 'Error in Batch Processing',
            'message': 'Batch prediction job failed for file "patients_20260105.csv". Please review the input data format.',
            'type': 'error',
            'priority': 'high',
        },
        {
            'user_id': 1,
            'title': 'New Patient Registered',
            'message': 'Patient Robert Johnson (MRN: 78910) has been added to the system.',
            'type': 'info',
            'priority': 'normal',
        },
    ]
    
    created_count = 0
    for notif_data in notifications_data:
        try:
            notification_service.create_notification(**notif_data)
            created_count += 1
        except Exception as e:
            print(f"  Error creating notification: {e}")
    
    print(f"✓ Created {created_count} test notifications")


def create_test_messages():
    """Create sample threaded messages"""
    print("\n💬 Creating test messages...")
    
    # Message 1: New conversation
    msg1 = message_service.send_message(
        sender_id=2,
        recipient_id=1,
        subject="Patient Consultation Request",
        body="Hi, I need your assistance with a high-risk patient case. The prediction shows 89% confidence for lung cancer. Can we schedule a review?",
        priority="high"
    )
    
    # Reply to message 1
    msg2 = message_service.send_message(
        sender_id=1,
        recipient_id=2,
        subject="Re: Patient Consultation Request",
        body="Absolutely! I've reviewed the case. Let's meet tomorrow at 2 PM to discuss the treatment plan. I'll prepare the detailed analysis.",
        priority="high",
        parent_message_id=msg1.id
    )
    
    # Reply to reply
    message_service.send_message(
        sender_id=2,
        recipient_id=1,
        subject="Re: Patient Consultation Request",
        body="Perfect! See you tomorrow at 2 PM. Thanks for the quick response!",
        priority="normal",
        parent_message_id=msg2.id
    )
    
    # Message 2: Different conversation
    msg3 = message_service.send_message(
        sender_id=3,
        recipient_id=1,
        subject="Lab Results Ready",
        body="The tumor marker results for Patient ID 456 are now available. CEA levels are elevated at 8.2 ng/mL (ref: 0-3). Please review.",
        priority="normal"
    )
    
    # Message 3: Another conversation
    message_service.send_message(
        sender_id=1,
        recipient_id=2,
        subject="Weekly Report",
        body="Please find attached the weekly summary of all high-risk predictions. We had 12 cases this week with an average confidence of 84.3%.",
        priority="low"
    )
    
    # Mark some as read
    message_service.mark_as_read(msg3.id)
    
    print("✓ Created test message threads with read receipts")


def main():
    print("=" * 60)
    print("🚀 Creating Test Data for Notifications & Messaging")
    print("=" * 60)
    
    create_test_users()
    create_test_notifications()
    create_test_messages()
    
    print("\n" + "=" * 60)
    print("✅ Test Data Creation Complete!")
    print("=" * 60)
    print("\n📊 Summary:")
    print("  • 3 test users created")
    print("  • 7 notifications with different priorities")
    print("  • 5 messages in 3 threaded conversations")
    print("  • Read receipts configured")
    print("\n💡 Test the features:")
    print("  1. Navigate to Notifications page")
    print("  2. Enable auto-refresh to see real-time updates")
    print("  3. Navigate to Messages page")
    print("  4. Check threaded conversations and read receipts")
    print("=" * 60)


if __name__ == "__main__":
    main()
