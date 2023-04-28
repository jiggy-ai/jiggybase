from pydantic import BaseModel, Field
from typing import Optional


class PineconeConfig(BaseModel):
    api_key: str = Field(..., description="Your Pinecone API Key")
    environment: str = Field(..., description="Your Pinecone environment")
    index: str = Field(..., description="Your Pinecone index")


class WeaviateConfig(BaseModel):
    host: str = Field(..., description="Your Weaviate host")
    port: int = Field(..., description="Your Weaviate port")
    index: str = Field(..., description="Your Weaviate index")
    username: Optional[str] = Field(None, description="Your Weaviate username")
    password: Optional[str] = Field(None, description="Your Weaviate password")
    scopes: Optional[str] = Field(None, description="Your Weaviate scopes")
    batch_size: Optional[int] = Field(None, description="Your Weaviate batch size")
    batch_dynamic: Optional[bool] = Field(None, description="Your Weaviate batch dynamic")
    batch_timeout_retries: Optional[int] = Field(None, description="Your Weaviate batch timeout retries")
    batch_num_workers: Optional[int] = Field(None, description="Your Weaviate batch number of workers")


class ZillizConfig(BaseModel):
    collection: str = Field(..., description="Your Zilliz collection")
    uri: str = Field(..., description="Your Zilliz URI")
    user: str = Field(..., description="Your Zilliz username")
    password: str = Field(..., description="Your Zilliz password")


class MilvusConfig(BaseModel):
    collection: str = Field(..., description="Your Milvus collection")
    host: str = Field(..., description="Your Milvus host")
    port: str = Field(default="19530", description="Your Milvus port")
    user: str = Field(None, description="Your Milvus username")
    password: str = Field(None, description="Your Milvus password")
    index_params: Optional[str] = Field(..., description="Custom index options for the collection.")
    search_params: Optional[str] = Field(..., description="Custom search options for the collection")
    consistency_level: Optional[str] = Field(..., description="Custom consistency level for the collection")
    
class QdrantConfig(BaseModel):
    url: str = Field(..., description="Your Qdrant URL")
    port: str = Field("6333", description="Your Qdrant port")
    grpc_port: str = Field("6334", description="Your Qdrant gRPC port")
    api_key: str = Field(..., description="Your Qdrant API key")
    collection: str = Field(..., description="Your Qdrant collection")


class RedisConfig(BaseModel):
    host: str = Field(..., description="Your Redis host")
    port: int = Field(..., description="Your Redis port")
    password: str = Field(None, description="Your Redis password")
    index_name: str = Field(..., description="Your Redis index name")
    doc_prefix: str = Field(..., description="Your Redis document prefix")
    distance_metric: Optional[str] = Field(None, description="Your Redis distance metric")
    index_type: Optional[str] = Field(None, description="Your Redis index type")

