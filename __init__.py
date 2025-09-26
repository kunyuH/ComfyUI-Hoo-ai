# __init__.py
from .CustomAIImageNode import CustomAIImageNode, NODE_CLASS_MAPPINGS as AI_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as AI_NameMap
from .CustomTextNode import CustomTextNode, NODE_CLASS_MAPPINGS as Text_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Text_NameMap
from .MultiImageURLNode import MultiImageURLNode, NODE_CLASS_MAPPINGS as Multi_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Multi_NameMap

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {**AI_NodeMap, **Text_NodeMap, **Multi_NodeMap}
NODE_DISPLAY_NAME_MAPPINGS = {**AI_NameMap, **Text_NameMap, **Multi_NameMap}