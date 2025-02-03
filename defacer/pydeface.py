import subprocess

def run_pydeface(input_nifti):
    command = ["pydeface", input_nifti]

    try:
        subprocess.run(command, check=True)
        print(f"Defacing completed for {input_nifti}")
    except subprocess.CalledProcessError as e:
        print(f"Error running pydeface: {e}")

# replace chris_t1.nii with the path to the input NIfTI file
run_pydeface("chris_t1.nii") 
