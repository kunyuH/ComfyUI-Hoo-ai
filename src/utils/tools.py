import base64
import io
import json
import math

from PIL import Image

def tensor_to_base64(image_tensor, with_prefix=False):
    # 1. 转 NumPy
    image_np = (image_tensor.contiguous() * 255).clamp(0, 255).byte().cpu().numpy()
    # 形状: (B, H, W, C)

    # 2. 取 batch 里第一张 (B=1时)
    img = image_np[0]  # shape: (H, W, C)

    # 3. 转 PIL 图像
    pil_img = Image.fromarray(img)

    # 4. 转成字节流
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")  # 也可以改成 "JPEG"
    img_bytes = buffered.getvalue()

    # 5. 转 Base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    if with_prefix:
        return f"data:image/png;base64,{img_base64}"
    return img_base64

def tensor_to_buffered(image_tensor):
    # 1. 转 NumPy
    image_np = (image_tensor.contiguous() * 255).clamp(0, 255).byte().cpu().numpy()
    img = image_np[0]  # 取 batch 中第一张 (H,W,C)

    # 2. 转 PIL
    pil_img = Image.fromarray(img)

    # 3. 转字节流
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    buffered.seek(0)

    return buffered


def to_int(value):
    try:
        return int(value)
    except:
        return value


def is_number(num):
    try:
        float(num)
        return True
    except (ValueError, TypeError):
        return False


def is_nan(value):
    try:
        return math.isnan(value)
    except:
        return False

def empty(value):
    if is_nan(value):
        return True
    if value is None:
        return True
    if value is False:
        return True
    if isinstance(value, (str, list, tuple, dict, set)) and len(value) == 0:
        return True
    if isinstance(value, (int, float)) and value == 0:
        return True
    if isinstance(value, str) and value.strip() == "0":
        return True
    return False

def is_json(s):
    if not isinstance(s, str):
        return False
    try:
        obj = json.loads(s)
        return isinstance(obj, (dict, list))  # 确保是对象或数组
    except json.JSONDecodeError:
        return False

def is_lambda(obj):
    return callable(obj)