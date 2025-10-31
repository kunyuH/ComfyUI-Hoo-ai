import json
from src.utils.tools import is_json

param_text1 = """{
  "success": true,
  "message": "草图操作请求已提交",
  "data": {
    "code": 1,
    "description": "提交成功",
    "result": "1761879453200475",
    "properties": {
      "discordInstanceId": "1350050044434317346",
      "discordChannelId": "1350050044434317346"
    }
  },
  "timestamp": "2025-10-31 10:57:33"
}"""
# param_text2 = "https://aigc-mj20.semirapp.com/api/v2/mj/task/{id}/enhanced"

# 确认返回值
if is_json(param_text1):
    res_json = json.loads(param_text1)

    # 提取任务id
    task_id = res_json.get('data',{}).get('result')
    if not task_id:
        raise Exception("返回值中没有任务id")

    result_text1 = task_id
else:
    raise Exception("返回值不是json格式")