import base64
import io
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