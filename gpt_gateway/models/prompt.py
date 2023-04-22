from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
from time import time


class PrompMessageRole(str, Enum):
    system   : str = "system"
    user     : str = "user"
    assistant: str = "assistant"
    
    def __str__(self):
        return str(self.value)


class PromptMessage(BaseModel):
   id     :    int               = Field(description="The unique ID of the prompt message")
   org_id :    int               = Field(description="The unique ID of the org that this prompt belongs to")
   role   :    PrompMessageRole  = Field(description="The role of the prompt")
   content:    str               = Field(description="The text of the prompt")
   created_at: float             = Field(description="The time the prompt was created")


class PromptPostRequest(BaseModel):
   role   : PrompMessageRole  = Field(description="The role of the prompt")
   content: str               = Field(description="The text of the prompt")
   
   @validator('content')
   def content_must_not_be_empty(cls, v):
       if v == "":
           raise ValueError("content must not be empty")
       return v


   
   
   