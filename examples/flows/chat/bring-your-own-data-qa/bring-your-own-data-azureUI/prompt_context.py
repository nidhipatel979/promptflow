import os
from typing import Union

from promptflow import tool
from promptflow.connections import AzureOpenAIConnection, CognitiveSearchConnection
from utils.acs_helpers import AIAAzureSearch
from utils.oai import OAIEmbedding

@tool
def prompt_context(connection: Union[CognitiveSearchConnection,AzureOpenAIConnection],input) -> list:
    print("eright here")
    embedding_func = OAIEmbedding()
    acs_milo_search_index = AIAAzureSearch(
                                            azure_search_key = connection.api_key,
                                            azure_search_endpoint=connection.api_base,
                                            index_name='milo-latest',
                                            embedding_function=embedding_func,
                                            #search_type='similarity',
                                            # semantic_configuration_name = "milo-semantic-config" #required in case of semantic search
                                        )
    
    
    acs_search_kwargs = {
                    "k" : 8,
                    "search_type" : "similarity", # vector search
                    
                }
    
    return_docs = acs_milo_search_index.vector_search(query=input,k=8)
    print(type(return_docs),return_docs)
    return [{"page_content":doc.page_content,"metadata":doc.metadata} for doc in return_docs]