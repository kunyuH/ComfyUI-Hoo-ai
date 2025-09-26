import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np

class CustomAIImageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"default": ""}),
                "api_url": ("STRING", {"default": ""}),
                "n": ("INT", {"default": 1}),
                "model": ("STRING", {"default": "gpt-image-1"}),  # 可用 "gpt-4o-mini" 或 "gpt-4.1-mini" 等
                "size": ("STRING", {"default": "1024x1024"}),    # 可选 "256x256", "512x512", "1024x1024"
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "Custom Nodes"

    def generate(self, **kwargs):
        prompt = kwargs.get("prompt")
        api_key = kwargs.get("api_key")
        api_url = kwargs.get("api_url")
        n = kwargs.get("n")
        model = kwargs.get("model", "gpt-4o-mini")
        size = kwargs.get("size", "1024x1024")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size
        }

        try:
            # 调用 OpenAI 官方 Images API
            resp = requests.post(f"{api_url}images/generations", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            image_url = data['data'][0]['url']

            # 下载图片
            img_resp = requests.get(image_url)
            img_resp.raise_for_status()
            img = Image.open(BytesIO(img_resp.content)).convert("RGB")

            # PIL -> numpy H,W,3
            img_array = np.array(img)  # (H, W, 3)

            # numpy -> Tensor [1, H, W, 3]，加 batch 维度
            img_tensor = torch.from_numpy(img_array[None, ...]).float() / 255.0

            return (img_tensor.cpu(),)  # 注意必须返回元组

        except Exception as e:
            raise Exception(f"OpenAIImageNode Error: {str(e)}")

# 注册节点
NODE_CLASS_MAPPINGS = {"OpenAIImageNode": CustomAIImageNode}
NODE_DISPLAY_NAME_MAPPINGS = {"OpenAIImageNode": "OpenAI Image Node"}
