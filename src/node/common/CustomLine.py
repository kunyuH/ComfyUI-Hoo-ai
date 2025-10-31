
class CustomLine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": ''}),
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
NODE_CLASS_MAPPINGS = {"CustomLine": CustomLine}
NODE_DISPLAY_NAME_MAPPINGS = {"CustomLine": "文本输入 单行"}
