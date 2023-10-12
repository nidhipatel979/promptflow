# import faiss
from jinja2 import Environment, FileSystemLoader
import os

# from utils.index import FAISSIndex
from utils.oai import OAIEmbedding, render_with_token_limit
from utils.logging import log


def find_context(question: str,date:str, retrieved_docs: list):
    
    template = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)))
    ).get_template("qna_prompt.md")
    token_limit = int(os.environ.get("PROMPT_TOKEN_LIMIT"))

    # Try to render the template with token limit and reduce snippet count if it fails
    while True:
        try:
            prompt = render_with_token_limit(
                template, token_limit, question=question, date=date,context="\n\n".join(retrieved_docs)    
            )
            break
        except ValueError:
            retrieved_docs = retrieved_docs[:-1]
            log(f"Reducing snippet count to {len(retrieved_docs)} to fit token limit")
    return prompt, retrieved_docs
