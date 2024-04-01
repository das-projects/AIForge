from langflow import CustomComponent
from langchain.schema import Document
from langflow.services.database.models.base import orjson_dumps
from langchain_community.utilities.searchapi import SearchApiAPIWrapper
from typing import Optional


class SearchApi(CustomComponent):
    display_name: str = "SearchApi"
    description: str = "Real-time search engine results API."
    output_types: list[str] = ["Document"]
    documentation: str = "https://www.searchapi.io/docs/google"
    field_config = {
        "engine": {
            "display_name": "Engine",
            "field_type": "str",
            "info": "The search engine to use.",
        },
        "params": {
            "display_name": "Parameters",
            "info": "The parameters to send with the request.",
        },
        "code": {"show": False},
        "api_key": {
            "display_name": "API Key",
            "field_type": "str",
            "required": True,
            "password": True,
            "info": "The API key to use SearchApi.",
        },
    }

    def build(
        self,
        engine: str,
        api_key: str,
        params: Optional[dict] = None,
    ) -> Document:
        if params is None:
            params = {}

        search_api_wrapper = SearchApiAPIWrapper(engine=engine, searchapi_api_key=api_key)

        q = params.pop("q", "SearchApi Langflow")
        results = search_api_wrapper.results(q, **params)

        result = orjson_dumps(results, indent_2=False)

        document = Document(page_content=result)

        return document
