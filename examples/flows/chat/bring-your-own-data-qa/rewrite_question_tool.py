from promptflow import tool
from rewrite_question import rewrite_question


@tool
def rewrite_question_tool(question: str, history: list, env_ready_signal: str):
    ans = rewrite_question(question, history)
    print("This is the re-written question:",ans)
    return ans
