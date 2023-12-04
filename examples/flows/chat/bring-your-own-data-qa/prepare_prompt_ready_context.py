from typing import List
from promptflow import tool
from find_context import find_context
from datetime import datetime

def _get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y")

@tool
def generate_prompt_context(question: str,search_result: List[dict]) -> str:
   
    def format_doc(doc: dict):
        return f"Content: {doc['page_content']}\nSource: {doc['metadata']['metadata_source']}"
    retrieved_docs = []
    for doc in search_result:
        retrieved_docs.append(format_doc(doc))
    date = _get_datetime
    prompt, context = find_context(question, date,retrieved_docs)
    # return {"\n\n".join([format_doc(doc) for doc in retrieved_docs])    
    return {"prompt": prompt, "context": " ".join(context)}        
