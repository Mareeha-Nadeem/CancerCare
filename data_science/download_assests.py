import os
import subprocess

FILES = {
    # DATA
    "raw_data.csv": "1mlF6k-YVMx-jLp6t4UJPGxhAkr6Mq5Mm",
    "raw_data5000.csv": "1R74xRr1rU2_Ubvcho261qYWpgJg4W5zc",
    "cleaned_data.csv": "1Q5HeVqnN4J-khEhRlo93jSplXHe4vSot",

    # MODELS
    "Stacked_Model_pipeline.pkl": "17NFnenqnV4A-33hHtCl-pVKOYEy8yMV3",
    "Stacked_Model_pipeline_tuned.pkl": "1gjcd-QatnaQ5RzARXgYw0LmiV-BHbh_e",
    "RandomForest_Model_pipeline.pkl": "1-FHepupokjJzlrdI2DXbpFrgV0TkTU8x",
}

def download_from_drive(file_id, out_path):
    cmd = [
        "python", "-m", "gdown",
        f"https://drive.google.com/uc?id={file_id}",
        "-O", out_path,
    ]
    subprocess.check_call(cmd)

if __name__ == "__main__":
    os.makedirs("data_science/data", exist_ok=True)
    os.makedirs("data_science/models", exist_ok=True)

    for name, fid in FILES.items():
        folder = "models" if name.endswith(".pkl") else "data"
        out = f"data_science/{folder}/{name}"

        if not os.path.exists(out):
            print(f"Downloading {name}...")
            download_from_drive(fid, out)
        else:
            print(f"{name} already exists.")
