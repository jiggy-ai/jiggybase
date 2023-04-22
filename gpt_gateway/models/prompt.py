from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
from time import time


class PromptMessageRole(str, Enum):
    system              : str = "system"
    user                : str = "user"
    assistant           : str = "assistant"
    collection_context  : str = "collection_context"   # this is a special role that pulls in collection context in subsequent system messages
        
    def __str__(self):
        return str(self.value)

           
class PromptMessage(BaseModel):
    role      : PromptMessageRole  = Field(description="The role of the prompt")
    content   : str                = Field(description="The text of the prompt")
    position  : int                = Field(description="The position offset of the item in the prompt message list. 0-based, with negative values counting from the end.")


class PromptTaskType(Enum, str):
    chat            = "chat"             # iterative chat (e.g. chat with a model with user/assistant message history)
    collection_chat = "collection_chat"  # iterative chat augmented with retreival from a collection
    plugin_chat     = "plugin_chat"      # iterative chat augmented with tool use via plugin interface
    read_write      = "read_write"       # non-iterative task that involve reading a document and producing text or data

       
class PromptTask(BaseModel):
    id          :   int                      = Field(description="The unique ID of the prompt task")
    org_id      :   int                      = Field(description='The Org that owns this.')    
    name        :   str                      = Field(description="The name of the task. Unique within the org.")    
    type        :   Optional[PromptTaskType] = Field(description="The type of task")
    version     :   int                      = Field(description="The version of the task. Unique for a given org and task name.")
    description :   Optional[str]            = Field(description="The description of the task")
    prompts     :   List[PromptMessage]      = Field(description="The prompt messages used in the prompt task")
    created_at  :   float                    = Field(description='The epoch timestamp when the item was created.')

 
class PromptTaskPostRequest(BaseModel):
    name:          str                      = Field(description="The name of the task. Unique within the org.")
    version:       int                      = Field(description="The version of the task. Unique for a given org and task name.")
    type:          Optional[PromptTaskType] = Field(description="The type of task")        
    description:   Optional[str]            = Field(description="The description of the task")
    prompts:       List[PromptMessage]      = Field(description="The items that make up the prompt task")




