// install pyradiomics
python -m pip install pyradiomics

// if not installed already
pip install simpleitk 

//to generate mask i used nipy
pip install nipy
// to visualize the mask, use visualize_nifti_py (or 3dSlicer, etc.)


// to run the extractor, implement pyradiomics.py
    // generate mask if not already
    // then run pyradiomics on the input files for the image path and mask path
