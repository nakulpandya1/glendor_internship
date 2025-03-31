import os
import subprocess

input_directory = "/Users/nakulpandya/Desktop/3990/data"  # Folder with input MRI files
brain_output_directory = "/Users/nakulpandya/Desktop/3990/data/brain"  # Folder for brain-extracted images
mask_output_directory = "/Users/nakulpandya/Desktop/3990/data/mask"  # Folder for brain masks

# Ensure output directories exist
os.makedirs(brain_output_directory, exist_ok=True)
os.makedirs(mask_output_directory, exist_ok=True)

# Get all .nii or .nii.gz files in the input directory
input_image_paths = [f for f in os.listdir(input_directory) 
                     if f.endswith(('.nii', '.nii.gz'))]

if not input_image_paths:
    raise ValueError("No .nii or .nii.gz files found in the input directory.")

for filename in input_image_paths:
    input_file = os.path.join(input_directory, filename)
    print (f"Processing {filename} for brain extraction...")
    # Define output paths
    brain_output_file = os.path.join(brain_output_directory, filename.replace('.nii.gz', '').replace('.nii', '') + "_brain.nii")
    mask_output_file = os.path.join(mask_output_directory, filename.replace('.nii.gz', '').replace('.nii', '') + "_brain_mask.nii.gz")

    # Run BET with -m (outputs a mask alongside the brain-extracted image)
    bet_cmd = f"bet {input_file} {brain_output_file} -m"
    subprocess.run(bet_cmd, shell=True, check=True)

    # Move the mask file to the mask_output_directory
    generated_mask_file = brain_output_file.replace(".nii", "") + "_mask.nii.gz"
    os.rename(generated_mask_file, mask_output_file)

    print(f"Brain extraction completed: {brain_output_file}")
    print(f"Mask saved: {mask_output_file}")

print("All files have been processed.")

###########
import os
import subprocess
import shutil

input_directory = "/Users/nakulpandya/Desktop/3990/data/brain"  # Folder containing brain-extracted images
output_directory = "/Users/nakulpandya/Desktop/3990/data/segmentation"  # Folder to save FAST outputs

# Ensure output directories exist
os.makedirs(output_directory, exist_ok=True)
pve_0_dir = os.path.join(output_directory, "pve_0")
pve_1_dir = os.path.join(output_directory, "pve_1")
basename_dir = os.path.join(output_directory, "basename")

for folder in [pve_0_dir, pve_1_dir, basename_dir]:
    os.makedirs(folder, exist_ok=True)

# Get all .nii or .nii.gz files in the input directory
input_image_paths = [f for f in os.listdir(input_directory) 
                     if f.endswith(('.nii', '.nii.gz'))]

if not input_image_paths:
    raise ValueError("No .nii or .nii.gz files found in the input directory.")

for filename in input_image_paths:
    input_file = os.path.join(input_directory, filename)

    print(f"Processing {filename} for FAST segmentation...")
    
    # Remove extensions (.nii or .nii.gz) to create the output filename prefix
    base_filename = filename.replace('.nii.gz', '').replace('.nii', '')

    # Define output prefix
    output_prefix = os.path.join(output_directory, base_filename)

    # Run FAST segmentation
    fast_cmd = f"fast -o {output_prefix} {input_file}"
    subprocess.run(fast_cmd, shell=True, check=True)

    print(f"FAST segmentation completed: Organizing outputs...")

    # Move relevant output files to respective directories
    expected_files = [
        (f"{base_filename}_pve_0.nii.gz", pve_0_dir),
        (f"{base_filename}_pve_1.nii.gz", pve_1_dir),
        (f"{base_filename}_seg.nii.gz", basename_dir),  # Segmentation mask
        (f"{base_filename}_pve_2.nii.gz", basename_dir),
        (f"{base_filename}_mixeltype.nii.gz", basename_dir),
        (f"{base_filename}_pveseg.nii.gz", basename_dir)
    ]

    for file, destination in expected_files:
        src_path = os.path.join(output_directory, file)
        if os.path.exists(src_path):
            shutil.move(src_path, os.path.join(destination, file))

    print(f"Files organized: {base_filename}")

print("All files have been processed and organized.")