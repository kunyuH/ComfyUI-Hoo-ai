import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np

"""
图片url读取与展示
支持多张
"""
class MultiImageURLNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "urls": ("STRING", {"multiline": True}),  # 每行一个 URL
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_imagesw"
    CATEGORY = "Semir Hoo ai"

    """
    单张
    """
    def load_imagesx(self, **kwargs):
        urls = kwargs.get("urls", "").splitlines()
        image_url = urls[0]

        # 下载图片
        img_resp = requests.get(image_url)
        img_resp.raise_for_status()
        img = Image.open(BytesIO(img_resp.content)).convert("RGB")

        # PIL -> numpy H,W,3
        img_array = np.array(img)  # (H, W, 3)

        # numpy -> Tensor [1, H, W, 3]，加 batch 维度
        img_tensor = torch.from_numpy(img_array[None, ...]).float() / 255.0

        return (img_tensor.cpu(),)  # 注意必须返回元组
    """
    多张
    """
    def load_imagesw(self, **kwargs):
        urls = kwargs.get("urls", "").splitlines()

        img_tensors = []
        for image_url in urls:
            image_url = image_url.strip()
            if not image_url:
                continue
            # 下载图片
            img_resp = requests.get(image_url)
            img_resp.raise_for_status()
            img = Image.open(BytesIO(img_resp.content)).convert("RGB")

            # PIL -> numpy H,W,3
            # img_array = np.array(img)  # (H, W, 3)

            # numpy -> Tensor [1, H, W, 3]，加 batch 维度
            # img_tensor = torch.from_numpy(img_array[None, ...]).float() / 255.0
            # img_tensors.append(img_tensor.cpu())

            # PIL -> numpy H,W,3
            img_array = np.array(img, dtype=np.float32) / 255.0

            # numpy -> Tensor H,W,3
            img_tensor = torch.from_numpy(img_array)  # (H,W,3)
            img_tensors.append(img_tensor)

        # 把所有图片堆叠成一个张量 [N, H, W, 3]，PreviewImage 可以识别
        stacked_tensor = torch.stack(img_tensors, dim=0)

        return (stacked_tensor.cpu(),)  # 注意必须返回元组

# 注册节点
NODE_CLASS_MAPPINGS = {"MultiImageURLNode": MultiImageURLNode}
NODE_DISPLAY_NAME_MAPPINGS = {"MultiImageURLNode": "Multi Image URL Node"}

# urls = """https://midjourney-plus.oss-us-west-1.aliyuncs.com/sora/886430d8-cefa-4842-b1bf-b47e10a76fbe.png
# https://midjourney-plus.oss-us-west-1.aliyuncs.com/sora/69708920-70a6-433c-be0c-61914c5f9996.png
# """
# xx = MultiImageURLNode().load_images(urls=urls)
# xxx = MultiImageURLNode().load_imagesx(urls=urls)
# xxw = MultiImageURLNode().load_imagesw(urls=urls)
# pass