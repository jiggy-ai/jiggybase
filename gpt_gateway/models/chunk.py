from pydantic import BaseModel, Field


class ChunkConfig(BaseModel):
    """
    configuration for chunking policy
    """
    chunk_size:                 int = Field(200,   description="The target size of each text chunk in tokens")
    min_chunk_size_chars:       int = Field(350,   description="The minimum size of each text chunk in characters")
    min_chunk_length_to_embed:  int = Field(  5,   description="Discard chunks shorter than this")
    embeddings_batch_size:      int = Field(128,   description="The number of embeddings to request at a time")
    max_num_chunks:             int = Field(10000, description="The maximum number of chunks to generate from a text")
