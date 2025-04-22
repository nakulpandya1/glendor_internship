import nibabel as nib
import numpy as np
from nibabel.processing import resample_from_to
import pandas as pd
import os

def compute_dice_coefficient(mask1_path, mask2_path):
    img1 = nib.load(mask1_path)
    img2 = nib.load(mask2_path)

    # resample if needed to match dimensions
    if img1.shape != img2.shape or not np.allclose(img1.affine, img2.affine):
        print(f"Resampling {os.path.basename(mask2_path)} to match {os.path.basename(mask1_path)}")
        img2 = resample_from_to(img2, img1, order=0)

    mask1 = img1.get_fdata() > 0
    mask2 = img2.get_fdata() > 0

    intersection = np.sum(mask1 & mask2)
    total = np.sum(mask1) + np.sum(mask2)

    return (2 * intersection / total) if total > 0 else 0.0


def compute_dice(original_base, defaced_base, defacers, biomarkers, output_excel):
    all_tables = {}

    for label in biomarkers:
        original_folder = os.path.join(original_base, label)

        # get subject files
        original_files = sorted([
            f for f in os.listdir(original_folder)
            if f.endswith("_firstseg.nii.gz")
        ])

        # table to collect data
        biomarker_table = {}

        for f in original_files:
            subject = f.replace(f"_{label}_all_fast_firstseg.nii.gz", "")
            biomarker_table[subject] = {}

            orig_file = os.path.join(original_folder, f)

            for defacer in defacers:
                defaced_file = os.path.join(defaced_base.format(defacer=defacer), label, f)

                if not os.path.exists(defaced_file):
                    print(f" [Missing] {defacer}: {f}")
                    biomarker_table[subject][defacer] = None
                    continue

                dice = compute_dice_coefficient(orig_file, defaced_file)
                biomarker_table[subject][defacer] = round(dice, 4)

        # convert to DataFrame
        df = pd.DataFrame.from_dict(biomarker_table, orient="index")
        df.index.name = "Subject"
        all_tables[label] = df

    with pd.ExcelWriter(output_excel) as writer:
        for label, df in all_tables.items():
            df.to_excel(writer, sheet_name=label)

    print(f"\nDice scores saved to: {output_excel}")

original_base = "/Users/nakulpandya/Desktop/3990/data/input/segmentation/original"
defaced_base  = "/Users/nakulpandya/Desktop/3990/data/output_{defacer}/segmentation/original"

defacers = ["afni_deface", "afni_reface" "fsl_deface", "mri_deface", "mydeface", "pydeface", "quickshear"]
biomarkers = ["amygdala", "hippocampus", "thalamus"]

compute_dice(
    original_base=original_base,
    defaced_base=defaced_base,
    defacers=defacers,
    biomarkers=biomarkers,
    output_excel="/Users/nakulpandya/Desktop/3990/data/all_dice_scores_by_biomarker1.xlsx"
)


def compute_pve_dice(original_segmentation, defaced_segmentation, pve_classes=["pve_0", "pve_1", "pve_2"], output_excel="pve_dice_scores.xlsx"):
    all_results = {}

    for pve_class in pve_classes:
        print(f"\nProcessing: {pve_class}")

        original_folder = os.path.join(original_segmentation, pve_class)
        defaced_folder = os.path.join(defaced_segmentation, pve_class)

        subjects = sorted([
            f for f in os.listdir(original_folder)
            if f.endswith(".nii.gz")
        ])

        dice_scores = []

        for f in subjects:
            subject = f.replace(".nii.gz", "")
            orig_path = os.path.join(original_folder, f)
            defaced_path = os.path.join(defaced_folder, f)

            if not os.path.exists(defaced_path):
                print(f"  [Missing] {f} in defaced — skipping")
                continue

            dice = compute_dice_coefficient(orig_path, defaced_path)
            dice_scores.append({
                "Subject": subject,
                "Dice": round(dice, 4)
            })

        df = pd.DataFrame(dice_scores)
        all_results[pve_class] = df

    with pd.ExcelWriter(output_excel) as writer:
        for pve_class, df in all_results.items():
            df.to_excel(writer, sheet_name=pve_class, index=False)

    print(f"\nDice results saved to: {output_excel}")

original_segmentation = "/users/nakulpandya/Desktop/3990/data/original_segmentation/" 
defaced_segmentation = "/users/nakulpandya/Desktop/3990/data/defaced_segmentation/"

compute_pve_dice(
    original_segmentation=original_segmentation,
    defaced_segmentation=defaced_segmentation,
    pve_classes=["pve_0", "pve_1", "pve_2"],
    output_excel="/users/nakulpandya/Desktop/3990/data/pve_dice_scores.xlsx"
)


def compute_extraction_dice(original_base, defaced_base, defacers, output_excel):

    original_files = sorted([
        f for f in os.listdir(original_base)
        if f.endswith("_extraction.nii")
    ])

    results = {}

    
    results = {}
    for f in original_files:
        # strip off 'input_' prefix and '_extraction.nii' suffix
        subject = f[len("input_"):-len("_extraction.nii")]
        orig_path = os.path.join(original_base, f)

        row = {}
        for d in defacers:
            def_folder   = defaced_base.format(defacer=d)
            def_filename = f"{d}_{subject}_extraction.nii"
            def_path     = os.path.join(def_folder, def_filename)

            if not os.path.exists(def_path):
                print(f" [Missing] {f} in defaced — skipping")
                row[d] = None
            else:
                dice = compute_dice_coefficient(orig_path, def_path)
                row[d] = round(dice, 4)

        results[subject] = row

    df = pd.DataFrame.from_dict(results, orient="index")
    df.index.name = "Subject"
    df.to_excel(output_excel)
    print(f"\nDice comparison saved to: {output_excel}")

original_base = "/users/nakulpandya/Desktop/3990/data/extraction_input"
defaced_base = "/users/nakulpandya/Desktop/3990/data/extraction_{defacer}"

defacers = ["fsl", "afni", "mydeface", "quickshear", "pydeface", "mri"]

compute_extraction_dice(
    original_base=original_base,
    defaced_base=defaced_base,
    defacers=defacers,
    output_excel="/Users/nakulpandya/Desktop/3990/data/extraction_dice_results.xlsx"
)
