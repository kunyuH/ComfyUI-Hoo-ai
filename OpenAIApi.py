import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np

class OpenAIApi:
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
    CATEGORY = "Semir Hoo ai"

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

            img_tensors = []
            # 处理多张图片
            for item in data['data']:
                # 下载图片
                img_resp = requests.get(item['url'])
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

        except requests.exceptions.HTTPError as e:
            # 专门处理HTTP错误，提供更清晰的API访问问题提示
            if e.response.status_code == 500:
                raise Exception(f"CustomAIImageNode API Error: 服务器内部错误，请检查API URL是否正确或稍后再试。详细错误: {str(e)}")
            else:
                raise Exception(f"CustomAIImageNode API Error: HTTP错误 {e.response.status_code}。请检查API密钥、URL和网络连接。详细错误: {str(e)}")
        except requests.exceptions.RequestException as e:
            # 处理其他请求异常（如连接问题、超时等）
            raise Exception(f"CustomAIImageNode 网络错误: 无法连接到API服务器。请检查网络连接和API URL是否正确。详细错误: {str(e)}")
        except Exception as e:
            # 处理其他未知错误
            raise Exception(f"CustomAIImageNode 错误: {str(e)}")

# 注册节点
NODE_CLASS_MAPPINGS = {"CustomAIImageNode": OpenAIApi}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomAIImageNode": "OpenAi 文生图 API"}
