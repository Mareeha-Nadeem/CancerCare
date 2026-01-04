"""
Remove all emojis from Python files in the project.
"""
import re
from pathlib import Path

# Emoji pattern (matches most common emojis)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Extended Symbols and Pictographs
    "]+", 
    flags=re.UNICODE
)

def remove_emojis(text):
    """Remove emojis from text"""
    return EMOJI_PATTERN.sub('', text)

def process_file(file_path):
    """Remove emojis from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        new_content = remove_emojis(content)
        
        # Only write if changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, file_path.relative_to(PROJECT_ROOT)
        return False, None
    except Exception as e:
        return False, f"Error: {e}"

# Find project root
PROJECT_ROOT = Path(__file__).parent

# Find all Python files
python_files = list(PROJECT_ROOT.rglob('*.py'))

print(f"Found {len(python_files)} Python files")
print("Removing emojis...\n")

modified_count =  0
modified_files = []

for py_file in python_files:
    changed, info = process_file(py_file)
    if changed:
        modified_count += 1
        modified_files.append(str(info))
        print(f" {info}")

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Total files scanned: {len(python_files)}")
print(f"Files modified: {modified_count}")
print(f"\nDone!")
