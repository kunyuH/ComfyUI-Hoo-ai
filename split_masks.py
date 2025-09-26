import torch
import numpy as np
from skimage import measure

class SplitSAMMasksNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"mask": ("MASK", )}}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("masks",)
    FUNCTION = "split_masks"
    CATEGORY = "custom"

    def split_masks(self, mask):
        print('=====================')
        print(mask)
        print(type(mask))
        print(mask.shape)
        print('=====================')
        # 1. 提取 tensor 或 numpy/PIL
        if isinstance(mask, dict) and "mask" in mask:
            mask_tensor = mask["mask"]
        else:
            mask_tensor = mask

        # 2. 转为 numpy array
        if isinstance(mask_tensor, torch.Tensor):
            arr = mask_tensor.detach().cpu().numpy()
        elif "PIL" in str(type(mask_tensor)):
            arr = np.array(mask_tensor)
        else:
            arr = np.array(mask_tensor)

        masks_list = []

        # 3. 处理不同形状
        if arr.ndim == 3:
            if arr.shape[0] < arr.shape[-1]:  # [N,H,W]
                for i in range(arr.shape[0]):
                    masks_list.append((arr[i] > 0.5).astype(np.uint8) * 255)
            else:  # [H,W,C]
                arr = arr[..., 0] if arr.shape[-1] > 1 else arr[..., 0]

        if arr.ndim == 2:
            arr_bin = (arr > 0.5).astype(np.uint8)
            labeled = measure.label(arr_bin, connectivity=1)
            for val in np.unique(labeled):
                if val > 0:
                    masks_list.append((labeled == val).astype(np.uint8) * 255)

        if not masks_list:  # 其他情况
            masks_list.append((arr > 0.5).astype(np.uint8) * 255)

        # 4. 转为 torch.Tensor 列表，shape=[1,H,W], 值在 [0,1]
        # masks_tensor_list = [torch.from_numpy(m).unsqueeze(0).float() / 255.0 for m in masks_list]
        masks_tensor_list = [torch.from_numpy(m).to(torch.uint8) for m in masks_list]
        return (masks_tensor_list,)
        # return (masks_tensor_list,)

# 注册节点
NODE_CLASS_MAPPINGS = {"SplitSAMMasksNode": SplitSAMMasksNode}
NODE_DISPLAY_NAME_MAPPINGS = {"SplitSAMMasksNode": "Split SAM Masks"}
