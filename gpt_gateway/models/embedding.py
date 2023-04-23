from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum




class EmbeddingModelName(str, Enum):
    ada002 :str = "text-embedding-ada-002"
    
    def __str__(self):
        return str(self.value)    

    
class EmbeddingConfig(BaseModel):
    model : EmbeddingModelName =  Field(EmbeddingModelName.ada002, description="The name of the model to use for embedding the collection content.")
    