from typing import Optional, Union, List
from pydantic import BaseModel, Field
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl




class PluginAuthType(str, Enum):
    """
    Note that this is for custom plugins available in the JiggyBase enterprise tier and unrelated to the main JiggyBase plugin in the OpenAI plugin store.
    """
    bearer :str = "bearer"
    none   :str = "none"
    oauth  :str = "oauth"

    
class PluginAuthConfigOAuth(BaseModel):
    """
    The Plugin Oauth configuration as managed by JiggyBase
    Note that this is for custom plugins available in the JiggyBase enterprise tier and unrelated to the main JiggyBase plugin in the OpenAI plugin store.
    """    
    client_url:                 HttpUrl     = Field(description="ChatGPT will direct the user’s browser to this url to log in to the plugin")
    authorization_url:          HttpUrl     = Field(description="After successful login ChatGPT will complete the OAuth flow by making a POST request to this URL")
    scope:                      str         = Field(description="The scope used for the OAuth flow")
    client_id:                  str         = Field(unique=True, index=True, description="The client id to send to OpenAI for the plugin")
    client_secret:              str         = Field(description="The client secret to send to OpenAI for the plugin")
    openai_verification_token:  str         = Field(description="The verification token specified by OpenAI to configure in the plugin")

class PatchPluginOAuthConfigRequest(BaseModel):
    openai_verification_token: str  

class Source(str, Enum):
    email = "email"
    file = "file"
    chat = "chat"
    web  = "web"


class DocumentMetadata(BaseModel):
    source: Optional[Source] = None
    source_id: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    author: Union[str, List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = Field(description="The 2 character ISO 639-1 language code of the primary language of the content.")
    version: str = None

class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[list[float]] = None
    token_count: Optional[int] = None
    reference_url: Optional[str] = None

    def __str__(self):
        if len(self.text) > 100:
            text = self.text[:100] + '...'
        else: 
            text = self.text
        text = text.replace('\n', ' ')
        estr = "DocumentChunk("
        if self.id is not None:
            estr += f"id={self.id}, "
        if self.metadata is not None:
            estr += f"metadata={str(self.metadata)}, "
        if self.embedding is not None:
            estr += f"embedding=dim{len(self.embedding)}, "
        estr += f"text={text})"
        return estr

    
class DocumentChunkWithScore(DocumentChunk):
    score: float


class Document(BaseModel):
    id: Optional[str]
    text: str
    metadata: Optional[DocumentMetadata] = None
    mimetype: Optional[str] = None
    token_count: Optional[int] = None


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]

class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None
    source: Optional[Source] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format
    title: Optional[str] = None


class Query(BaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 3

class QueryWithEmbedding(Query):
    embedding: list[float]


class QueryResult(BaseModel):
    query: str
    results: list[DocumentChunkWithScore]


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    ids: List[str]


class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool


class Accounting(BaseModel):
    chunk_count: int
    doc_count: int
    page_count: int



class DocChunksResponse(BaseModel):
    docs       : list[list[DocumentChunk]] = Field(..., description="A list of documents, each containing a list of chunks")
    next_index : int                       = Field(..., description="The index of the next document to return.  Use this value as the index parameter in the next request to get the next set of documents")  
          