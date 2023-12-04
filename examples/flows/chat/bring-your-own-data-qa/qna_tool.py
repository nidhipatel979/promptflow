from promptflow import tool
from qna import qna
import time


@tool
def qna_tool(prompt: str, history: list,temperature:float):
    stream = qna(prompt, convert_chat_history_to_chatml_messages(history),temperature=temperature)
    print("Response stream")
    print(type(stream))
    ### For streaming response, comment the line 105 to 111 in oai.py--> stream  funtion and return response instead. Then return the stream
    # from this function as a generator object
    answer = ""
    for str in stream:
        # yield {"answer": str}
        answer = answer + str + ""

    return {"answer": answer,"end_time": time.time()}


def convert_chat_history_to_chatml_messages(history):
    messages = []
    for item in history:
        messages.append({"role": "user", "content": item["inputs"]["question"]})
        messages.append({"role": "assistant", "content": item["outputs"]["answer"]})

    return messages
