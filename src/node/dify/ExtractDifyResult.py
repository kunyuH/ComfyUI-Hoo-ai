import re
import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np
import json


class ExtractDifyResult:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dify_result": ("STRING", {"forceInput": True}),  # JSON 或 Markdown 字符串
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract_images"
    CATEGORY = "Semir Hoo ai"

    def extract_images(self, dify_result):
        """
        从 Dify API 富文本返回中提取图片 URL 并转换为 IMAGE_LIST
        """
        # 如果是 JSON 字符串
        if isinstance(dify_result, str):
            try:
                data = json.loads(dify_result)
            except Exception:
                # 不是 JSON，直接当文本处理
                data = {"text": dify_result}
        else:
            data = dify_result

        # 收集所有文本内容
        texts = []
        for key, val in data.items():
            if isinstance(val, str):
                texts.append(val)
            elif isinstance(val, list):
                texts.extend([str(v) for v in val])

        combined_text = "\n".join(texts)

        # 清理 JSON内容  防止把原图也拿出来
        combined_text = re.sub(r"json\s*(.*?)", r"\1", combined_text, flags=re.DOTALL)

        # 匹配 Markdown 图片 ![alt](url)
        url_matches = re.findall(r'!\[.*?\]\((https?://[^\s\)]+)\)', combined_text)
        # 匹配裸链接 png/jpg/jpeg
        url_matches += re.findall(r'(https?://[^\s\)]+?\.(?:png|jpg|jpeg))', combined_text)

        # 去重
        url_matches = list(set(url_matches))
        url_matches_json = json.dumps(url_matches, ensure_ascii=False)

        return (url_matches_json,)  # 注意必须返回元组

# 注册节点
NODE_CLASS_MAPPINGS = {"ExtractDifyResult": ExtractDifyResult}
NODE_DISPLAY_NAME_MAPPINGS = {"ExtractDifyResult": "Dify API 结果解析"}
