import nibabel
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import os

# load nifti file
brain_vol1 = nibabel.load("chris_t1.nii")
brain_vol2 = nibabel.load("chris_t1_defaced.nii")

# use NiBabel to read in the NIfTI file just created
type(brain_vol1)
nibabel.nifti1.Nifti1Image

type(brain_vol2)
nibabel.nifti1.Nifti1Image

# # view metadata
# print(brain_vol1.header)
# print(brain_vol2.header)

# access data in the nifti file
brain_vol1_data = brain_vol1.get_fdata()
type(brain_vol1_data)

brain_vol2_data = brain_vol2.get_fdata()
type(brain_vol2_data)

# visualize a slice
#for brain_vol1
plt.imshow(brain_vol1_data[96], cmap='bone')
plt.axis('off')
plt.show()

#for brain_vol2
plt.imshow(brain_vol2_data[96], cmap='bone')
plt.axis('off')
plt.show()

# visualize a series of slices
#for brain_vol1
fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol1_data.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = int((n_slice - plot_range) / 2)

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(ndi.rotate(brain_vol1_data[img, :, :], 90), cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()

#for brain_vol2
fig_rows = 4
fig_cols = 4
n_subplots = fig_rows * fig_cols
n_slice = brain_vol2_data.shape[0]
step_size = n_slice // n_subplots
plot_range = n_subplots * step_size
start_stop = int((n_slice - plot_range) / 2)

fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

for idx, img in enumerate(range(start_stop, plot_range, step_size)):
    axs.flat[idx].imshow(ndi.rotate(brain_vol2_data[img, :, :], 90), cmap='gray')
    axs.flat[idx].axis('off')
        
plt.tight_layout()
plt.show()
