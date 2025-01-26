import SimpleITK as sitk
import six
from radiomics import featureextractor
# from nipy.labs.mask import compute_mask_files

# # generate mask file
# compute_mask_files("chris_t1.nii", "chris_t1_mask.nii", return_mean=False, m=0.2, M=0.9, cc=1, exclude_zeros=False, opening=2)

# Load the input image and mask
imagePath = sitk.ReadImage("chris_t1.nii")
maskPath = sitk.ReadImage("chris_t1_mask.nii")

# Instantiate the extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor.enabledImagetypes)
print('Enabled features:\n\t', extractor.enabledFeatures)

result = extractor.execute(imagePath, maskPath)

print('Result type:', type(result))  # result is returned in a Python ordered dictionary)
print('')
print('Calculated features')
for key, value in six.iteritems(result):
    print('\t', key, ':', value)
