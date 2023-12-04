import os
from typing import Union

from promptflow import tool
from promptflow.connections import AzureOpenAIConnection, CognitiveSearchConnection
from utils.acs_helpers import AIAAzureSearch
from utils.oai import OAIEmbedding
import time
@tool
def token_usage(prompt:str,query_converted:str,response) -> list:
    answer = ""
    for str in response:
        answer = answer + str + ""
    condense_llm_token_count = num_tokens_from_messages(query_converted)
    chat_token_cnt = num_tokens_from_messages(prompt)
        # Chat llm - completion token count
    chat_llm_completion_token_cnt = num_tokens_from_messages(answer)
    return {'condense_llm_prompt' : condense_llm_token_count,
                            'chat_llm_prompt' : chat_token_cnt,
                            'chat_llm_completion' : chat_llm_completion_token_cnt
             }

import tiktoken
def num_tokens_from_messages(messages):
    """Return the number of tokens used by a list of messages. : Ref: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb"""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(messages))