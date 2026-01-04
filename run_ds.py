"""
Run Data Science Scripts - Helper Script
Allows running data_science scripts from project root
"""
import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("""
Usage: python run_ds.py <script_name>

Available scripts:
  preprocess       - Run data preprocessing
  train           - Train ML model
  predict         - Make predictions with trained model
  interface       - Interactive prediction interface

Examples:
  python run_ds.py preprocess
  python run_ds.py train
  python run_ds.py predict
        """)
        sys.exit(1)
    
    script_name = sys.argv[1].lower()
    
    # Map script names to actual files
    scripts = {
        'preprocess': 'data_science/model_1/preprocess.py',
        'train': 'data_science/model_1/train_model.py',
        'predict': 'data_science/model_1/prediction.py',
        'interface': 'data_science/model_1/interface.py',
    }
    
    if script_name not in scripts:
        print(f" Unknown script: {script_name}")
        print(f"Available: {', '.join(scripts.keys())}")
        sys.exit(1)
    
    script_path = Path(scripts[script_name])
    
    if not script_path.exists():
        print(f" Script not found: {script_path}")
        sys.exit(1)
    
    print(f" Running: {script_path}")
    print("=" * 50)
    
    # Run the script
    result = subprocess.run([sys.executable, str(script_path)] + sys.argv[2:])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
