import json
import time
import requests

param_text1 = "https://aigc-mj20.semirapp.com/api/v2/mj/task/1761214091950304/enhanced"
param_text2 = """
{
   "x-api-key":"mjpro_test_key_**********",
   "Content-Type":"application/json"
}
"""

start_time = time.time()  # 记录开始时间
timeout = 60 * 5  # 最大循环时间为 5 分钟

error = 2       # 异常重试次数
error_num = 0

while True:
    try:
        response = requests.get(
            url=param_text1,
            headers=json.loads(param_text2),
            timeout=60
        ).json()
        # 验证是否生成成功 成功则退出 不成功 则继续
        status = response.get('data', {}).get('status')
        if status == "SUCCESS":
            imgs = []
            imgs_list = response.get('data', {}).get('imgs', [])
            for img in imgs_list:
                imgs.append(img.get('imageUrl', ''))
            # 收集到生成的所有图片 返回 用于节点展示
            result_text1 = json.dumps(imgs, ensure_ascii=False, indent=4)
            # 返回完整的数据 入库时 会特殊处理
            result_text2 = json.dumps(imgs_list, ensure_ascii=False, indent=4)
            print("生成成功")
            # 生成成功 退出循环
            break
        if status == "FAILURE":
            result_text1 = ''
            result_text2 = ''
            # 有异常 退出循环
            raise Exception(f"有异常，收到的返回：{str(response)}")
        if not response.get('success', False):
            result_text1 = ''
            result_text2 = ''
            # 有异常 退出循环
            raise Exception(f"有异常，收到的返回：{str(response)}")
        pass
    except Exception as e:
        print(e)
        error_num += 1
        if error_num > error:
            print("连续错误次数超过限制，退出")
            raise Exception(e)
        break

    # 判断是否超过 timeout 秒
    if time.time() - start_time > timeout:
        print(f"循环超过 {timeout} 秒，终止")
        break

    time.sleep(10)