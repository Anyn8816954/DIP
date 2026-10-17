import cv2
import numpy as np
from spatial_operations import (convolution, box_filter, laplacian_filter,
                                sobel_filter, image_product, image_sum)
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from image_io import read_image, write_image
from spatial_operations import gamma_transform as original_gamma_transform


def gamma_transform(input_image, c=1.0, gamma=1.0, g=None):
    # Keep the teacher's g=0.5 call without changing the student's function.
    if g is not None:
        gamma = g
    return original_gamma_transform(input_image, c=c, gamma=gamma)


def enhance_image(image_path, folder_out):
    # Load input test image
    color_image = read_image(image_path)
    # Convert input image to grayscale image
    input_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    # Create output folder if not exist
    folder_out.mkdir(parents=True, exist_ok=True)

    # Enhance the input image through a series spatial operations
    laplacian_image = laplacian_filter(input_image)
    gradient_image = sobel_filter(input_image)
    smoothed_gradient_image = box_filter(gradient_image, 2)
    sharpened_image = image_sum(input_image, laplacian_image)
    mask_image = image_product(laplacian_image, smoothed_gradient_image) # 梯度較弱的位置少加一點細節，梯度較強的位置保留較多细節
    denoised_sharpened_image = image_sum(input_image, mask_image) # 把細節加回原圖
    gamma_enhanced_image = gamma_transform(denoised_sharpened_image,
                                          c=1, gamma=0.5)

    # TODO: Write your observation on report
    # 1. Compare laplacian_image and gradient image: comment their differences in figure details
    # 2. Compare laplacian_image and mask_image: comment their differences in figure details
    # 3. Compare input_image, sharpened_image and denoised_sharpened_image: comment their differences in figure details
    # 4. Test on another image 'wellcome-skull.png' and do the above comparisons.

    # Dump image
    names = ['0-gray', '1-laplacian', '2-gradient', '3-smoothed-gradient',
             '4-sharpened', '5-mask', '6-denoised_sharpened', '7-gamma-enhanced']
    images = [input_image, laplacian_image, gradient_image,
              smoothed_gradient_image, sharpened_image, mask_image,
              denoised_sharpened_image, gamma_enhanced_image]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    # Write image to the folder
    for name, image, ax in zip(names, images, axes.flat):
        write_image(folder_out / (name + '.png'), image)
        ax.imshow(image, cmap='gray', vmin=0, vmax=255)
        ax.set_title(name)
        ax.axis('off')
    fig.tight_layout()
    fig.savefig(folder_out / 'comparison.png', dpi=160)
    plt.close(fig)

    padded_image = np.pad(input_image, 1, mode='constant')
    write_image(folder_out / 'padded.png', padded_image)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.imshow(padded_image, cmap='gray', vmin=0, vmax=255)
    ax.set_title('Zero padding: one pixel on each side')
    ax.set_xlim(-3, min(24, padded_image.shape[1]))
    ax.set_ylim(min(24, padded_image.shape[0]), -3)
    fig.tight_layout()
    fig.savefig(folder_out / 'padding-detail.png', dpi=160)
    plt.close(fig)
    print('Finished:', image_path.name)


def convolution_example(folder_out):
    input_image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
    kernel = np.array([[-1, 1, 1], [-1, 1, 1], [1, 1, 1]], dtype=float) / 7
    output_image = convolution(input_image, kernel)
    expected = np.array([[-2, 3, 16], [1, 15, 33], [8, 21, 28]]) / 7
    np.testing.assert_allclose(output_image, expected, atol=1e-12)
    np.savetxt(folder_out / 'convolution-test.csv', output_image,
               delimiter=',', fmt='%.8f')
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    arrays = [input_image, kernel, np.pad(input_image, 1), output_image]
    titles = ['Input', 'Kernel', 'Zero-padded input', 'Convolution output']
    for ax, array, title in zip(axes, arrays, titles):
        ax.axis('off')
        ax.set_title(title)
        table = ax.table(cellText=[[f'{v:.4f}' for v in row] for row in array],
                         cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.8)
    fig.tight_layout()
    fig.savefig(folder_out / 'convolution-test.png', dpi=160)
    plt.close(fig)
    print('3x3 convolution test:\n', output_image)


def run_experiments():
    base = Path(__file__).resolve().parent
    report_folder = base / 'results' / 'medical'
    report_folder.mkdir(parents=True, exist_ok=True)
    convolution_example(report_folder)
    enhance_image(base / 'images' / 'pxhere-mouth.jpeg', report_folder / 'mouth')
    enhance_image(base / 'images' / 'wellcome-skull.png', report_folder / 'skull')


if __name__ == '__main__':
    run_experiments()
