"""
Test script to verify messaging setup and database initialization
"""
from core.db_config import init_database, get_session
from core.models import Message, User, Notification
from core.services.message_service import message_service
from datetime import datetime
import sys

def verify_database():
    """Verify database tables exist and seed test data"""
    print("=" * 60)
    print("CancerCare Messaging Module Verification")
    print("=" * 60)
    
    # 1. Initialize database
    print("\n1. Initializing database...")
    try:
        init_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    
    # 2. Check if tables exist and count records
    print("\n2. Checking database tables...")
    session = get_session()
    try:
        user_count = session.query(User).count()
        message_count = session.query(Message).count()
        notification_count = session.query(Notification).count()
        
        print(f"✓ Users table: {user_count} records")
        print(f"✓ Messages table: {message_count} records")
        print(f"✓ Notifications table: {notification_count} records")
        
        # Get all users for reference
        if user_count > 0:
            print("\n3. Available users:")
            users = session.query(User).all()
            for user in users:
                print(f"   - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        
        # 4. Create test messages if we have at least 2 users
        if user_count >= 2:
            print("\n4. Creating test messages...")
            try:
                # Get first two users
                users = session.query(User).limit(2).all()
                user1, user2 = users[0], users[1]
                
                # Send test messages
                msg1 = message_service.send_message(
                    sender_id=user1.id,
                    recipient_id=user2.id,
                    subject="Welcome to CancerCare",
                    body="This is a test message to verify the messaging system is working correctly."
                )
                print(f"✓ Message 1 created: {user1.username} → {user2.username}")
                
                msg2 = message_service.send_message(
                    sender_id=user2.id,
                    recipient_id=user1.id,
                    subject="Re: Welcome to CancerCare",
                    body="Thank you! The messaging system looks great.",
                    parent_message_id=msg1.id
                )
                print(f"✓ Message 2 created: {user2.username} → {user1.username} (threaded reply)")
                
                msg3 = message_service.send_message(
                    sender_id=user1.id,
                    recipient_id=user2.id,
                    subject="Appointment Reminder",
                    body="Don't forget your appointment tomorrow at 10 AM.",
                    priority="high"
                )
                print(f"✓ Message 3 created: {user1.username} → {user2.username}")
                
            except Exception as e:
                print(f"✗ Failed to create test messages: {e}")
        else:
            print("\n⚠ Not enough users to create test messages (need at least 2)")
            print("  Run database_init.py to seed sample users")
        
        # 5. Test message retrieval
        print("\n5. Testing message service functions...")
        try:
            if user_count >= 2:
                users = session.query(User).limit(2).all()
                user1_id = users[0].id
                
                # Test get_conversations
                conversations = message_service.get_conversations(user1_id)
                print(f"✓ get_conversations: {len(conversations)} conversations")
                
                # Test get_unread_count
                unread = message_service.get_unread_count(user1_id)
                print(f"✓ get_unread_count: {unread} unread messages")
                
                # Test get_user_messages
                inbox = message_service.get_user_messages(user1_id, sent=False)
                sent = message_service.get_user_messages(user1_id, sent=True)
                print(f"✓ get_user_messages: {len(inbox)} inbox, {len(sent)} sent")
                
        except Exception as e:
            print(f"✗ Message service test failed: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"✗ Database verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    print("\n" + "=" * 60)
    print("Verification complete! Messaging system is ready.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)
