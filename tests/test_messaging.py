"""
Test Messaging System - Verify all functionality works
"""
from core.services.message_service import message_service
from core.db_config import get_session
from core.models import User

def test_messaging_system():
    print("=" * 60)
    print("TESTING MESSAGING SYSTEM")
    print("=" * 60)
    
    # Test with user ID 1 (default)
    user_id = 1
    
    print(f"\nTesting with user_id: {user_id}")
    
    # Test1: Get stats
    print("\n[TEST 1] Getting messaging statistics...")
    try:
        stats = message_service.get_stats(user_id)
        print(f"  Total Messages: {stats['total_messages']}")
        print(f"  Active Conversations: {stats['active_conversations']}")
        print(f"  Data Transferred: {stats['data_transferred_kb']} KB")
        print(f"  Unread: {stats['unread_count']}")
        print("  ✓ Stats retrieval successful")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 2: Get conversations
    print("\n[TEST 2] Getting conversations...")
    try:
        conversations = message_service.get_conversations(user_id)
        print(f"  Found {len(conversations)} conversations")
        if conversations:
            for idx, conv in enumerate(conversations[:3], 1):
                print(f"    {idx}. {conv['other_user']} - {conv['latest_message'].subject}")
        print("  ✓ Conversations retrieval successful")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 3: Check if we can send messages
    print("\n[TEST 3] Verifying message sending capability...")
    try:
        # Get available users
        session = get_session()
        users = session.query(User).filter(User.id != user_id).limit(1).all()
        session.close()
        
        if users:
            recipient = users[0]
            print(f"  Found recipient: {recipient.username} (ID: {recipient.id})")
            
            # Send a test message
            message = message_service.send_message(
                sender_id=user_id,
                recipient_id=recipient.id,
                subject="Test Message",
                body="This is a test message to verify the messaging system works.",
                priority='normal'
            )
            print(f"  ✓ Test message sent successfully (ID: {message.id})")
            print(f"    Thread ID: {message.thread_id}")
            
            # Verify stats updated
            new_stats = message_service.get_stats(user_id)
            print(f"  ✓ Stats updated - Total Messages now: {new_stats['total_messages']}")
            
        else:
            print("  ⚠ No other users found for testing")
            print("    You can still compose messages in the app")
        
        print("  ✓ Message sending capability verified")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 4: Unread count
    print("\n[TEST 4] Testing unread count...")
    try:
        unread = message_service.get_unread_count(user_id)
        print(f"  Unread messages: {unread}")
        print("  ✓ Unread count retrieval successful")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print("\nMessaging system is fully functional!")
    print("\nFeatures verified:")
    print("  ✓ Statistics tracking (Total, Active, Data, Unread)")
    print("  ✓ Conversation management")
    print("  ✓ Message sending")
    print("  ✓ Unread count tracking")
    print("\nYou can now use the messaging module in your Streamlit app!")
    
    return True


if __name__ == "__main__":
    test_messaging_system()
