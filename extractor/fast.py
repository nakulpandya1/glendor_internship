from nipype.interfaces import fsl
from nipype.interfaces.fsl import BET
import os

input_image = "chris_t1_defaced.nii"  # replace with the file path

bet = BET() # initialize BET interface
bet.inputs.in_file = input_image
bet.inputs.frac = 0.5  # fractional intensity threshold (default is 0.5)
bet.inputs.mask = True  # generate a overall brain mask

result = bet.run() # run BET

print(f"Brain extraction has completed. Output saved to: {result.outputs.out_file}")

###########

#input_path = "/Users/nakulpandya/Desktop/3990/data/chris_t1.nii"  # replace with the path to the MRI image file
output_directory = "/Users/nakulpandya/Desktop/3990/data"  # replace with the desired output directory
input_directory = "/Users/nakulpandya/Desktop/3990/data"  # folder with the MRI files

# obtains all .nii or .nii.gz files from the directory
input_image_paths = [os.path.join(input_directory, f) for f in os.listdir(input_directory) 
                     if f.endswith(('.nii', '.nii.gz'))]

print("files to be processed:")
for path in input_image_paths:
    print(path)

# Ensure there are files in the list
if not input_image_paths:
    raise ValueError("no .nii or .nii.gz files found in the directory.")

for input_file in input_image_paths:
    print(f"processing {input_file}.")

    # set up FAST for tissue segmentation
    fast = fsl.FAST()
    # assigns the current input file to FAST
    fast.inputs.in_files = input_file
    # change to the output directory as it is needed to complete the segmentation
    os.chdir(output_directory)
    # run FAST on the current file
    fast.run()

print("FAST segmentation has completed for all files.")
