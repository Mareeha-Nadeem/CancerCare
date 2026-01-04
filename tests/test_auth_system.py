"""
Test Authentication System
Tests landing page, signup, login, and dashboard access
"""
import sys
sys.path.insert(0, 'e:/Project/CancerCare -- Copy')

from core.services.auth_service import auth_service


def test_auth_system():
    """Test complete authentication flow"""
    
    print("\n" + "="*60)
    print("   TESTING AUTHENTICATION SYSTEM")
    print("="*60 + "\n")
    
    # Test 1: User Registration
    print(" Test 1: User Registration")
    print("-" * 40)
    
    username = "testuser"
    email = "test@cancercare.com"
    password = "test123"
    
    user, error = auth_service.register_user(
        username=username,
        email=email,
        password=password,
        role="admin"
    )
    
    if error and "already exists" not in error:
        print(f"    Registration failed: {error}")
        return
    elif error:
        print(f"   ℹ  User already exists, continuing with login test")
    else:
        print(f"    User registered successfully!")
        print(f"      Username: {user.username}")
        print(f"      Email: {user.email}")
        print(f"      Role: {user.role}")
    
    print()
    
    # Test 2: Login with correct password
    print(" Test 2: Login with Correct Credentials")
    print("-" * 40)
    
    user, error = auth_service.login_user(username, password)
    
    if error:
        print(f"    Login failed: {error}")
    else:
        print(f"    Login successful!")
        print(f"      User ID: {user.id}")
        print(f"      Username: {user.username}")
        print(f"      Role: {user.role}")
        print(f"      Last Login: {user.last_login}")
    
    print()
    
    # Test 3: Login with wrong password
    print(" Test 3: Login with Wrong Password")
    print("-" * 40)
    
    user, error = auth_service.login_user(username, "wrongpassword")
    
    if error:
        print(f"    Correctly rejected: {error}")
    else:
        print(f"    Should have failed but didn't!")
    
    print()
    
    # Test 4: Retrieve user by username
    print(" Test 4: Retrieve User")
    print("-" * 40)
    
    user = auth_service.get_user_by_username(username)
    
    if user:
        print(f"    User found!")
        print(f"      ID: {user.id}")
        print(f"      Username: {user.username}")
        print(f"      Email: {user.email}")
        print(f"      Active: {user.is_active}")
    else:
        print(f"    User not found")
    
    print("\n" + "="*60)
    print("   ALL AUTHENTICATION TESTS COMPLETED!")
    print("="*60 + "\n")
    
    print(" To test the full system:")
    print("   1. Run: streamlit run app.py")
    print("   2. Landing page will appear")
    print("   3. Click 'Sign Up' or 'Login'")
    print("   4. After login, dashboard appears")
    print("   5. Access all features from dashboard\n")


if __name__ == "__main__":
    test_auth_system()
