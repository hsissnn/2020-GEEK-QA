# 2020-GEEK-QA
客服场景问答对抽取

### 背景
在用户与人工客服的聊天记录中，包含了大量信息类知识，在客服工作中需要通过系统查询或者电话联系供应商来获取这些信息。如果可以将客人提问的问题及客服提供答案从聊天记录中挖掘出来，那么我们便可以在客服端工具中展示这些信息，减少信息查询成本，提高客服工作效率

### 成果
1、从用户在本次会话发送的多条消息中，抽取出一个用户的业务问题（需排除闲聊类等和业务无关的消息，会话涉及多个问题的仅抽取出出现的第一个问题）

2、从客服在本次会话发送的多条消息中，以机器阅读理解或者机器摘要的方式找到对用户问题的回答信息。