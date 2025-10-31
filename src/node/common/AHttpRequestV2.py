import json
import traceback

import requests

class AHttpRequestV2:
    """
    🌐 通用 HTTP 客户端节点
    支持 GET / POST / PUT / DELETE 等请求
    可自定义 headers / params / body
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "https://example.com/api"}),
                "method": (["GET", "POST", "PUT", "DELETE"], {"default": "GET"}),
                "headers": ("STRING", {
                    "multiline": True,
                    "default": "{\n  \"Content-Type\": \"application/json\"\n}"
                }),
                "params": ("STRING", {
                    "multiline": True,
                    "default": "{ }"
                }),
                "body": ("STRING", {
                    "multiline": True,
                    "default": "{ }"
                }),
                "timeout": ("INT", {"default": 60, "min": 1, "max": 600}),
            },
            "optional": {
                "hoo_stream": ("BOOL", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response_text", "status_code")
    FUNCTION = "do_request"
    CATEGORY = "Semir Hoo ai / Common"

    def do_request(self, url, method="GET", headers="{}", params="{}", body="{}", timeout=60, hoo_stream=False):
        """
        发起 HTTP 请求并返回响应内容
        """
        try:
            # 转换 headers / params / body
            def parse_json(s):
                if not s.strip():
                    return {}
                try:
                    return json.loads(s)
                except Exception:
                    print(f"[WARN] 非 JSON 字符串，将以文本形式发送: {s}")
                    return s

            headers = parse_json(headers)
            params = parse_json(params)
            data = parse_json(body)

            print(f"=== 🌐 HTTP Request ===\n→ URL: {url}\n→ Method: {method}")
            print(f"→ Headers: {headers}\n→ Params: {params}\n→ Body: {data}")

            # 选择请求方法
            method = method.upper()
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params if method == "GET" else None,
                json=data if isinstance(data, dict) else None,
                data=None if isinstance(data, dict) else data,
                timeout=timeout,
                stream=hoo_stream
            )

            # 处理响应
            status_code = str(response.status_code)
            if hoo_stream:
                result = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        print(line)
                        result += line + "\n"
            else:
                try:
                    result = json.dumps(response.json(), ensure_ascii=False, indent=2)
                    # result = response.json()
                except Exception:
                    result = response.text

            print(f"=== ✅ HTTP Response ({status_code}) ===")
            return (result, status_code)

        except Exception as e:
            err = f"请求异常: {str(e)}"
            print(traceback.format_exc())
            return (err, "ERROR")


# 注册节点
NODE_CLASS_MAPPINGS = {
    "AHttpRequestV2": AHttpRequestV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AHttpRequestV2": "🌐 HTTP 客户端v2"
}
