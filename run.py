"""
Quick run script for CancerCare Application
"""
import subprocess
import sys

print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║               🫁 CancerCare Application                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

🚀 Starting application on http://localhost:8501
Press Ctrl+C to stop
""")

try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])
except KeyboardInterrupt:
    print("\n\n👋 Application stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nIf you haven't set up the application yet, run: python setup.py")
