"""
一个简单的demo，调用CharacterGLM实现角色扮演，调用CogView生成图片，调用ChatGLM生成CogView所需的prompt。

依赖：
pyjwt
requests
streamlit
zhipuai
python-dotenv

运行方式：
```bash
streamlit run characterglm_api_demo_streamlit.py
```
"""

import requests
import time
import os
import random
import itertools
from typing import Literal, TypedDict, List, Union, Iterator, Optional

import jwt

import streamlit as st
from dotenv import load_dotenv


# 通过.env文件设置环境变量
# reference: https://github.com/theskumar/python-dotenv
load_dotenv()


## 数据类型 #####
class BaseMsg(TypedDict):
    pass


class TextMsg(BaseMsg):
    role: Literal["user", "assistant"]
    content: str


class ImageMsg(BaseMsg):
    role: Literal["image"]
    image: st.elements.image.ImageOrImageList
    caption: Optional[Union[str, List[str]]]


Msg = Union[TextMsg, ImageMsg]
TextMsgList = List[TextMsg]
MsgList = List[Msg]


class CharacterMeta(TypedDict):
    user_info: str  # 用户人设
    bot_info: str   # 角色人设
    bot_name: str   # bot扮演的角色的名字
    user_name: str  # 用户的名字


def filter_text_msg(messages: MsgList) -> TextMsgList:
    return [m for m in messages if m["role"] != "image"]


## api ##
# 智谱开放平台API key，参考 https://open.bigmodel.cn/usercenter/apikeys
API_KEY: str = ""


class ApiKeyNotSet(ValueError):
    pass


def verify_api_key_not_empty():
    if not API_KEY:
        raise ApiKeyNotSet


def generate_token(apikey: str, exp_seconds: int):
    # reference: https://open.bigmodel.cn/dev/api#nosdk
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)
 
    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
 
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def get_characterglm_response(messages: TextMsgList, meta: CharacterMeta):
    """ 通过http调用characterglm """
    # Reference: https://open.bigmodel.cn/dev/api#characterglm
    verify_api_key_not_empty()
    url = "https://open.bigmodel.cn/api/paas/v3/model-api/charglm-3/sse-invoke"
    resp = requests.post(
        url,
        headers={"Authorization": generate_token(API_KEY, 1800)},
        json=dict(
            model="charglm-3",
            meta=meta,
            prompt=messages,
            incremental=True)
    )
    resp.raise_for_status()
    
    # 解析响应（非官方实现）
    sep = b':'
    last_event = None
    for line in resp.iter_lines():
        if not line or line.startswith(sep):
            continue
        field, value = line.split(sep, maxsplit=1)
        if field == b'event':
            last_event = value
        elif field == b'data' and last_event == b'add':
            yield value.decode()


def get_characterglm_response_via_sdk(messages: TextMsgList, meta: CharacterMeta):
    """ 通过旧版sdk调用characterglm """
    # 与get_characterglm_response等价
    # Reference: https://open.bigmodel.cn/dev/api#characterglm
    # 需要安装旧版sdk，zhipuai==1.0.7
    import zhipuai
    verify_api_key_not_empty()
    zhipuai.api_key = API_KEY
    response = zhipuai.model_api.sse_invoke(
        model="charglm-3",
        meta= meta,
        prompt= messages,
        incremental=True
    )
    for event in response.events():
        if event.event == 'add':
            yield event.data


def get_chatglm_response_via_sdk(messages: TextMsgList):
    """ 通过sdk调用chatglm """
    # reference: https://open.bigmodel.cn/dev/api#glm-3-turbo  `GLM-3-Turbo`相关内容
    # 需要安装新版zhipuai
    from zhipuai import ZhipuAI
    verify_api_key_not_empty()
    client = ZhipuAI(api_key=API_KEY) # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-3-turbo",  # 填写需要调用的模型名称
        messages=messages,
        stream=True,
    )
    for chunk in response:
        yield chunk.choices[0].delta.content


def generate_role_appearance(role_profile: str):
    """ 用chatglm生成角色的外貌描写 """
    
    instruction = f"""
请从下列文本中，抽取人物的外貌描写。若文本中不包含外貌描写，请你推测人物的性别、年龄，并生成一段外貌描写。要求：
1. 只生成外貌描写，不要生成任何多余的内容。
2. 外貌描写不能包含敏感词，人物形象需得体。
3. 尽量用短语描写，而不是完整的句子。
4. 不要超过50字

文本：
{role_profile}
"""
    return get_chatglm_response_via_sdk(
        messages=[
            {
                "role": "user",
                "content": instruction.strip()
            }
        ]
    )


