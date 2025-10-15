# CustomText.py
class CustomText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # "text": ("STRING", {"multiline": True}),
                "text": ("STRING", {"default": True}),
                "text2": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING","STRING")
    FUNCTION = "generate"
    CATEGORY = "Semir Hoo ai"

    def generate(self, **kwargs):
        # 获取输入文本
        text = kwargs.get("text")
        text2 = kwargs.get("text2")
        # 这里可以做文本处理、模板替换等
        return (text,text2)

# 注册节点
NODE_CLASS_MAPPINGS = {"CustomText": CustomText}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomText": "文本输入"}
