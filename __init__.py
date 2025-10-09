# __init__.py
from .src.node.dify.DifyApi import NODE_CLASS_MAPPINGS as DIFY_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as DIFY_NameMap
from .src.node.dify.ExtractDifyResult import NODE_CLASS_MAPPINGS as DifyResult_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as DifyResult_NameMap
from .src.node.dify.UrlToImg import NODE_CLASS_MAPPINGS as UrlToImg_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as UrlToImg_NameMap

from .OpenAIApi import NODE_CLASS_MAPPINGS as AI_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as AI_NameMap
from .OpenAIApiEdit import NODE_CLASS_MAPPINGS as AI_EDIT_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as AI_EDIT_NameMap
from .CustomText import NODE_CLASS_MAPPINGS as Text_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Text_NameMap
from .MultiImageURLNode import NODE_CLASS_MAPPINGS as Multi_NodeMap, NODE_DISPLAY_NAME_MAPPINGS as Multi_NameMap

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {**AI_NodeMap,**AI_EDIT_NodeMap, **Text_NodeMap, **Multi_NodeMap, **DIFY_NodeMap, **DifyResult_NodeMap, **UrlToImg_NodeMap}
NODE_DISPLAY_NAME_MAPPINGS = {**AI_NameMap,**AI_EDIT_NameMap, **Text_NameMap, **Multi_NameMap, **DIFY_NameMap, **DifyResult_NameMap, **UrlToImg_NameMap}