def generate_chat_scene_prompt(messages: TextMsgList, meta: CharacterMeta):
    """ 调用chatglm生成cogview的prompt，描写对话场景 """
    instruction = f"""
阅读下面的角色人设与对话，生成一段文字描写场景。

{meta['bot_name']}的人设：
{meta['bot_info']}
    """.strip()
    
    if meta["user_info"]:
        instruction += f"""

{meta["user_name"]}的人设：
{meta["user_info"]}
""".rstrip()

    if messages:
        instruction += "\n\n对话：" + '\n'.join((meta['bot_name'] if msg['role'] == "assistant" else meta['user_name']) + '：' + msg['content'].strip() for msg in messages)
    
    instruction += """
    
要求如下：
1. 只生成场景描写，不要生成任何多余的内容
2. 描写不能包含敏感词，人物形象需得体
3. 尽量用短语描写，而不是完整的句子
4. 不要超过50字
""".rstrip()
    print(instruction)
    
    return get_chatglm_response_via_sdk(
        messages=[
            {
                "role": "user",
                "content": instruction.strip()
            }
        ]
    )


def generate_cogview_image(prompt: str) -> str:
    """ 调用cogview生成图片，返回url """
    # reference: https://open.bigmodel.cn/dev/api#cogview
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=API_KEY) # 请填写您自己的APIKey
    
    response = client.images.generations(
        model="cogview-3", #填写需要调用的模型名称
        prompt=prompt
    )
    return response.data[0].url


def generate_fake_response(messages: TextMsgList, meta: CharacterMeta) -> Iterator[str]:
    # 用于debug
    bot_response = random.choice(['abcd', '你好', '世界', '42'])
    for c in bot_response:
        yield c
        time.sleep(0.5)


### UI ###
st.set_page_config(page_title="CharacterGLM API Demo", page_icon="🤖", layout="wide")
debug = os.getenv("DEBUG", "").lower() in ("1", "yes", "y", "true", "t", "on")

def update_api_key(key: Optional[str] = None):
    global API_KEY
    if debug:
        print(f'update_api_key. st.session_state["API_KEY"] = {st.session_state["API_KEY"]}, key = {key}')
    key = key or st.session_state["API_KEY"]
    if key:
        API_KEY = key

api_key = st.sidebar.text_input("API_KEY", value=os.getenv("API_KEY", ""), key="API_KEY", type="password", on_change=update_api_key)
update_api_key(api_key)


# 初始化
if "history" not in st.session_state:
    st.session_state["history"] = []
if "meta" not in st.session_state:
    st.session_state["meta"] = {
        "user_info": "",
        "bot_info": "",
        "bot_name": "",
        "user_name": ""
    }


def init_session():
    st.session_state["history"] = []


# 4个输入框，设置meta的4个字段
meta_labels = {
    "bot_name": "角色名",
    "user_name": "用户名", 
    "bot_info": "角色人设",
    "user_info": "用户人设"
}

# 2x2 layout
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(label="角色名", key="bot_name", on_change=lambda : st.session_state["meta"].update(bot_name=st.session_state["bot_name"]), help="模型所扮演的角色的名字，不可以为空")
        st.text_area(label="角色人设", key="bot_info", on_change=lambda : st.session_state["meta"].update(bot_info=st.session_state["bot_info"]), help="角色的详细人设信息，不可以为空")
        
    with col2:
        st.text_input(label="用户名", value="用户", key="user_name", on_change=lambda : st.session_state["meta"].update(user_name=st.session_state["user_name"]), help="用户的名字，默认为用户")
        st.text_area(label="用户人设", value="", key="user_info", on_change=lambda : st.session_state["meta"].update(user_info=st.session_state["user_info"]), help="用户的详细人设信息，可以为空")


def verify_meta() -> bool:
    # 检查`角色名`和`角色人设`是否空，若为空，则弹出提醒
    if st.session_state["meta"]["bot_name"] == "" or st.session_state["meta"]["bot_info"] == "":
        st.error("角色名和角色人设不能为空")
        return False
    else:
        return True


