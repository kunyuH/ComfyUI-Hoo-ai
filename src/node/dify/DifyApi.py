import json

import requests

class DifyApi:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "api_url": ("STRING", {"default": ""}),
                "content": ("STRING", {"multiline": True,"default": "[]"}),
                "model": ("STRING", {"default": "gpt-4o-image"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Semir Hoo ai"

    def generate(self, **kwargs):
        api_key = kwargs.get("api_key")
        api_url = kwargs.get("api_url")
        model = kwargs.get("model", "gpt-4o-image")
        content = kwargs.get("content","[]")
        # json字符串转字典
        content = json.loads(content)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "stream":True
        }

        print("=== Dify Stream Start ===")
        try:
            with requests.post(api_url, headers=headers, json=payload, stream=True, timeout=300) as r:
                r.raise_for_status()
                collected = ""

                for line in r.iter_lines(decode_unicode=False):  # 不让 requests 自动解码
                    if not line:
                        continue

                    # 判断类型后手动解码
                    if isinstance(line, bytes):
                        try:
                            line = line.decode("utf-8", errors="ignore")
                        except Exception as e:
                            print(f"解码失败: {e}")
                            continue

                    if not line.startswith("data:"):
                        continue

                    data = line[len("data:"):].strip()
                    if data == "[DONE]":
                        break

                    try:
                        j = json.loads(data)
                        delta = j.get("choices", [{}])[0].get("delta", {})
                        if "content" in delta:
                            print(delta["content"], end="", flush=True)
                            collected += delta["content"]
                    except Exception as e:
                        print(f"解析流失败: {e}")

                print("\n=== Dify Stream Done ===")
        except Exception as e:
            print(f"请求异常: {e}")
            return (None,)
        return (collected,)

# 注册节点
NODE_CLASS_MAPPINGS = {"DifyApi": DifyApi}
NODE_DISPLAY_NAME_MAPPINGS = {"DifyApi": "Dify 图文生图 API"}
