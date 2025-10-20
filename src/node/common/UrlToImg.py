import re
import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np
import json

from ...utils.tools import is_json


class UrlToImg:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url_matches": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "extract_images"
    CATEGORY = "Semir Hoo ai / Common"

    def extract_images(self, url_matches):
        print("####### UrlToImg input ########")
        print(url_matches)
        if is_json(url_matches):
            url_matches = json.loads(url_matches)
        else:
            url_matches = [url_matches]

        img_tensors = []
        # 处理多张图片
        for url in url_matches:
            # 下载图片
            img_resp = requests.get(url)
            img_resp.raise_for_status()
            img = Image.open(BytesIO(img_resp.content)).convert("RGB")

            # PIL -> numpy H,W,3
            img_array = np.array(img, dtype=np.float32) / 255.0

            # numpy -> Tensor H,W,3
            img_tensor = torch.from_numpy(img_array)  # (H,W,3)
            img_tensors.append(img_tensor)

        # 把所有图片堆叠成一个张量 [N, H, W, 3]，PreviewImage 可以识别
        stacked_tensor = torch.stack(img_tensors, dim=0)

        return (stacked_tensor.cpu(),)  # 注意必须返回元组

# 注册节点
NODE_CLASS_MAPPINGS = {"UrlToImg": UrlToImg}
NODE_DISPLAY_NAME_MAPPINGS = {"UrlToImg": "图片url转img数据"}
