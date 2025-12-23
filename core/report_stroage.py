import os
import uuid

UPLOAD_DIR = "database/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file):
    ext = os.path.splitext(file.name)[1]
    new_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, new_name)
    
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    
    return path, new_name
