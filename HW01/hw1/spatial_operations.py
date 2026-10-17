import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def gamma_transform(input_image, c=1.0, gamma=1.0):
    output_image = input_image.copy() # Initialize output image
    # TODO: Implement the gamma enhancement
    #先將影像轉成浮點數並除以 255，使亮度落在 [0,1]。接著照s=cr^gamma 計算新的亮度，最後乘回 255、限制範圍，再轉成 uint8

    normalized_image = input_image.astype(np.float64) / 255.0
    output_image = c * (normalized_image ** gamma)
    output_image = np.clip(output_image * 255.0, 0, 255).astype(np.uint8)
    # Note: 
    # 1. You CANNOT use 3rd party gamma correction API, must implement the transformation formula inside your function 
    # 2. You should normalize image intensity value to [0, 1] before transformation and map back to [0, 255] after
    # transformation
    return output_image

def histogram_equalization(input_image):
    output_image = input_image.copy() # Initialize output image
    # TODO: Implement the histogram equalization funtion
    folder_out = "results"
    if not os.path.exists(folder_out):
        os.makedirs(folder_out)

    # Step 1: Compute normalized histogram 
    # 將二維影像攤成一維，統計各灰階的像素數，並保留灰階 0～255 的位置。再除以總像素數，得到每個灰階所占的比例，使 normalized histogram 的總和為 1
    histogram = np.bincount(input_image.ravel(), minlength=256)
    normalized_histogram = histogram / input_image.size

    # TODO: draw and report the ’normalized’ histogram and attach to the report
    # Hint: you can generate the figure by matplotlib (plt.bar)
    # 將各灰階的像素比例畫成長條圖，觀察原圖亮度集中在哪個範圍。橫軸是灰階，縱軸是比例 ,圖片在results裡面,檔名:histogram-input

    plt.bar(np.arange(256), normalized_histogram, width=1.0)
    plt.xlabel("Input intensity")
    plt.ylabel("Normalized frequency")
    plt.title("Normalized Input Histogram")
    plt.savefig(folder_out + "/histogram-input.png")
    plt.close()
    
    # Step 2: Compute the output intensity by the cumulative distribution function for each input intensity
    # 用cumsum() 計算累積分布函數 CDF，再乘以 255 並向下取整，建立輸入灰階到輸出灰階的映射。
    cumulative_distribution = np.cumsum(normalized_histogram)
    intensity_mapping = np.floor(255 * cumulative_distribution).astype(np.uint8)

    #TODO: draw and report the figure to show the mapping from input intensities to output intensities
    # 將 CDF 建立的映射畫成曲線，呈現各輸入灰階對應的新灰階, 圖片在results裡面,檔名:histogram-mapping

    plt.plot(np.arange(256), intensity_mapping)
    plt.xlabel("Input intensity")
    plt.ylabel("Output intensity")
    plt.title("Histogram Equalization Mapping")
    plt.savefig(folder_out + "/histogram-mapping.png")
    plt.close()

    # Step 3: Update pixel intensity of output image
    # 將映射表當作查詢表，依每個像素原本的灰階取得新灰階。
    output_image = intensity_mapping[input_image]

    # TODO: draw and report the ’normalized’ output histogram
    # 統計並顯示均衡化後的亮度比例，與輸入分布比, 圖片在results裡面,檔名:histogram-output

    output_histogram = np.bincount(output_image.ravel(), minlength=256)
    normalized_output_histogram = output_histogram / output_image.size
    plt.bar(np.arange(256), normalized_output_histogram, width=1.0)
    plt.xlabel("Output intensity")
    plt.ylabel("Normalized frequency")
    plt.title("Normalized Output Histogram")
    plt.savefig(folder_out + "/histogram-output.png")
    plt.close()

    return output_image

def convolution(input_image, kernel):
    #Assume the type of the input image is float
    output_image = input_image.copy()
    #Note: CANNOT use third party convolution API (e.g., np.convolve is not allowed).
    height, width = input_image.shape
    size = kernel.shape[0]
    if kernel.shape != (size, size) or size % 2 == 0:
        raise ValueError('The kernel must be a square with odd side length.')
    radius = size // 2
    #TODO: Padd the input image with zeros according to kernel size (i.e., assume kernel size is (2r+1)x(2r+1),
    #padd the image with width r horizontally and vertically). Attach the padded image to report.pdf
    # 確認 kernel 是奇數邊長的方形矩陣，再依半徑在影像四周補零。這樣能處理邊界位置並維持輸出大小；浮點數輸出可以保留小數與負值。

    padded_image = np.pad(input_image.astype(float), radius, mode='constant')
    output_image = np.zeros((height, width), dtype=float)

    flipped_kernel = kernel[::-1, ::-1] # 有點問題
    #TODO: Perform convolution on the padded image with two-level for loops
    # 遍歷影像的列與欄，每個位置取出局部區塊，與 kernel 逐項相乘後加總 (採數學上的卷積定義，先把 kernel 旋轉 180 度)

    for y in range(height):
        for x in range(width):
            region = padded_image[y:y + size, x:x + size]
            output_image[y, x] = np.sum(region * flipped_kernel)
    #TODO: Report a test output_image by convolution a test 3x3 input image with a test kernel to report.pdf:
    # The test input image:
    # [[1, 2, 3],
    #  [4, 5, 6],
    #  [7, 8, 9]]
    # The test kernel:
    # [
    #    [-1/7, 1/7, 1/7],
    #    [-1/7, 1/7, 1/7],
    #    [1/7, 1/7, 1/7]
    # ]
    return output_image
    
