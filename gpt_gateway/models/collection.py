from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
import re
from time import time


class PluginAuthType(str, Enum):
    bearer :str = "bearer"
    none   :str = "none"
    oauth  :str = "oauth"
    

        
class CollectionPostRequest(BaseModel):
    """
    Used to create a new Collection service
    """
    name:         str                      = Field(description="The globally unique hostname for the collection. Subject to DNS naming rules. ")
    display_name: str                      = Field(description="The human friendly display name for the collection.")
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




# Use DNS naming rules for convenience as they prohibit special characters, underscores, spaces, etc.
ALLOWED_NAME = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)   # REGEX for valid Name, based on DNS name component requirements
        
class Collection(BaseModel):
    """
    A managed collection of searchable documents exposed via as a ChatGPT plugin and a REST API.
    """
    id:          int            = Field(description="The unique ID of the service")
    name:        str            = Field(description="The DNS hostname for the service. The subdomain, not the FQDN.  Subject to DNS naming rules.")
    display_name: str           = Field(description="The human friendly display name for the collection.")    
    description: Optional[str]  = Field(description="A description of the collection.")
    fqdn:        str            = Field(description="The FQDN for the service, derived from the hostname and the domain name.")
    org_id:      int            = Field(description='The Org that owns this Service.')
    created_by:  int            = Field(description='The user_id that created this item.')
    updated_by:  int            = Field(description='The user_id that last modified this item.')
    plugin_auth: PluginAuthType = Field(description='The auth plugin to use for this org.')
    created_at:  float          = Field(description='The epoch timestamp when the collection was created.')
    updated_at:  float          = Field(description='The epoch timestamp when the collection was created.')

    @validator('name')
    def _name(cls, v):
        if len(v) > 63 or not v:
            raise ValueError(f'{v} is an invalid name. It must not be empty and is limited to 63 characters.')
        elif not bool(ALLOWED_NAME.match(v)):
            raise ValueError(f'{v} is an invalid name. It can only contain letters, numbers, and hyphens, and must not start or end with a hyphen.')
        return v
