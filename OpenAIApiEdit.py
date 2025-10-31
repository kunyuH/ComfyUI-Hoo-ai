import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np

from .src.utils.tools import tensor_to_buffered


class OpenAIApiEdit:
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
            },
            "optional":{
                "image1": ("IMAGE", {"default": ""}),
                "image2": ("IMAGE", {"default": ""}),
                "mask": ("IMAGE", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "Semir Hoo ai"

    def generate(self, **kwargs):
        prompt = kwargs.get("prompt")
        image1 = kwargs.get("image1")
        image2 = kwargs.get("image2")
        mask = kwargs.get("mask")
        api_key = kwargs.get("api_key")
        api_url = kwargs.get("api_url")
        n = kwargs.get("n")
        model = kwargs.get("model", "gpt-4o-mini")
        size = kwargs.get("size", "1024x1024")

        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size
        }

        try:
            print("****************************")
            print(f"{api_url}images/edits")
            # 文生图
            if image1 is None and image2 is None and mask is None:
                print(f"===prompt to image===")
                headers['Content-Type'] = "application/json"
                # 调用 OpenAI 官方 Images API
                resp = requests.post(f"{api_url}images/generations", json=payload, headers=headers)
                resp.raise_for_status()
            # 图文生图
            else:
                print(f"===prompt and image to image===")
                files = []
                if image1 is not None:
                    image1_buffered = tensor_to_buffered(image1)
                    files.append(("image", ("upload.png", image1_buffered, "image/png")))
                if image2 is not None:
                    image2_buffered = tensor_to_buffered(image2)
                    files.append(("image", ("upload.png", image2_buffered, "image/png")))
                if mask is not None:
                    mask_buffered = tensor_to_buffered(mask)
                    files.append(("mask", ("mask.png", mask_buffered, "image/png")))
                resp = requests.post(f"{api_url}images/edits", data=payload, files=files, headers=headers, verify=False)
                resp.raise_for_status()
            print(resp.text)
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
                raise Exception(f"CustomAIImageNode API Error: 服务器内部错误，请检查API URL是否正确或稍后再试。详细错误: {str(e)};内容: {e.response.text}")
            else:
                raise Exception(f"CustomAIImageNode API Error: HTTP错误 {e.response.status_code}。请检查API密钥、URL和网络连接。详细错误: {str(e)}；内容: {e.response.text}")
        except requests.exceptions.RequestException as e:
            # 处理其他请求异常（如连接问题、超时等）
            raise Exception(f"CustomAIImageNode 网络错误: 无法连接到API服务器。请检查网络连接和API URL是否正确。详细错误: {str(e)}")
        except Exception as e:
            # 处理其他未知错误
            raise Exception(f"CustomAIImageNode 错误: {str(e)}")

# 注册节点
NODE_CLASS_MAPPINGS = {"CustomAIImageEditNode": OpenAIApiEdit}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomAIImageEditNode": "OpenAi 图文生图 API"}
