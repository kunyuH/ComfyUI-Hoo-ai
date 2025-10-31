# CustomText.py
class CustomText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Semir Hoo ai / Common"

    def generate(self, **kwargs):
        # 获取输入文本
        text = kwargs.get("text")
        # 这里可以做文本处理、模板替换等
        return (text,)

# 注册节点
NODE_CLASS_MAPPINGS = {"CustomText": CustomText}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomText": "文本输入 多行"}
