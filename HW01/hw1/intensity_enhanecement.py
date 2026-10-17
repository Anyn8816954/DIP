import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from spatial_operations import *

# Create output folder if not exist
folder_out = "results"
if not os.path.exists(folder_out):
    os.makedirs(folder_out)

# Demo Gamma Enhancement
# Load the test image
input_image = cv2.imread('images/brian-pennington.jpeg')

# Convert input image to grayscale image
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# TODO: Use 'gamma_transform' to update the output image such that the overexposure of the tower and people can be reduced. Report your parameter value (c and gamma) in the report.
# TODO: Attach the output image in your report.
# TODO: Provide at least three other cases to demonstrate and report the gamma enhancement
# 選擇 c=1、gamma=2 壓低中高灰階亮度，降低鐵塔與人物的過亮感
# 照片在results的資料夾中 參數: (c, gamma) dark:(1, 0.5) normal:(1, 1.5) bright:(1, 2)


output_image = gamma_transform(input_image, c=1.0, gamma=2.0)

# Write results to the folder
cv2.imwrite(folder_out+'/brian-pennington-gray.png', input_image)
cv2.imwrite(folder_out+'/gamma-enhancement.png', output_image)

# Test a dark outdoor image
dark_image = cv2.imread("images/gamma_dark.jpg")
dark_image = cv2.cvtColor(dark_image, cv2.COLOR_BGR2GRAY)

# gamma < 1 brightens a dark image
dark_output = gamma_transform(dark_image, c=1.0, gamma=0.5)

cv2.imwrite(folder_out + "/gamma-dark-gray.png", dark_image)
cv2.imwrite(folder_out + "/gamma-dark-enhanced.png", dark_output)


# Test an overexposed image
bright_image = cv2.imread("images/gamma_bright.jpg")
bright_image = cv2.cvtColor(bright_image, cv2.COLOR_BGR2GRAY)

# gamma > 1 darkens an overexposed image
bright_output = gamma_transform(bright_image, c=1.0, gamma=2.0)

cv2.imwrite(folder_out + "/gamma_bright-gray.png", bright_image)
cv2.imwrite(folder_out + "/gamma_bright-enhanced.png", bright_output)


# Test a normally exposed image
normal_image = cv2.imread("images/gamma_normal.jpg")
normal_image = cv2.cvtColor(normal_image, cv2.COLOR_BGR2GRAY)

# Slightly darken the normally exposed image
normal_output = gamma_transform(normal_image, c=1.0, gamma=1.5)

cv2.imwrite(folder_out + "/gamma_normal-gray.png", normal_image)
cv2.imwrite(folder_out + "/gamma_normal-enhanced.png", normal_output)

# Demo histogram equalization
# Load input test image
input_image = cv2.imread('images/dark.jpg')

# Convert input image to grayscale image
input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

# Note: You CANNOT use 3rd party histogram equalization API, must implement the transformation formula inside your function 
# TODO: Attach the output image in your report.
# 圖片也在results裡面

output_image = histogram_equalization(input_image)

# Write results to the folder
cv2.imwrite(folder_out+'/dark-gray.png', input_image)
cv2.imwrite(folder_out+'/equalized.png', output_image)
