import json
import time
import requests

param_text1 = """
https://aigc-mj20.semirapp.com/api/v2/mj/task/1760689229012561/enhanced
"""
param_text2 = """
{
   "x-api-key":"mjpro_test_key_6jx8k9f2l1p3qrst",
   "Content-Type":"application/json"
}
"""

start_time = time.time()  # 记录开始时间
timeout = 60 * 20  # 最大循环时间为 20 分钟

while True:
    try:
        response = requests.get(
            url=param_text1,
            headers=json.loads(param_text2),
            timeout=60
        ).json()
        # 验证是否生成成功 成功则退出 不成功 则继续
        progress = response.get('data', {}).get('progress', 0)
        if progress == 100:
            result_text1 = response.get('data', {}).get('imageUrl', '')
            result_text2 = response.get('data', {}).get('thumbnailUrl', '')
            print("生成成功")
            # 生成成功 退出循环
            break
        if not response.get('success', False):
            result_text1 = ''
            result_text2 = ''
            # 有异常 退出循环
            break
        pass
    except Exception as e:
        print(e)

    # 判断是否超过 timeout 秒
    if time.time() - start_time > timeout:
        print(f"循环超过 {timeout} 秒，终止")
        break

    time.sleep(10)