def box_filter(input_image, radius):
    output_image = input_image.copy().astype(float) # Initialize the output image
    output_image /= 255 # Scale image intensity to [0, 1]

    #TODO: Define the box kernel, report resulted box kernel in the report.pdf
    #Note: The size should be (2 * radius + 1) x (2 * radius + 1)
    #Note: The kernel should be normalized such that the sum of the kernel equals 1.
    #TODO: Call your implemented function convolution to get the filter results
    # 根據 radius 計算 kernel 大小，建立全為 1 的矩陣，再除以元素總數，使係數總和為 1。因此卷積得到的是局部平均。

    size = 2 * radius + 1
    kernel = np.ones((size, size), dtype=float) / (size * size)
    
    output_image = convolution(output_image, kernel)
    
    # Scale image intensity back to [0, 255]
    output_image *= 255

    # Convert the data type to uint8 for visualization
    output_image = output_image.astype(np.uint8)
    return output_image

def laplacian_filter(input_image):
    output_image = input_image.copy().astype(float) # Initialize the output image
    output_image /= 255 # Scale image intensity to [0, 1]

    #TODO: Define the 3x3 laplacian kernel, report resulted laplacian kernel in the report.pdf
    #Note: The size should be 3 x 3
    #Note: Please choose one of the two kernels with central weight be positives (see slides)
    #TODO: Call your implemented function convolution to get the filter results
    # 使用中心為正的八鄰居 Laplacian kernel。它比較中心與周圍像素，平坦區域反應較小，亮度快速變化處反應較大，可提取細節。

    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]], dtype=float)

    output_image = convolution(output_image, kernel)

    # Scale image intensity back to [0, 255]
    output_image *= 255

    # Clip the image value to [0, 255]
    output_image[output_image > 255] = 255
    output_image[output_image < 0] = 0

    # Convert the data type to uint8 for visualization
    output_image = output_image.astype(np.uint8)

    return output_image

def sobel_filter(input_image):
    output_image = input_image.copy().astype(float) # Initialize the output image
    output_image /= 255 # Scale image intensity to [0, 1]

    #TODO: Define the sobel kernels, report resulted kernel in the report.pdf
    #Note: Use 3x3 kernels, please see slides
    #Note: There should be two kernels, please see slides
    #TODO: Call your implemented function convolution to get the filter results
    #Note: Perform convolution on the input image with the two sobel kernels and then generate two filter result images gx and gy
    # 兩個 Sobel kernels 分別取得左右與上下方向的亮度變化。

    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]], dtype=float)
    kernel_y = np.array([[-1, -2, -1],
                         [ 0,  0,  0],
                         [ 1,  2,  1]], dtype=float)
    
    gx = convolution(output_image, kernel_x)
    gy = convolution(output_image, kernel_y) 

    #TODO: Derive the magnitude image.
    #Note: The intensity of the magnitude image: m(x,y) = sqrt(gx(x, y)^2+gy(x, y)^2)
    # 直接套用Note裡面的公式

    output_image = np.sqrt(gx ** 2 + gy ** 2)

    # Scale image intensity back to [0, 255]
    output_image *= 255

    # Clip the image value to [0, 255]
    output_image[output_image > 255] = 255

    # Convert the data type to uint8 for visualization
    output_image = output_image.astype(np.uint8)
    return output_image

def image_product(input_image_a, input_image_b):
    input_image_a = input_image_a.astype(float) 
    input_image_b = input_image_b.astype(float) 
    input_image_a /= 255 # Scale image intensity to [0, 1]
    input_image_b /= 255 # Scale image intensity to [0, 1]
    output_image = input_image_a.copy() # Initialize the output image
    #TODO: Perform elementwise product between two images.
    #Hint: You can use numpy API here.
    # 對相同位置的像素相乘

    output_image = input_image_a * input_image_b

    # Scale image intensity back to [0, 255]
    output_image *= 255

    # Convert the data type to uint8 for visualization
    output_image = output_image.astype(np.uint8)
    return output_image

def image_sum(input_image_a, input_image_b):
    input_image_a = input_image_a.astype(float) 
    input_image_b = input_image_b.astype(float) 
    input_image_a /= 255 # Scale image intensity to [0, 1]
    input_image_b /= 255 # Scale image intensity to [0, 1]
    output_image = input_image_a.copy() # Initialize the output image
    #TODO: Perform elementwise summation between two images.
    #Hint: You can use numpy API here.
    # 就直接相加

    output_image = input_image_a + input_image_b

    # Scale image intensity back to [0, 255]
    output_image *= 255

    # Clip the image value to [0, 255]
    output_image[output_image > 255] = 255

    # Convert the data type to uint8 for visualization
    output_image = output_image.astype(np.uint8)
    return output_image
