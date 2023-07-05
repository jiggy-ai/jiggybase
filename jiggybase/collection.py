import os
from typing import Optional, List, Iterator, Tuple
from pydantic import BaseModel, Field, BaseConfig, HttpUrl
from enum import Enum
from .models import collection, CollectionChatConfig, PatchCollectionChatConfig
from .jiggybase_session import JiggyBaseSession
from .models import UpsertResponse,  Query, QueryRequest, QueryResponse, UpsertRequest, Document, DocumentChunk, DeleteRequest, DeleteResponse, DocumentMetadataFilter, DocChunksResponse
from .models import Message, CompletionRequest, ChatCompletion 
from .chat_stream import extract_content_from_sse_bytes
from .models import ExtractMetadataConfig
from .models import CollectionPatchRequest, PluginAuthConfigOAuth, PatchPluginOAuthConfigRequest
from .models import DocumentMetadata
from typing import Union, List


        
class Collection(collection.Collection):
    """
    derived from models.collection.Collection data model for purposes of adding management methods
    """
    class Config(BaseConfig):
        extra = "allow"

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session        
        api_key = self.session.api_key
        self.plugin_session = JiggyBaseSession(host=f'https://{kwargs["fqdn"]}', api='', api_key=api_key)
        self.chat_session = JiggyBaseSession(host=session.host, api='v1', api_key=api_key)
        
    def set_description(self, description:str) -> "Collection":
        """
        Update an existing collection using its ID and the provided description.
        """
        patch_request = CollectionPatchRequest(description=description)
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}", model=patch_request)
        self.description = rsp.json()['description']


    def set_oauth_verification_token(self, openai_verification_token: str) -> PluginAuthConfigOAuth:
        """
        Set the OpenAI verification token for this collection's plugin.
        This is the token that OpenAI provides during while registering a plugin configured to use Oauth.
        """
        patch_request = PatchPluginOAuthConfigRequest(openai_verification_token=openai_verification_token)
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}/plugin_oauth", model=patch_request)
        return PluginAuthConfigOAuth(**rsp.json())

    def plugin_oauth_config(self) -> PluginAuthConfigOAuth:
        """
        Get the OAuth configuration for this collection's plugin.
        The client_id and client_secret returned here are configured with OpenAI while 
        registering a plugin configured to use Oauth.
        """
        rsp = self.session.get(f"/orgs/{self.org_id}/collections/{self.id}/plugin_oauth")
        return PluginAuthConfigOAuth(**rsp.json())

    def delete(self):
        """
        Delete a collection.  Warning: this is permanent.
        """
        self.session.delete(f"/orgs/{self.org_id}/collections/{self.id}")


    def get_chat_config(self) -> CollectionChatConfig:
        """
        Get the chat configuration for this collection.
        """
        rsp = self.session.get(f"/orgs/{self.org_id}/collections/{self.id}/chat_config")
        return collection.CollectionChatConfig(**rsp.json())

    def update_chat_config(self, model: str, prompt_task_id: int) -> CollectionChatConfig:
        """
        Update the chat configuration for this collection.
        """
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}/chat_config/{model}", model=PatchCollectionChatConfig(prompt_task_id=prompt_task_id))
        return CollectionChatConfig(**rsp.json())

 
    def upsert_file(self, file_path: str, mimetype: str = None, id: str = None, metadata : DocumentMetadata = None) -> UpsertResponse:
        """
        Add a file to the collection.
        Mimetype can be specified, otherwise it will be inferred from the file extension.
        The doc id can be specified, otherwise it will be generated.
        Metadata can be specified, otherwise some metadata will be inferred from the file.
        """
        if not os.path.exists(file_path):
            raise ValueError("File not found")
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file, mimetype)}
            params = {'id': id} if id else {}
            if metadata:
                rsp = self.plugin_session.post("/upsert-file", 
                                               files=files, 
                                               params=params,
                                               data={'metadata': metadata.json(exclude_unset=True)})
            else:
                rsp = self.plugin_session.post("/upsert-file", params=params, files=files)
        return UpsertResponse.parse_obj(rsp.json())

    def upsert(self, documents: List[Document]) -> UpsertResponse:
        """
        Add a list of Document objects to the collection.
        """
        upsert_request = UpsertRequest(documents=documents)
        rsp = self.plugin_session.post("/upsert", model=upsert_request)
        return  UpsertResponse.parse_obj(rsp.json())
    
    def query(self, queries: Union[str, List[str], Query], top_k : int = 10) -> QueryResponse:
        """
        Query the collection returning the top_k results for each query.
        queries can be either a single string, a list of strings, or a list of Query objects.
        if it is a string or list of strings, the specified top_k will be used for each of the queries.
        Returns a QueryResponse object.
        """
        if isinstance(queries, str):
            queries = [Query(query=queries, top_k=top_k)]
        elif isinstance(queries, Query):
            queries = [Query(query=q, top_k=top_k) for q in queries]
        qr = QueryRequest(queries=queries)
        rsp = self.plugin_session.post("/query", model=qr)
        return  QueryResponse.parse_obj(rsp.json())

    def get_doc(self, id: str) -> list[DocumentChunk]:
        """
        Get a document by id
        """
        rsp = self.plugin_session.get(f"/docs/{id}")
        return [DocumentChunk.parse_obj(c) for c in rsp.json()]
    
    def get_chunks(self, 
                   start: int = 0, 
                   limit: int = 10, 
                   reverse: bool = True) -> List[DocumentChunk]:
        """
        low level interface for iterating through the chunks in a collection
        start - Offset of the first result to return
        limit - Number of results to return starting from the offset
        reverse - Reverse the order of the items returned
        """
        params = {"start": start, "limit": limit, "reverse": reverse}
        rsp = self.plugin_session.get("/chunks", params=params)
        return [DocumentChunk.parse_obj(chunk) for chunk in rsp.json()]

    def get_doc_chunks(self, 
                       index: int = -1, 
                       limit: int = 10, 
                       reverse: bool = True,
                       max_chunks_per_doc = 1) -> Tuple[List[List[DocumentChunk]], int]:
         """
         low level interface for iterating through the initial chunks for all docs in a collection
         index - index of the first result to return, should be -1 to start at the end
         limit - Number of results to return starting from the offset
         reverse - Reverse the order of the items returned; True to return newest first
         max_chunks_per_doc - maximum number of chunks to return for each document
         """
         params = {"index": index, "limit": limit, "reverse": reverse, "max_chunks_per_doc": max_chunks_per_doc}
         rsp = self.plugin_session.get("/doc_chunks", params=params)
         dcr_rsp = DocChunksResponse.parse_obj(rsp.json())
         return dcr_rsp.docs, dcr_rsp.next_index

    def delete_docs(self, 
                    ids                      : Optional[List[str]] = None, 
                    document_metadata_filter : Optional[DocumentMetadataFilter] = None, 
                    delete_all               : Optional[bool] = False) -> DeleteResponse:
        """
        Delete items in the collection by document id's or document metadata filter.
        A delete_all option is also provided to delete all documents in the collection.
        """
        delete_request = DeleteRequest(ids=ids, filter=document_metadata_filter, delete_all=delete_all)
        rsp = self.plugin_session.delete("/delete", model=delete_request)
        return DeleteResponse.parse_obj(rsp.json())


    def _chat_completion(self, 
                         messages: List[Message],
                         model = 'gpt-3.5-turbo',
                         max_tokens = None,
                         temperature = .1) -> ChatCompletion:
        """
        low level interface for chat completion
        The input here mirrors openai chat completion parameters, while the output is different
        """
        cr = CompletionRequest(model       = f'{self.name}_{model}', 
                               messages    = messages,
                               max_tokens  = max_tokens,
                               temperature = temperature,
                               stream      = False)
        rsp = self.chat_session.post("/chat/completions", model=cr)          
        return ChatCompletion.parse_obj(rsp.json())

    def _chat_completion_stream_str(self, 
                         messages: List[Message],
                         model = 'gpt-3.5-turbo',
                         max_tokens = None,
                         temperature = .1) -> Iterator[str]:
        """
        low level interface for chat completion with streaming
        yields the model output as an iteration of strings
        """
        cr = CompletionRequest(model       = f'{self.name}_{model}', 
                               messages    = messages,
                               max_tokens  = max_tokens,
                               temperature = temperature,
                               stream      = True)
        rsp = self.chat_session.post("/chat/completions", model=cr, stream=True)
        for line in rsp.iter_lines():
            if line:  # filter out keep-alive newlines        
                yield extract_content_from_sse_bytes(line)

    def get_extract_metadata_config(self):
        """
        Get the metadata configuration for this collection.
        """
        rsp = self.session.get(f"/orgs/{self.org_id}/collections/{self.id}/extract_metadata_config")
        return ExtractMetadataConfig(**rsp.json())

    def patch_extract_metadata_config(self, config: ExtractMetadataConfig):
        """
        Get the metadata configuration for this collection.
        """
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}/extract_metadata_config", model=config)
        return ExtractMetadataConfig(**rsp.json())    

    def __str__(self) -> str:
        return f"Collection(id={self.id:4}, name={self.display_name:30}, hostname={self.hostname:30}, org_id={self.org_id:4},\n" \
               f"           description='{self.description}')"

    def __repr__(self) -> str:
        return str(self)    