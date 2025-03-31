import subprocess
import os

def get_voxel_statistics(image_path):

    if not os.path.exists(image_path):
        print(f"The file {image_path} does not exist.")
        return None

    try:
        # run fslstats to get the mean, standard deviation, range, and voxel count/volume
        result = subprocess.run(
            ["fslstats", image_path, "-M", "-S", "-R", "-v"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stats_output = result.stdout.decode('utf-8').strip().split() # to be able to read the output
        mean, stddev = float(stats_output[0]), float(stats_output[1])
        voxel_count, volume = int(float(stats_output[4])), float(stats_output[5])
        
        return {
            "mean": mean,
            "stddev": stddev,
            "voxel_count": voxel_count,
            "volume_mm3": volume
        }
    
    except subprocess.CalledProcessError as e:
        errorMessage = e.stderr.decode('utf-8') if e.stderr else str(e)
        print(f"Error running fslstats on {image_path}: {errorMessage}")
        return None

def compare_voxel_statistics(before_mask, after_mask, biomarker_type):

    print(f"\nComparing voxel statistics for biomarker type '{biomarker_type}':")
    
    before_stats = get_voxel_statistics(before_mask)
    after_stats = get_voxel_statistics(after_mask)
    
    if before_stats and after_stats:
        print(f"Voxel Statistics for {os.path.basename(before_mask)}:")
        print(f"Mean: {before_stats['mean']}, Stddev: {before_stats['stddev']}, "
              f"Voxels: {before_stats['voxel_count']}, Volume (mm³): {before_stats['volume_mm3']}")

        print(f"\nVoxel Statistics for {os.path.basename(after_mask)}:")
        print(f"Mean: {after_stats['mean']}, Stddev: {after_stats['stddev']}, "
              f"Voxels: {after_stats['voxel_count']}, Volume (mm³): {after_stats['volume_mm3']}")

        # calculates the differences
        mean_diff = after_stats['mean'] - before_stats['mean']
        stddev_diff = after_stats['stddev'] - before_stats['stddev']
        voxel_diff = after_stats['voxel_count'] - before_stats['voxel_count']
        volume_diff = after_stats['volume_mm3'] - before_stats['volume_mm3']

        print("\nComparison:")
        print(f"Mean difference: {mean_diff}")
        print(f"Standard Deviation difference: {stddev_diff}")
        print(f"Voxel count difference: {voxel_diff}")
        print(f"Volume difference (mm³): {volume_diff}")
    else:
        print("Could not extract voxel statistics for one or both images.")

# comparison for each biomarker type
if __name__ == "__main__":
    base_path = "/Users/nakulpandya/Desktop/3990/data/segmentation"

    biomarker_types = ["amygdala_all_fast_firstseg", "hippocampus_all_fast_firstseg", "thalamus_all_none_firstseg"] # can be changed

    for biomarker in biomarker_types:
        before_mask = f"{base_path}/chris_t1_{biomarker}.nii.gz"
        after_mask = f"{base_path}/chris_t1_defaced_{biomarker}.nii.gz"

        compare_voxel_statistics(before_mask, after_mask, biomarker)