

FILES = {
    # DATA
    # "raw_data.csv": "1mlF6k-YVMx-jLp6t4UJPGxhAkr6Mq5Mm",
    "raw_data.csv": "1n51N2oWXXKgtasUcR5nzk9HJWguLR4ZE",
    # "raw_data5000.csv": "1R74xRr1rU2_Ubvcho261qYWpgJg4W5zc",
    # "cleaned_data.csv": "1Q5HeVqnN4J-khEhRlo93jSplXHe4vSot",

    # MODELS
    # "Stacked_Model_pipeline.pkl": "17NFnenqnV4A-33hHtCl-pVKOYEy8yMV3",
    # "Stacked_Model_pipeline_tuned.pkl": "1gjcd-QatnaQ5RzARXgYw0LmiV-BHbh_e",
    # "RandomForest_Model_pipeline.pkl": "1-FHepupokjJzlrdI2DXbpFrgV0TkTU8x",
}



import gdown
import os

def download_from_drive(file_id, out_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)  # make sure folder exists
    gdown.download(url, out_path, quiet=False)

for name, fid in FILES.items():
    folder = "models" if name.endswith(".pkl") else "data"
    out = f"{folder}/{name}"

    if not os.path.exists(out):
        print(f"Downloading {name}...")
        download_from_drive(fid, out)
    else:
        print(f"{name} already exists.")
