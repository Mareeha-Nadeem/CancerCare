"""
Simple Password Fixer - Updates .env with your PostgreSQL password
"""

print("""

                                                                  
           PostgreSQL Password Fix                              
                                                                  


This will update your .env file with the correct PostgreSQL password.
""")

print("\nWhat is your PostgreSQL password?")
print("(This is the password you set when installing PostgreSQL)\n")

password = input("Enter PostgreSQL password: ").strip()

if not password:
    print("\n No password entered. Exiting.")
    exit(1)

# Update .env file
try:
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('DATABASE_URL='):
                # Update with new password
                f.write(f'DATABASE_URL=postgresql+psycopg2://postgres:{password}@localhost:5432/cancercare\n')
            else:
                f.write(line)
    
    print("\n Password updated in .env file!")
    print("\nNow run:")
    print("  python init_db_simple.py")
    print("\nThen:")
    print("  streamlit run app.py")
    
except Exception as e:
    print(f"\n Error: {e}")
