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
