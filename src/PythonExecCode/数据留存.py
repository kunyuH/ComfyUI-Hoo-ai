import json

# param_text1 是需要留存的字符 key
# param_text2 是需要留存的数据 是一个字符串

if not param_text1:
 param_text1 = 'save_data'

result_text1 = "hoo_save:"+json.dumps({
param_text1:param_text2
}, ensure_ascii=False, indent=4)