from io import BytesIO

import numpy as np
import requests
from PIL import Image
import torch

image_url = "https://midjourney-plus.oss-us-west-1.aliyuncs.com/sora/8d079ede-b14b-48b0-b68f-5c2791eec722.png"

# 下载图片
img_resp = requests.get(image_url)
img_resp.raise_for_status()
img = Image.open(BytesIO(img_resp.content)).convert("RGB")

# PIL -> numpy H,W,3
img_array = np.array(img, dtype=np.float32) / 255.0  # 归一化到 [0,1]
print(img_array.shape)  # 应该是 (1024,1024,3)
# numpy -> Tensor C,H,W
img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)  # (C,H,W)

print(img_tensor)
print(img_tensor[0].shape)
print(img_tensor.shape)
pass