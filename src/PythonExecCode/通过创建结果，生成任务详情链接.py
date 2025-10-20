import json
from src.utils.tools import is_json

# 确认返回值
if is_json(param_text1):
    res_json = json.loads(param_text1)

    # 提取任务id
    task_id = res_json['data']['result']

    result_text1 = param_text2.format(id=task_id)
    result_text2 = task_id