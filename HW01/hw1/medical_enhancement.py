from spatial_operations import *

# Load input test image
input_image = cv2.imread('images/pxhere-mouth.jpeg')

# Convert input image to grayscale image
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Enhance the input image through a series spatial operations 
laplacian_image = laplacian_filter(input_image)
print('Finished Laplacian filtering.')
gradient_image = sobel_filter(input_image)
print('Finished Sobel filtering.')
smoothed_gradient_image = box_filter(gradient_image, 2)
print('Finished box filtering on gradient image.')
sharpened_image = image_sum(input_image, laplacian_image)
print('Finished adding laplacian image onto input image.')
mask_image = image_product(laplacian_image, smoothed_gradient_image)
print('Finished multiplying smoothed gradient image to Laplacian image to generate the mask.')
denoised_sharpened_image = image_sum(input_image, mask_image)
print('Finished adding the mask image to the input image.')
# Added: accept the teacher's g parameter without changing the original call.
from medical_experiments import gamma_transform
gamma_enhanced_image = gamma_transform(denoised_sharpened_image, c=1, g=0.5)
print('Finished gamma enhancement for the final image.')

# TODO: Write your observation on report
# 1. Compare laplacian_image and gradient image: comment their differences in figure details
# 2. Compare laplacian_image and mask_image: comment their differences in figure details
# 3. Compare input_image, sharpened_image and denoised_sharpened_image: comment their differences in figure details 
# 4. Test on another image 'wellcome-skull.png' and do the above comparisons.
# 尚未比較

# Dump image
# Create output folder if not exist
folder_out = "results"
if not os.path.exists(folder_out):
    os.makedirs(folder_out)
# Write image to the folder
cv2.imwrite(folder_out+'/0-gray.png', input_image)
cv2.imwrite(folder_out+'/1-laplacian.png', laplacian_image)
cv2.imwrite(folder_out+'/2-gradient.png', gradient_image)
cv2.imwrite(folder_out+'/3-smoothed-gradient.png', smoothed_gradient_image)
cv2.imwrite(folder_out+'/4-sharpened.png', sharpened_image)
cv2.imwrite(folder_out+'/5-mask.png', mask_image)
cv2.imwrite(folder_out+'/6-denoised_sharpened.png', denoised_sharpened_image)
cv2.imwrite(folder_out+'/7-gamma-enhanced.png', gamma_enhanced_image)


# Added: report figures and the second test image.
if __name__ == '__main__':
    from medical_experiments import run_experiments
    run_experiments()
