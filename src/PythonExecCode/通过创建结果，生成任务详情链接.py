import json
from src.utils.tools import is_json

# param_text1 = """{
#   "success": true,
#   "message": "U Creative操作请求已提交",
#   "data": {
#     "code": 3,
#     "description": "无可用的账号实例",
#     "result": null,
#     "properties": {}
#   },
#   "timestamp": "2025-10-27 16:27:44"
# }"""
# param_text2 = "https://aigc-mj20.semirapp.com/api/v2/mj/task/{id}/enhanced"

# 确认返回值
if is_json(param_text1):
    res_json = json.loads(param_text1)

    # 提取任务id
    task_id = res_json['data']['result']
    if not task_id or task_id == 'null':
        raise Exception(f"有异常，没有任务id收到的返回：{param_text1}")

    result_text1 = param_text2.format(id=task_id)
    result_text2 = task_id