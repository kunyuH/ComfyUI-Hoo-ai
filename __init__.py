# __init__.py
from .OpenAIApi import OpenAIApi, NODE_CLASS_MAPPINGS as AI_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as AI_NameMap
from .OpenAIApiEdit import OpenAIApiEdit, NODE_CLASS_MAPPINGS as AI_EDIT_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as AI_EDIT_NameMap
from .CustomText import CustomText, NODE_CLASS_MAPPINGS as Text_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Text_NameMap
from .MultiImageURLNode import MultiImageURLNode, NODE_CLASS_MAPPINGS as Multi_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Multi_NameMap

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {**AI_NodeMap,**AI_EDIT_NodeMap, **Text_NodeMap, **Multi_NodeMap}
NODE_DISPLAY_NAME_MAPPINGS = {**AI_NameMap,**AI_EDIT_NameMap, **Text_NameMap, **Multi_NameMap}