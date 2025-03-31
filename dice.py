# import os
# import nibabel as nib
# import numpy as np

# def test_nifti_all_labels_dice_score(seg_path, seg_file, truth_path, truth_file):
#     truth_uid = os.listdir(truth_path)
#     print(truth_uid)
#     dice_score = 0
#     for uid in  truth_uid:
#         seg_file_path = os.path.join(seg_path, seg_file)
#         truth_file_path = os.path.join(truth_path, truth_file)
#         seg_nib = nib.load(seg_file_path)
#         seg_data = seg_nib.get_fdata()
#         truth_nib = nib.load(truth_file_path)
#         truth_data = truth_nib.get_fdata()
#         uid_dice = calculate_nifti_all_labels_dice_score(seg_data, truth_data)
#         print(uid_dice)
#         dice_score+=uid_dice
#     print('dice score:', dice_score/len(truth_uid))

# def calculate_nifti_all_labels_dice_score(seg_data, truth_data):
#     z_range = range(seg_data.shape[-1])
#     z_len = len(z_range)
#     dice_sum = 0
#     for z in  z_range:
#         seg_slice = seg_data[:,:,z]
#         truth_slice = truth_data[:,:,z]
#         slice_dice = calculate_slice_all_labels_dice_score(seg_slice, truth_slice)
#         dice_sum+=slice_dice

#     return dice_sum / z_len

# def calculate_slice_all_labels_dice_score(segmentation, truth):
#     area_sum = np.sum(segmentation) + np.sum(truth)
#     if area_sum > 0:
#         return np.sum(segmentation[truth>0])*2.0 / area_sum
#     else:
#         return 1

# test_nifti_all_labels_dice_score('/Users/nakulpandya/Desktop/3990/data/mask',
#                                  'combined_mask.nii.gz',
#                                  '/Users/nakulpandya/Desktop/3990/data/mask',
#                                  'combined_mask_defaced.nii.gz')


import nibabel as nib
import numpy as np

def compute_dice_coefficient(mask1_path, mask2_path):

    # load the NIfTI images
    mask1 = nib.load(mask1_path).get_fdata()
    mask2 = nib.load(mask2_path).get_fdata()

    # compute intersection and total voxel count
    intersection = np.sum((mask1 > 0) & (mask2 > 0))
    total_voxels = np.sum(mask1 > 0) + np.sum(mask2 > 0)

    # compute Dice coefficient
    dice = (2 * intersection) / total_voxels if total_voxels > 0 else 1.0
    return dice

# define input file paths
mask1_path = "/Users/nakulpandya/Desktop/3990/chris_t1_all_fast_firstseg.nii.gz"
mask2_path = "/Users/nakulpandya/Desktop/3990/chris_t1_defaced_all_fast_firstseg.nii.gz"

# define folder paths with label folders for each file
mask1_folder =  "/Users/nakulpandya/Desktop/3990/data/segmentation/original"
mask2_folder = "/Users/nakulpandya/Desktop/3990/data/segmentation/defaced/"

# compute and print Dice coefficient
dice_score = compute_dice_coefficient(mask1_path, mask2_path)
print(f"Dice Coefficient: {dice_score}")