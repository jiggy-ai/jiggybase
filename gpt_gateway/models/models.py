from .auth import *
from .user import *
from .org import *
from .embedding import *
from .metadata import *
from .chunk import *
from .chatmodel import *
from .plugin import *
from .collection import *
from .prompt import *


from pydantic import BaseModel, Field, HttpUrl
from typing import List



class PluginAuthConfigOAuth(BaseModel):
    """
    The Plugin Oauth configuration when plugin_auth == PluginAuthType.oauth
    """    
    client_url:                 HttpUrl     = Field(description="ChatGPT will direct the user’s browser to this url to log in to the plugin")
    authorization_url:          HttpUrl     = Field(description="After successful login ChatGPT will complete the OAuth flow by making a POST request to this URL")
    scope:                      str         = Field(description="The scope used for the OAuth flow")
    client_id:                  str         = Field(unique=True, index=True, description="The client id to send to OpenAI for the plugin")
    client_secret:              str         = Field(description="The client secret to send to OpenAI for the plugin")
    openai_verification_token:  str         = Field(description="The verification token specified by OpenAI to configure in the plugin")




class PluginBearerTokenConfig(BaseModel):
    """
    A list of bearer tokens that are authorized to access the /plugin api when plugin_auth == PluginAuthType.bearer
    """
    authorized_tokens : List[str]  =  []    
from enum import Enum

 
class ChatModelName(Enum):
    gpt3_5_turbo :str = "gpt-3-5-turbo"
    gpt4         :str = "gpt-4"
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
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
import re



class PluginAuthType(Enum):
    bearer :str = "bearer"
    none   :str = "none"
    oauth  :str = "oauth"

        
class CollectionPostRequest(BaseModel):
    """
    Used to create a new Collection service
    """
    name:         str                      = Field(description="The globally unique hostname for the collection. Subject to DNS naming rules. ")
    display_name: Optional[str]            = Field(description="The human friendly display name for the collection.")
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
    id:          int           = Field(description="The unique ID of the service")
    name:        str           = Field(description="The DNS hostname for the service. The subdomain, not the FQDN.  Subject to DNS naming rules.")
    description: Optional[str] = Field(description="A description of the collection.")
    fqdn:        str           = Field(description="The FQDN for the service, derived from the hostname and the domain name.")
    org_id:      int           = Field(description='The Org that owns this Service.')
    created_by:  int           = Field(description='The user_id that created this item.')
    updated_by:  int           = Field(description='The user_id that last modified this item.')
    plugin_auth: str           = Field(description='The auth plugin to use for this org.')


    @validator('name')
    def _name(cls, v):
        if len(v) > 63 or not v:
            raise ValueError(f'{v} is an invalid name. It must not be empty and is limited to 63 characters.')
        elif not bool(ALLOWED_NAME.match(v)):
            raise ValueError(f'{v} is an invalid name. It can only contain letters, numbers, and hyphens, and must not start or end with a hyphen.')
        return v
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum




class EmbeddingModelName(Enum):
    ada002 :str = "text-embedding-ada-002"
    
class EmbeddingConfig(BaseModel):
    model : EmbeddingModelName =  Field(EmbeddingModelName.ada002, description="The name of the model to use for embedding the collection content.")
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
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from enum import Enum



class OrgRole(str, Enum):
    admin   = 'admin'
    member  = 'member'
    service = 'service'
    view    = 'view'
    

class OrgPostRequest(BaseModel):
    name:        str           = Field(min_length=1, max_length=39, description='Unique name for this org.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')

class OrgPatchRequest(BaseModel):
    name:        Optional[str] = Field(max_length=39, description='Unique name for this org.')
    description: Optional[str] = Field(max_length=255, description='Optional user supplied description.')

class OrgMemberPostRequest(BaseModel):
    email:  EmailStr          = Field(description='The user_id of a member to invite to the org.')
    role:        OrgRole      = Field(description='The users role in the org')

class OrgMember(BaseModel):
    id:                  int      = Field(description="Unique membership id")
    name:                str      = Field(description="Member name")
    email:               EmailStr  = Field(description="Member email")    
    created_at:          float    = Field(description='The epoch timestamp when the membership was created.')
    updated_at:          float    = Field(description='The epoch timestamp when the membership was updated.')
    invited_by_name: str      = Field(description="The name that invited this member to the org.")
    role:                OrgRole = Field(description="The user's role in the org")
    accepted:            bool     = Field(description='True if the user has accepted the org membership.')
    
     
class Org(BaseModel):
    id:          int           = Field(description='Internal org id')
    name:        str           = Field(min_length=1, max_length=39, description='Unique name for this org.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')
    created_at:  float         = Field(description='The epoch timestamp when the org was created.')
    updated_at:  float         = Field(description='The epoch timestamp when the org was updated.')
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
    logo:                  Optional[str] = Field(description="The URL of the logo for the plugin.")


    @validator('name_for_model')
    def _name_for_model(cls, v):
        if len(v) > 50 or not v:
            raise ValueError(f'"{v}" is an invalid model name. It must not be empty and is limited to 50 characters.')
        elif not bool(MODELNAME.match(v)):
         raise ValueError(f'"{v}" is an invalid model name. It can only contain letters, numbers, and underscores, and must start with a letter.')
        return v
     from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from enum import Enum

###
## API Key
###


class  ApiKey(BaseModel):
    key:         str           = Field(default=None, description='The api key.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description of the key.')
    created_at:  float         = Field(description='The epoch timestamp when the key was created.')
    last_used :  float         = Field(description='The epoch timestamp when the key was last used to create a JWT.')
    
###
## User
###

class User(BaseModel):
    id:              int = Field(description='Internal user_id')
    name:            str = Field(min_length=1, max_length=39, description='Unique name for the user.')
    email:           EmailStr  = Field(description='Email address for the user.')    
    auth0_userid:    str = Field(description='Auth0 userid.  This can be None for anonymous accounts created via api key')


class UserPostRequest(BaseModel):
    name:        str = Field(min_length=1, max_length=39, description='Unique name for the user.')
    description: Optional[str] = Field(default=None, max_length=255, description='Optional user supplied description.')
    

class UserPostPatchRequest(BaseModel):
    name:        Optional[str] = Field(min_length=1, max_length=39, description='Unique name for the user.')
    description: Optional[str] = Field(default=None, max_length=255, description='Optional user supplied description.')
