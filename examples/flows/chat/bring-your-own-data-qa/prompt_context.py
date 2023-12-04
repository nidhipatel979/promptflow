import os
from typing import Union

from promptflow import tool
from promptflow.connections import AzureOpenAIConnection, CognitiveSearchConnection
from utils.acs_helpers import AIAAzureSearch
from utils.oai import OAIEmbedding
import time
@tool
def prompt_context(connection: Union[CognitiveSearchConnection,AzureOpenAIConnection],question,brands,provinces, language, status,publish_date) -> list:
    start_time = time.time()
    embedding_func = OAIEmbedding()
    acs_milo_search_index = AIAAzureSearch(
                                            azure_search_key = connection.api_key,
                                            azure_search_endpoint=connection.api_base,
                                            index_name='milo-latest',
                                            embedding_function=embedding_func,
                                            #search_type='similarity',
                                            # semantic_configuration_name = "milo-semantic-config" #required in case of semantic search
                                        )
    
    acs_province_filter = f"metadata_provinces/any(t: search.in(t, '{','.join(provinces)}'))"
    acs_brand_filter = f"metadata_brands/any(t: search.in(t, '{','.join(brands)}'))"
    acs_expr_filter = f"({acs_province_filter}) and ({acs_brand_filter})"

    if status in ['Current', 'Expired']:
        acs_expr_filter = f"(metadata_status eq '{status}') and ({acs_expr_filter})"

    if publish_date:
        acs_expr_filter = f"(metadata_publish_date ge {publish_date}T00:00:00Z) and ({acs_expr_filter})"

    if language in ['en', 'fr']:
        acs_expr_filter = f"(metadata_language eq '{language}') and ({acs_expr_filter})"

    return_docs = acs_milo_search_index.vector_search(query=question,k=8,filters=acs_expr_filter)
    # return_docs = acs_milo_search_index.vector_search(query=question,k=8)
    return {"search_result":[{"page_content":doc.page_content,"metadata":doc.metadata} for doc in return_docs],"start_time":start_time}