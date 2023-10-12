from typing import List
from promptflow import tool
from find_context import find_context
@tool
def generate_prompt_context(question: str,date:str,search_result: List[dict]) -> str:
    def format_doc(doc: dict):
        return f"Content: {doc['page_content']}\nSource: {doc['metadata']['metadata_source']}"
    retrieved_docs = []
    for doc in search_result:
        retrieved_docs.append(format_doc(doc))
    print("error here",date)
    print("docs are",retrieved_docs)
    # prompt, context = find_context(question, date,retrieved_docs)
    return "\n\n".join(retrieved_docs)    
    # return {"prompt": prompt, "context": context}        
