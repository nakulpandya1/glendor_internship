import subprocess
import os
from glob import glob
import shutil

# FIRST structures to segment
structure_map = {
    "amygdala": "L_Amyg,R_Amyg",
    # "hippocampus": "L_Hipp,R_Hipp",
    # "thalamus": "L_Thal,R_Thal",
}

def run_first_all(input_file, output_prefix, structures):
    print(f"\nRunning FIRST for [{structures}] on {os.path.basename(input_file)}")
    command = [
        "run_first_all",
        "-i", input_file,
        "-s", structures,
        "-o", output_prefix,
    ]
    subprocess.run(command, check=True)

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    others_folder = os.path.join(output_folder, "others")
    os.makedirs(others_folder, exist_ok=True)

    mri_files = glob(os.path.join(input_folder, "*.nii*"))
    output_prefixes = []

    for mri_file in mri_files:
        filename = os.path.basename(mri_file)
        basename = filename.replace(".nii.gz", "").replace(".nii", "")

        # Determine if it's original or defaced
        subfolder_type = "defaced" if "defaced" in basename.lower() else "original"

        for label, structure_code in structure_map.items():
            output_prefix = os.path.join(output_folder, f"{basename}_{label}")
            run_first_all(mri_file, output_prefix, structure_code)
            output_prefixes.append((output_prefix, basename, label, subfolder_type))

    # Organize files AFTER all processing
    for prefix, basename, label, subfolder_type in output_prefixes:
        dest_folder = os.path.join(output_folder, subfolder_type, f"{basename}_{label}")
        os.makedirs(dest_folder, exist_ok=True)

        for file in glob(f"{prefix}*"):
            if not os.path.isfile(file):
                continue
            filename = os.path.basename(file)
            if filename.endswith("_firstseg.nii.gz"):
                shutil.move(file, os.path.join(dest_folder, filename))
            else:
                shutil.move(file, os.path.join(others_folder, filename))

    print("\nAll segmentations completed and organized.")

# Example usage
input_folder = "/Users/nakulpandya/Desktop/3990/data/original"
output_folder = "/Users/nakulpandya/Desktop/3990/data/segmentation"

process_folder(input_folder, output_folder)