def draw_new_image():
    if not verify_meta():
        return
    text_messages = filter_text_msg(st.session_state["history"])
    if text_messages:
        image_prompt = "".join(
            generate_chat_scene_prompt(
                text_messages[-10: ],
                meta=st.session_state["meta"]
            )
        )
        
    else:
        image_prompt = "".join(generate_role_appearance(st.session_state["meta"]["bot_info"]))
    
    if not image_prompt:
        st.error("调用chatglm生成Cogview prompt出错")
        return
    
    # TODO: 加上风格选项
    image_prompt = '二次元风格。' + image_prompt.strip()
    
    print(f"image_prompt = {image_prompt}")
    n_retry = 3
    st.markdown("正在生成图片，请稍等...")
    for i in range(n_retry):
        try:
            img_url = generate_cogview_image(image_prompt)
        except Exception as e:
            if i < n_retry - 1:
                st.error("遇到了一点小问题，重试中...")
            else:
                st.error("又失败啦，点击【生成图片】按钮可再次重试")
    img_msg = ImageMsg({"role": "image", "image": img_url, "caption": image_prompt})
    # 若history的末尾有图片消息，则替换它，（重新生成）
    # 否则，append（新增）
    while st.session_state["history"] and st.session_state["history"][-1]["role"] == "image":
        st.session_state["history"].pop()
    st.session_state["history"].append(img_msg)
    st.rerun()


button_labels = {
    "clear_meta": "清空人设",
    "clear_history": "清空对话历史",
    "gen_picture": "生成图片"
}
if debug:
    button_labels.update({
        "show_api_key": "查看API_KEY",
        "show_meta": "查看meta",
        "show_history": "查看历史"
    })

# 在同一行排列按钮
with st.container():
    n_button = len(button_labels)
    cols = st.columns(n_button)
    button_key_to_col = dict(zip(button_labels.keys(), cols))
    
    with button_key_to_col["clear_meta"]:
        clear_meta = st.button(button_labels["clear_meta"], key="clear_meta")
        if clear_meta:
            st.session_state["meta"] = {
                "user_info": "",
                "bot_info": "",
                "bot_name": "",
                "user_name": ""
            }
            st.rerun()

    with button_key_to_col["clear_history"]:
        clear_history = st.button(button_labels["clear_history"], key="clear_history")
        if clear_history:
            init_session()
            st.rerun()
    
    with button_key_to_col["gen_picture"]:
        gen_picture = st.button(button_labels["gen_picture"], key="gen_picture")

    if debug:
        with button_key_to_col["show_api_key"]:
            show_api_key = st.button(button_labels["show_api_key"], key="show_api_key")
            if show_api_key:
                print(f"API_KEY = {API_KEY}")
        
        with button_key_to_col["show_meta"]:
            show_meta = st.button(button_labels["show_meta"], key="show_meta")
            if show_meta:
                print(f"meta = {st.session_state['meta']}")
        
        with button_key_to_col["show_history"]:
            show_history = st.button(button_labels["show_history"], key="show_history")
            if show_history:
                print(f"history = {st.session_state['history']}")


# 展示对话历史
for msg in st.session_state["history"]:
    if msg["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(msg["content"])
    elif msg["role"] == "image":
        with st.chat_message(name="assistant", avatar="assistant"):
            st.image(msg["image"], caption=msg.get("caption", None))
    else:
        raise Exception("Invalid role")


if gen_picture:
    draw_new_image()


with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()


def output_stream_response(response_stream: Iterator[str], placeholder):
    content = ""
    for content in itertools.accumulate(response_stream):
        placeholder.markdown(content)
    return content


def start_chat():
    query = st.chat_input("开始对话吧")
    if not query:
        return
    else:
        if not verify_meta():
            return
        if not API_KEY:
            st.error("未设置API_KEY")

        input_placeholder.markdown(query)
        st.session_state["history"].append(TextMsg({"role": "user", "content": query}))
        
        response_stream = get_characterglm_response(filter_text_msg(st.session_state["history"]), meta=st.session_state["meta"])
        bot_response = output_stream_response(response_stream, message_placeholder)
        if not bot_response:
            message_placeholder.markdown("生成出错")
            st.session_state["history"].pop()
        else:
            st.session_state["history"].append(TextMsg({"role": "assistant", "content": bot_response}))
            
    
start_chat()
