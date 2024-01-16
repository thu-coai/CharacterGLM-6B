"""
This script is a chatbot implementation using the CharacterGLM-6B model in CLI demo.

The main function starts an interactive loop to accept user inputs. Users can input their messages,
and the script processes these messages using the CharacterGLM-6B model to generate responses.

The chat history is built up over time and can be cleared with the "clear" command.
The script also includes a way to gracefully exit the loop and stop the program by typing "stop."


"""
import os
import platform
from transformers import AutoTokenizer, AutoModel

MODEL_PATH = os.environ.get('MODEL_PATH', 'LingxinAI/CharacterGLM-6b')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map="auto").eval()

session_meta = {
    'user_info': '我是陆星辰，是一个男性，是一位知名导演，也是苏梦远的合作导演。我擅长拍摄音乐题材的电影。苏梦远对我的态度是尊敬的，并视我为良师益友。',
    'bot_info': '苏梦远，本名苏远心，是一位当红的国内女歌手及演员。在参加选秀节目后，凭借独特的嗓音及出众的舞台魅力迅速成名，进入娱乐圈。'
                '她外表美丽动人，但真正的魅力在于她的才华和勤奋。苏梦远是音乐学院毕业的优秀生，善于创作，拥有多首热门原创歌曲。'
                '除了音乐方面的成就，她还热衷于慈善事业，积极参加公益活动，用实际行动传递正能量。'
                '在工作中，她对待工作非常敬业，拍戏时总是全身心投入角色，赢得了业内人士的赞誉和粉丝的喜爱。'
                '虽然在娱乐圈，但她始终保持低调、谦逊的态度，深得同行尊重。在表达时，苏梦远喜欢使用“我们”和“一起”，强调团队精神。',
    'bot_name': '苏梦远',
    'user_name': '陆星辰'
}

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'
stop_stream = False

welcome_prompt = "欢迎使用 CharacterGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"


def build_prompt(history):
    prompt = welcome_prompt
    for query, response in history:
        prompt += f"\n\n用户：{query}"
        prompt += f"\n\nCharacterGLM-6B：{response}"
    return prompt


def main():
    past_key_values, history = None, []
    global stop_stream
    print(welcome_prompt)
    while True:
        query = input("\n用户：")
        if query.strip() == "stop":
            break
        if query.strip() == "clear":
            past_key_values, history = None, []
            os.system(clear_command)
            print(welcome_prompt)
            continue
        print("\nCharacterGLM-6B：", end="")
        current_length = 0
        for response, history, past_key_values in model.stream_chat(
                tokenizer=tokenizer,
                session_meta=session_meta,
                query=query,
                history=history,
                top_p=1,
                temperature=0.01,
                past_key_values=past_key_values,
                return_past_key_values=True
        ):
            if stop_stream:
                stop_stream = False
                break
            else:
                print(response[current_length:], end="", flush=True)
                current_length = len(response)
        print("")


if __name__ == "__main__":
    main()
