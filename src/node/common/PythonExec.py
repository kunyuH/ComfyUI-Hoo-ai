# -*- coding: utf-8 -*-
import os, sys

# 获取当前文件所在的 ComfyUI-Hoo-ai 根目录
# 因为自定义的代码 需要引入内部其他包
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)

class PythonExecNode:
    """
    🌟 通用 Python 执行节点
    - 支持从上一个节点或内部输入执行 Python 代码
    - 返回三个值：执行结果、异常信息、状态
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "code_input": ("STRING", {
                    "multiline": True,
                    "default": "# 在这里写 Python 代码\nresult = 'Hello ComfyUI!'"
                })
            },
            "optional": {
                "param_text1": ("STRING", {"default": "", "forceInput": True}),
                "param_text2": ("STRING", {"default": "", "forceInput": True}),
                "param_bool": ("BOOLEAN", {"default": False , "forceInput": True}),
                "param_image": ("IMAGE", {"default": None}),
                "param_tensor": ("TENSOR", {"default": None}),
            }
        }

    RETURN_TYPES = ("STRING","STRING", "BOOLEAN", "IMAGE", "TENSOR", "STRING", "STRING")
    RETURN_NAMES = ("result_text1","result_text2","result_bool","result_image","result_tensor", "error", "status")
    FUNCTION = "run_python"
    CATEGORY = "Semir Hoo ai / Common"

    def run_python(self, **kwargs):
        """
        执行 Python 代码
        返回 result, error, status
        """
        code_input = kwargs.get("code_input")
        param_text1 = kwargs.get("param_text1")
        param_text2 = kwargs.get("param_text2")
        param_bool = kwargs.get("param_bool", False)
        param_image = kwargs.get("param_image")
        param_tensor = kwargs.get("param_tensor")

        # 如果 override_input 不为空，则优先执行它
        code_to_exec = code_input.strip()

        # 定义局部变量，传入 exec
        local_vars = {
            "param_text1": param_text1,
            "param_text2": param_text2,
            "param_bool": param_bool,
            "param_image": param_image,
            "param_tensor": param_tensor,
            "kwargs": kwargs,

            "result_text1": None,
            "result_text2": None,
            "result_bool": None,
            "result_image": None,
            "result_tensor": None
        }

        try:
            # 执行代码
            exec(code_to_exec, {}, local_vars)

            return (
                local_vars.get("result_text1"),
                local_vars.get("result_text2"),
                local_vars.get("param_bool"),
                local_vars.get("result_image"),
                local_vars.get("result_tensor"),
                "",
                "success"
            )

            # # 尝试获取变量 result
            # result = local_vars.get("result", "")
            # return (str(result), "", "success")

        except Exception:
            import traceback
            return (None, None, False, None, None, traceback.format_exc(), "error")


# 注册节点
NODE_CLASS_MAPPINGS = {
    "PythonExecNode": PythonExecNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PythonExecNode": "🐍 Python 逻辑块"
}


# 测试独立运行
if __name__ == "__main__":
    node = PythonExecNode()
    code = """
x = 10
y = 20
result = x + y
"""
    res = node.run_python(code)
    print(res)
