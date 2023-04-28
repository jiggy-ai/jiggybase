from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum

from .chatmodel import ChatModelName

class ExtractMetadataConfig(BaseModel):
    """
    configuration for metadata extraction
    """
    created_at:  bool          = Field(True, description="Attempt to extract the created_at metadata field")
    author:      bool          = Field(True, description="Attempt to extract the author metadata field")
    title:       bool          = Field(True, description="Attempt to extract the title metadata field")
    model:       ChatModelName = Field(ChatModelName.gpt4, description="The name of the model to use for metadata extraction")
