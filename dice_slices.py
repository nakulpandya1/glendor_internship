import os
import nibabel as nib
import numpy as np
import pandas as pd
from nibabel.processing import resample_from_to

def load_nifti(filepath):
    return nib.load(filepath)

def get_slices(image_data, num_slices=16, axis=2):
    total_slices = image_data.shape[axis]
    slice_indices = np.linspace(0, total_slices - 1, num_slices, dtype=int)
    slices = [image_data[:, :, i] if axis == 2 
              else image_data[i, :, :] if axis == 0 
              else image_data[:, i, :]
              for i in slice_indices]
    return slices, slice_indices

def binarize(image, threshold=0.5):
    return (image > threshold).astype(np.uint8)

def dice_coefficient(mask1, mask2):
    intersection = np.sum((mask1 > 0) & (mask2 > 0))
    total_voxels = np.sum(mask1 > 0) + np.sum(mask2 > 0)
    return (2. * intersection / total_voxels) if total_voxels > 0 else 0.0

def compute_slicewise_dice(original_base, defaced_base, defacers, biomarkers, axis=2, output_excel=None):

    writer = pd.ExcelWriter(output_excel)

    for label in biomarkers:
        print(f"\nProcessing biomarker: {label}")
        original_folder = os.path.join(original_base, label)
        subject_files = sorted([f for f in os.listdir(original_folder) if f.endswith("_firstseg.nii.gz")])

        # dictionary of dataframes for each defacer
        defacer_slice_tables = {defacer: {} for defacer in defacers}
        slice_count = None

        for filename in subject_files:
            subject = filename.replace(f"_{label}_all_fast_firstseg.nii.gz", "")
            orig_path = os.path.join(original_folder, filename)

            orig_img = load_nifti(orig_path)
            orig_data = orig_img.get_fdata()
            if slice_count is None:
                slice_count = orig_data.shape[axis]

            # load defaced data
            for defacer in defacers:
                defaced_path = os.path.join(defaced_base.format(defacer=defacer), label, filename)
                if not os.path.exists(defaced_path):
                    print(f" [Missing] {defacer}: {filename}")
                    continue
                # resample defaced data to match original
                defaced_img = load_nifti(defaced_path)
                if orig_img.shape != defaced_img.shape or not np.allclose(orig_img.affine, defaced_img.affine):
                    print(f"Resampling {os.path.basename(defaced_path)} to match {os.path.basename(orig_path)}")
                    defaced_img = resample_from_to(defaced_img, orig_img, order=0)

                defaced_data = defaced_img.get_fdata()
                slice_dice_scores = []
                # compute dice score for each slice
                for i in range(slice_count):
                    if axis == 0:
                        orig_slice = orig_data[i, :, :]
                        defaced_slice = defaced_data[i, :, :]
                    elif axis == 1:
                        orig_slice = orig_data[:, i, :]
                        defaced_slice = defaced_data[:, i, :]
                    else:
                        orig_slice = orig_data[:, :, i]
                        defaced_slice = defaced_data[:, :, i]

                    dice = dice_coefficient(binarize(orig_slice), binarize(defaced_slice))
                    slice_dice_scores.append(dice)

                defacer_slice_tables[defacer][subject] = slice_dice_scores

        # save dataframes to excel
        for defacer, subject_dice in defacer_slice_tables.items():
            if not subject_dice:
                continue
            df = pd.DataFrame.from_dict(subject_dice, orient="index")
            df.columns = [f"Slice_{i}" for i in range(df.shape[1])]
            df.index.name = "Subject"
            sheet_name = f"{label}_{defacer}"
            df.to_excel(writer, sheet_name=sheet_name)

    writer.close()
    print(f"\nFull-slice Dice scores saved to: {output_excel}")


original_base = "/Users/nakulpandya/Desktop/3990/data/reoriented_input/segmentation/original"
defaced_base = "/Users/nakulpandya/Desktop/3990/data/output_{defacer}/segmentation/original"

defacers = ["afni_deface", "afni_reface" "fsl_deface", "mri_deface", "mydeface", "pydeface", "quickshear"]
biomarkers = ["amygdala", "hippocampus", "thalamus"]

compute_slicewise_dice(
    original_base=original_base,
    defaced_base=defaced_base,
    defacers=defacers,
    biomarkers=biomarkers,
    axis=2,
    output_excel="/Users/nakulpandya/Desktop/3990/data/all_slicewise_dice_scores.xlsx"
)
