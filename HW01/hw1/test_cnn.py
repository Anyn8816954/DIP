from cnn import *
import random
from pathlib import Path
import time
import cv2
import torch
import torch.nn as nn
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cnn import ConvolutionalNeuralNetwork, ThirdPartyCNN
from image_io import read_image, write_image


def compare_outputs(custom, third):
    mse = 0
    # TODO: Compute the MSE of the two outputs
    # 將兩個輸出的差值平方後平均，得到 mean squared error。平方避免正負差異互相抵消；item() 將單一數值 tensor 轉成 Python 數字

    mse = torch.mean((custom - third) ** 2).item()
    return mse


def make_test_image(size):
    # Draw a simple test image with stripes, a rectangle and a circle.
    image = np.zeros((size, size, 3), dtype=np.uint8)
    for col in range(size):
        image[:, col] = (40 if (col // 12) % 2 == 0 else 160, 50, 80)
    cv2.rectangle(image, (size // 8, size // 8), (size // 2, size // 2),
                  (30, 210, 100), -1)
    cv2.circle(image, (3 * size // 4, 3 * size // 4), size // 6,
               (220, 100, 30), -1)
    return image


if __name__ == '__main__':
    custom_out = []
    third_out = []
    base = Path(__file__).resolve().parent
    folder_out = base / 'results' / 'cnn'
    folder_out.mkdir(parents=True, exist_ok=True)
    # One thread avoids overhead for the small tensor operations in our loops.
    torch.set_num_threads(1)
    cases = [('drawn-120', 120), ('drawn-160', 160),
             ('drawn-240', 240), ('photo-128', 128)]

    for name, size in cases:
        # TODO: Read an input image which the input size should range between 120 x 120 x 3 and 240 x 240 x 3
        # Note: Rearrange the input image as the format (B, C, H, W) to fit pytorch API, where B = batch (=1 here), C=image channels, H=image height, W=image width
        # 依案例名稱決定讀取照片或建立自製影像，使輸入尺寸符合範圍，並保存測試影像。接著將 BGR 轉成 RGB，正規化後轉成 torch tensor。使用 permute 將 (H,W,C) 改成 (C,H,W)，再加入 batch 維度，得到 (1,C,H,W)

        if name == 'photo-128':
            image = read_image(base / 'images' / 'gamma_normal.jpg')
            image = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
        else:
            image = make_test_image(size)
        height, width, channels = image.shape
        write_image(folder_out / (name + '-input.png'), image)
        # OpenCV reads BGR; use RGB, [0,1], then (B,C,H,W).
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        x = torch.from_numpy(rgb.astype(np.float64) / 255.0)
        x = x.permute(2, 0, 1).unsqueeze(0).contiguous()

        # TODO: Set the output size should range between 10 x 1 and 3 x 1
        # 根據案例設定 3、5 或 10 個輸出，並以 (output_count,1) 傳給兩個模型，使輸出符合指定範圍且能逐項比較。固定隨機 seed，讓初始權重可重現。

        if name == 'drawn-120':
            output_count = 3
        elif name == 'drawn-240':
            output_count = 10
        else:
            output_count = 5
        output_size = (output_count, 1)
        torch.manual_seed(7)

        # TODO: Create the model of your implemented network
        # 將輸入影像尺寸與指定輸出大小傳入自製 CNN，讓模型依尺寸計算 Flatten 特徵數，並建立卷積及全連接層參數
        custom = ConvolutionalNeuralNetwork((height, width, channels), output_size)

        # TODO: Compute the output of your model
        # 將输入 tensor 傳入自製模型的 forward，依序完成卷積、sigmoid、pooling及全連接運算，將結果存入 custom_out。使用 no_grad 關閉梯度紀錄，因為這次只進行前向比較；記錄執行前後的時間差，取得自製模型的運算時間。
        with torch.no_grad():
            start = time.perf_counter()
            custom_out = custom.forward(x)
            custom_seconds = time.perf_counter() - start

        # TODO: Create the model from third party API (pytorch)
        # 使用相同的輸入尺寸與輸出大小建立 PyTorch CNN，並將模型設定為 evaluation 模式
        third = ThirdPartyCNN((height, width, channels), output_size)
        third.eval()

        # TODO: Copy the weights of your model to the third party model
        # 將自製模型兩個卷積層及全連接層的 weight、bias 完整複製到 PyTorch 模型
        with torch.no_grad():
            third.conv1.weight.copy_(custom.weight1)
            third.conv1.bias.copy_(custom.bias1)
            third.conv2.weight.copy_(custom.weight2)
            third.conv2.bias.copy_(custom.bias2)
            third.fc.weight.copy_(custom.fc_weight)
            third.fc.bias.copy_(custom.fc_bias)

        # TODO: Compute the output of third party model
        # 同一個輸入 tensor x 傳入 PyTorch 模型。third(x) 會呼叫模型的 forward，使用第三方 layers 完成前向運算，再將結果存入 third_out，並記錄執行時間
        with torch.no_grad():
            start = time.perf_counter()
            third_out = third(x)
            third_seconds = time.perf_counter() - start

        assert custom_out.shape == (1, output_count)
        torch.testing.assert_close(custom_out, third_out, rtol=1e-9, atol=1e-10)
        # TODO: Report the MSE
        # 計算 MSE 與額外的最大絕對誤差，再把兩組輸出畫在同一張圖。橫軸是輸出神經元編號，縱軸是 sigmoid 值
    
        mse = compare_outputs(custom_out, third_out)
        max_error = torch.max(torch.abs(custom_out - third_out)).item()
        # Each row is one neuron, corresponding to the required Nx1 output vector.
        np.savetxt(folder_out / (name + '-custom-vector.txt'),
                   custom_out.numpy().reshape(-1, 1), fmt='%.15f')
        np.savetxt(folder_out / (name + '-pytorch-vector.txt'),
                   third_out.numpy().reshape(-1, 1), fmt='%.15f')
        np.savetxt(folder_out / (name + '-outputs.csv'),
                   np.column_stack([custom_out.numpy().ravel(), third_out.numpy().ravel()]),
                   delimiter=',', header='custom,pytorch', comments='', fmt='%.15f')
        lines = ['Layer | Shape (B,C,H,W or B,N)']
        lines += [f'{layer} | {shape}' for layer, shape in custom.layer_shapes]
        lines += [f'Output column vector: ({output_count}, 1)',
                  f'MSE: {mse:.12e}', f'Maximum absolute error: {max_error:.12e}',
                  f'Custom forward seconds: {custom_seconds:.4f}',
                  f'PyTorch forward seconds: {third_seconds:.4f}']
        (folder_out / (name + '-summary.txt')).write_text('\n'.join(lines), encoding='utf-8')
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(range(1, output_count + 1), custom_out.numpy().ravel(), 'o-', label='Custom')
        ax.plot(range(1, output_count + 1), third_out.numpy().ravel(), 'x--', label='PyTorch')
        ax.set_xlabel('Output neuron')
        ax.set_ylabel('Sigmoid output')
        ax.set_title(name + f' (MSE={mse:.2e})')
        ax.legend()
        fig.tight_layout()
        fig.savefig(folder_out / (name + '-comparison.png'), dpi=160)
        plt.close(fig)
        print(f'{name}: output={tuple(custom_out.shape)}, MSE={mse:.3e}, '
              f'max error={max_error:.3e}, custom={custom_seconds:.2f}s')

