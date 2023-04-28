
from typing import Optional, Union
from pydantic import BaseModel
from enum import Enum


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
    author: Union[str, list[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    

class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[list[float]] = None


class DocumentChunkWithScore(DocumentChunk):
    score: float



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

class QueryRequest(BaseModel):
    queries: list[Query]

class QueryResponse(BaseModel):
    results: list[QueryResult]
