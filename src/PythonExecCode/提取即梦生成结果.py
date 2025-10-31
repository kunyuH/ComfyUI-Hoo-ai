import json

from src.utils.tools import is_json

# param_text1 = """
# """
result = []
if is_json(param_text1):
    urls = json.loads(param_text1)['data']
    for url in urls:
        result.append(url['url'])
    if not result:
        raise Exception(f'即梦返回没有图片，返回原始内容：{param_text1}')
    # 返回所有图片链接
    result_text1 = json.dumps(result, ensure_ascii=False)

else:
    raise Exception(f'即梦返回异常，返回原始内容：{param_text1}')

pass