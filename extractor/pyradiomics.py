from nipy.labs.mask import compute_mask_files

# Generate mask file
compute_mask_files("chris_t1.nii", "chris_t1_mask.nii", return_mean=False, m=0.2, M=0.9, cc=1, exclude_zeros=False, opening=2)
compute_mask_files("chris_t1_defaced.nii", "chris_t1_defaced_mask.nii", return_mean=False, m=0.2, M=0.9, cc=1, exclude_zeros=False, opening=2)
