import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def load_nifti(filepath):
    # load and get data from nifti file
    nii_img = nib.load(filepath)
    return nii_img.get_fdata()

def get_slices(image, num_slices=16, axis=2):
    # extract slices
    total_slices = image.shape[axis]    
    # select evenly spaced indices using linspace
    slice_indices = np.linspace(0, total_slices - 1, num_slices, dtype=int)

    # extract slices depending on axis ( 0 = x sagittal slice, 1 = y coronal slice, 2 = z axial slice )
    # we are using axis = 2 for axial slices
    slices = [image[:, :, i] if axis == 2 
              else image[i, :, :] if axis == 0 
              else image[:, i, :]
              for i in slice_indices]
    
    return slices, slice_indices  # return list of extracted slices & their indices

# if the image shape is (256, 256, 160), and axis=2:
	# •	image[:, :, 0] → First axial slice (top of the brain)
	# •	image[:, :, 80] → Middle axial slice
	# •	image[:, :, 159] → Last axial slice (bottom of the brain)

def binarize(image, threshold=0.5):
    # binarize image using threshold - it works by setting all values below the threshold to 0 and all values above to 1
    return (image > threshold).astype(np.uint8)

def dice_coefficient(mask1, mask2):
    # compute intersection and total voxel count for dice coefficient
    intersection = np.sum((mask1 > 0) & (mask2 > 0))
    total_voxels = np.sum(mask1 > 0) + np.sum(mask2 > 0)
    return ((2. * intersection) / total_voxels)

# load normal and defaced NIfTI images
normal_img = load_nifti("/Users/nakulpandya/Desktop/3990/chris_t1_all_fast_firstseg.nii.gz")
defaced_img = load_nifti("/Users/nakulpandya/Desktop/3990/chris_t1_defaced_all_fast_firstseg.nii.gz")

print(normal_img.shape)
# extract the slices from each image
normal_slices, slice_indices = get_slices(normal_img, num_slices=16)
defaced_slices, slice_indices = get_slices(defaced_img, num_slices=16)

# Compute Dice scores for each slice
dice_scores = []
for normal_slice, defaced_slice in zip(normal_slices, defaced_slices):
    # binarize both images
    normal_mask = binarize(normal_slice)
    defaced_mask = binarize(defaced_slice)

    # Dice similarity
    dice = dice_coefficient(normal_mask, defaced_mask)
    dice_scores.append(dice)

# print Dice scores for each slice
for idx, score in zip(slice_indices, dice_scores):
    print(f"Slice {idx}: Dice Coefficient = {score:.4f}")

# plot Dice scores across slices
plt.figure(figsize=(10, 5))
plt.plot(slice_indices, dice_scores, marker='o', linestyle='-', color='r')
plt.xlabel("Slice Idx")
plt.ylabel("Dice Coefficient")
plt.title("Dice Similarity Across 16 Slices")
plt.grid(True)
plt.show()