import os
from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional
from enum import Enum
from sqlmodel import SQLModel, Field
from .collection import PluginAuthType        
import re

MODELNAME = re.compile("[a-zA-Z][a-zA-Z0-9_]*")

class PluginConfig(BaseModel): 
    """
    The user-customizable part of PluginConfig
    """
    name_for_model:        str = Field("retrieval", max_length=50, description="The name of the plugin as it will be appear to the model.")
    name_for_human:        str = Field(max_length=50, description="The name of the plugin as it will be appear to the human user.")
    description_for_model: str = Field(max_length=4000, description="Description of the plugin as it will appear to the model.")
    description_for_human: str = Field(max_length=120, description="Description of the plugin as it will appear to the human user.")
    logo:                  Optional[str] = Field(description="The logo for the plugin")
    logo_url:              Optional[HttpUrl] = Field(description="The logo url for the plugin")

    @validator('name_for_model')
    def _name_for_model(cls, v):
        if len(v) > 50 or not v:
            raise ValueError(f'"{v}" is an invalid model name. It must not be empty and is limited to 50 characters.')
        elif not bool(MODELNAME.match(v)):
         raise ValueError(f'"{v}" is an invalid model name. It can only contain letters, numbers, and underscores, and must start with a letter.')
        return v


class PatchPluginConfigRequest(BaseModel):
    name_for_model:        Optional[str] = Field(description="The plugin name for the model")
    name_for_human:        Optional[str] = Field(description="The plugin name for human")
    description_for_model: Optional[str] = Field(description="The plugin description for the model")
    description_for_human: Optional[str] = Field(description="The plugin description for human")
    logo:                  Optional[str] = Field(description="The logo for the plugin")
    logo_url:              Optional[HttpUrl] = Field(description="The logo url for the plugin")

    @validator('name_for_model')
    def _name_for_model(cls, v):
        if len(v) > 50 or not v:
            raise ValueError(f'"{v}" is an invalid model name. It must not be empty and is limited to 50 characters.')
        elif not bool(MODELNAME.match(v)):
         raise ValueError(f'"{v}" is an invalid model name. It can only contain letters, numbers, and underscores, and must start with a letter.')
        return v



class OpenAIVerificationToken(BaseModel):
    openai: str


class OpenAIPluginAuthConfigOAuth(BaseModel):
    """
    The Plugin Oauth configuration as it is presented in the ai-plugin.json 
    """
    type:                       str         = Field("oauth", const=True)
    client_url:                 HttpUrl     = Field(description="ChatGPT will direct the user’s browser to this url to log in to the plugin")
    authorization_url:          HttpUrl     = Field(description="After successful login ChatGPT will complete the OAuth flow by making a POST request to this URL")
    scope:                      str         = Field(description="The scope used for the OAuth flow")    
    authorization_content_type: str         = Field("application/json", const=True)
    verification_tokens:        OpenAIVerificationToken = Field(description="The verification token to send to OpenAI for the plugin")

