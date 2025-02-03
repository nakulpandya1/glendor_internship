// install pydeface
pip install pydeface

// downloaded and ran the installer, fslinstaller.py from https: fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index
python ~/Downloads/fslinstaller.py

// show the directory where fsl is installed to verify install
echo $FSLDIR 

// ran pydeface on the test file (old)
// pydeface.py is used to run pydeface in python instead of the command line

// install library packages
pip install matplotlib 
pip install nibabel

// then ran visualize_nifti.py to view both files
