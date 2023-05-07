from typing import Optional, Tuple, List
from pydantic import BaseModel, Field, BaseConfig, HttpUrl
from enum import Enum
from .models import collection, CollectionChatConfig, PatchCollectionChatConfig
from .jiggybase_session import JiggyBaseSession
from .models import UpsertResponse,  Query, QueryRequest, QueryResponse, UpsertRequest, Document, DocumentChunk, DeleteRequest, DeleteResponse, DocumentMetadataFilter, DocChunksResponse
import os
import mimetypes

from typing import Union, List
class PluginAuthType(Enum):
    bearer :str = "bearer"
    none   :str = "none"
    oauth  :str = "oauth"

        
class CollectionPostRequest(BaseModel):
    """
    Used to create a new Collection service
    """
    name:         str                      = Field(description="The globally unique hostname for the collection. Subject to DNS naming rules. ")
    display_name: Optional[str]            = Field(description="The human friendly display name for the collection.")
    description:  Optional[str]            = Field(description="A description of the collection.")
    plugin_auth:  Optional[PluginAuthType] = Field(default=PluginAuthType.bearer, description="The authentication type to use for this collection's ChatGPT plugin.")


class CollectionPatchRequest(BaseModel):
    """
    Used to modify an existing service
    """
    description:  Optional[str] = Field(description="A description of the collection.")
    plugin_auth:  Optional[str] = Field(description='The auth plugin to use for this org.')
    display_name: Optional[str] = Field(description="The human friendly display name for the collection.")



class PluginAuthConfigOAuth(BaseModel):
    """
    The Plugin Oauth configuration as managed by GPT-Gateway
    """    
    client_url:                 HttpUrl     = Field(description="ChatGPT will direct the user’s browser to this url to log in to the plugin")
    authorization_url:          HttpUrl     = Field(description="After successful login ChatGPT will complete the OAuth flow by making a POST request to this URL")
    scope:                      str         = Field(description="The scope used for the OAuth flow")
    client_id:                  str         = Field(unique=True, index=True, description="The client id to send to OpenAI for the plugin")
    client_secret:              str         = Field(description="The client secret to send to OpenAI for the plugin")
    openai_verification_token:  str         = Field(description="The verification token specified by OpenAI to configure in the plugin")

class PatchPluginOAuthConfigRequest(BaseModel):
    openai_verification_token: str  

        
class Collection(collection.Collection):
    """
    derived from models.collection.Collection data model for purposes of adding management methods
    """
    class Config(BaseConfig):
        extra = "allow"

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        self.plugin_session = JiggyBaseSession(host=f'https://{kwargs["fqdn"]}', api='')

    def set_description(self, description:str) -> "Collection":
        """
        Update an existing collection using its ID and the provided description.
        """
        patch_request = CollectionPatchRequest(description=description)
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}", model=patch_request)
        return Collection(**rsp.json())

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

 
    def upsert_file(self, file_path: str, mimetype: str = None) -> UpsertResponse:
        """
        Add a file to the collection.
        """
        if not os.path.exists(file_path):
            raise ValueError("File not found")
             
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file, mimetype)}
            rsp = self.plugin_session.post("/upsert-file", files=files)
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
        low level interface for iterating through the chunks in a collection
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
        