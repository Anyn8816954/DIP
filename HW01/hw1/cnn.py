import math
import torch
from torch import nn
import time


class ThirdPartyCNN(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        # TODO: Setting kernel and pooling shapes for each layer so that the input size is matched to the output size
        # Note: the shape setting should be exactly the same as your model
        # 先取得輸入影像的高、寬、通道數與指定輸出數量。架構設計為兩個卷積層，通道數分別由 3 轉成 4，再由 4 轉成 8。卷積使用 3×3 kernel、padding=1 和 stride=1，使高寬不變；pooling使用 2×2、stride=2，使每次池化後高寬減半

        height, width, channels = input_size
        output_count, _ = output_size

        # TODO: Initialize convolution kernel and pooling layers with API
        # 據前面決定的架構，使用 PyTorch 的 Conv2d 建立兩個卷積層，並由 API 初始化其 weight 與 bias。再使用 MaxPool2d 建立池化層，於每個 2×2 區塊取最大值。將 layers 保存為 self 的屬性，供 forward() 後續呼叫

        self.conv1 = nn.Conv2d(channels, 4, 3, padding=1)
        self.conv2 = nn.Conv2d(4, 8, 3, padding=1)
        self.pool = nn.MaxPool2d(2, stride=2)

        # TODO: Compute size of the flatten feature
        # 兩次pooling 後，高寬縮小為四分之一，且保留八個通道，所以 Flatten 長度為三者乘積

        self.flatten_size = 8 * (height // 4) * (width // 4)

        # TODO: Initialize the FCN parameters with randomized numbers
        # Linear 將特徵轉成指定輸出數量，參數由 PyTorch 初始化

        self.fc = nn.Linear(self.flatten_size, output_count)
        self.sigmoid = nn.Sigmoid()
        self.double()

    def forward(self, x):
        out = x
        # TODO: Generate the outputs through the network.
        # 輸入依序經過兩組卷積、sigmoid 與pooling，再保留 batch 維度將特徵攤平，最後通過全連接層與 sigmoid 產生輸出

        out = self.sigmoid(self.conv1(out))
        out = self.pool(out)
        out = self.sigmoid(self.conv2(out))
        out = self.pool(out)
        out = out.reshape(out.shape[0], -1)
        out = self.sigmoid(self.fc(out))
        return out


#sigmoid activation functions
class SigmoidActivation:
    def activate(self, z):
        out = z
        # TODO: Implement the sigmoid activation
        # 直接用 sigma(z) = 1/(1 + e^-z) 計算 sigmoid
        out = 1.0 / (1.0 + torch.exp(-out))
        return out


class ConvolutionalNeuralNetwork:
    def __init__(self, input_size, output_size):
        H, W, C = input_size
        N, _  =  output_size
        height, width, channels = H, W, C
        output_count = N
        # TODO: Setting shapes of convolution kernel, pooling and fcn  for each corresponding layer so that the input size is matched to the output size
        # TODO: Report the designed shapes of each layer in a table
        # 記錄每層輸出，檢查卷積、pooling、Flatten 與全連接層是否銜接。卷積保持高寬，pooling減半，Flatten 合併通道與空間維度

        self.layer_shapes = [
            ('Input', (1, channels, height, width)),
            ('Conv1 + sigmoid', (1, 4, height, width)),
            ('Pool1', (1, 4, height // 2, width // 2)),
            ('Conv2 + sigmoid', (1, 8, height // 2, width // 2)),
            ('Pool2', (1, 8, height // 4, width // 4)),
            ('Flatten', (1, 8 * (height // 4) * (width // 4))),
            ('FC + sigmoid', (1, output_count)),
        ]

        # TODO: Compute size of the flatten feature
        # 兩次池化後，影像高寬分別縮小為原本的四分之一，最後一個卷積層的輸出通道數為八。因此將八個通道的高寬相乘，得到 Flatten 後的特徵數，用來決定全連接層的輸入大小。

        self.flatten_size = 8 * (height // 4) * (width // 4)

        # Small random weights avoid making sigmoid outputs all near 0 or 1.
        # TODO: Initialize convolution kernel parameters with random numbers
        # 權重排列為「輸出通道、輸入通道、kernel 高、kernel 寬」。使用隨機值初始化，每個輸出通道另外有一個 bias。乘以 0.1 控制初始尺度，降低 sigmoid 飽和的機會

        self.weight1 = torch.randn(4, channels, 3, 3, dtype=torch.float64) * 0.1
        self.bias1 = torch.randn(4, dtype=torch.float64) * 0.1
        self.weight2 = torch.randn(8, 4, 3, 3, dtype=torch.float64) * 0.1
        self.bias2 = torch.randn(8, dtype=torch.float64) * 0.1

        # TODO: Initialize the FCN parameters with randomized numbers
        # 全連接層的權重大小設定為輸出神經元數量乘上 Flatten 特徵數，使每個輸出都能對全部特徵進行加權。使用隨機數初始化權重與 bias，並縮小初始數值尺度，降低後續 sigmoid 飽和的情況

        self.fc_weight = torch.randn(output_count, self.flatten_size,
                                     dtype=torch.float64) / math.sqrt(self.flatten_size)
        self.fc_bias = torch.randn(output_count, dtype=torch.float64) * 0.1
        self.sigmoid = SigmoidActivation()



    def convolution(self, x, weight, bias, padding=1, stride=1):
        out = x
        # TODO: Implement the convolution using torch tensor (CANNOT directly use third party convolution API)
        # Note: Add zero-padding so that the output width/height equals the input width/height
        # 手動補零，再取出每個局部區塊，與所有輸出通道的權重相乘。對輸入通道及 kernel 高寬加總，加上 bias 得到輸出

        batch, channels, height, width = x.shape
        out_channels, _, kernel_h, kernel_w = weight.shape
        padded = x.new_zeros(batch, channels, height + 2 * padding,
                             width + 2 * padding)
        padded[:, :, padding:padding + height, padding:padding + width] = x
        out_h = (height + 2 * padding - kernel_h) // stride + 1
        out_w = (width + 2 * padding - kernel_w) // stride + 1
        out = x.new_zeros(batch, out_channels, out_h, out_w)

        # Conv2d uses cross-correlation: multiply without flipping the kernel.
        for y in range(out_h):
            for col in range(out_w):
                region = padded[:, :, y * stride:y * stride + kernel_h,
                                col * stride:col * stride + kernel_w]
                products = region.unsqueeze(1) * weight.unsqueeze(0)
                out[:, :, y, col] = products.sum(dim=(2, 3, 4)) + bias
        return out

    def maxpool(self, x, pool_size, pool_stride):
        out = x
        # TODO: Implement max pooling using torch tensor (CANNOT directly use third party pooling API)
        # 依照 pooling 大小與 stride 取出區塊，再對高寬取最大值。Batch 和通道分開保留，不混合不同影像或 feature maps

        batch, channels, height, width = x.shape
        out_h = (height - pool_size) // pool_stride + 1
        out_w = (width - pool_size) // pool_stride + 1
        out = x.new_zeros(batch, channels, out_h, out_w)
        for y in range(out_h):
            for col in range(out_w):
                region = x[:, :, y * pool_stride:y * pool_stride + pool_size,
                           col * pool_stride:col * pool_stride + pool_size]
                out[:, :, y, col] = region.amax(dim=(2, 3))
        return out

    def forward(self, x):
        out = x
        # TODO: Generate the outputs through the network.
        # 依序執行兩組卷積、sigmoid 和 pooling，再 Flatten 成特徵向量。全連接層以矩陣乘法與 bias 計算輸出，最後經 sigmoid。每個步驟的輸出都是下一個步驟的輸入

        out = self.convolution(out, self.weight1, self.bias1)
        out = self.sigmoid.activate(out)
        out = self.maxpool(out, 2, 2)
        out = self.convolution(out, self.weight2, self.bias2)
        out = self.sigmoid.activate(out)
        out = self.maxpool(out, 2, 2)
        out = out.reshape(out.shape[0], -1)
        out = out @ self.fc_weight.T + self.fc_bias
        out = self.sigmoid.activate(out)
        return out
