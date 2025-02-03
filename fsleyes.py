# view nifti files using fsleyes
import subprocess

def run_fsleyes(nifti_file):
    command = ["fsleyes", nifti_file]
    
    try:
        subprocess.run(command, check=True)
        print("FSLeyes launched successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error launching FSLeyes: {e}")

# replace chris_t1.nii with the path to the input NIfTI file
run_fsleyes("chris_t1.nii")