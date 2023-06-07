from typing import Optional
from pydantic import BaseModel, Field


        
class CollectionPostRequest(BaseModel):
    """
    Used to create a new Collection service
    """
    display_name: str                      = Field(description="The human friendly display name for the collection.")
    description:  Optional[str]            = Field(description="A description of the collection.")


class CollectionPatchRequest(BaseModel):
    """
    Used to modify an existing service
    """
    description:  Optional[str] = Field(description="A description of the collection.")
    display_name: Optional[str] = Field(description="The human friendly display name for the collection.")





class Collection(BaseModel):
    """
    A managed collection of searchable documents exposed via as a ChatGPT plugin and a REST API.
    """
    id:           int           = Field(description="The unique ID of the service")
    display_name: str           = Field(description="The human friendly display name for the collection.")    
    description:  Optional[str] = Field(description="A description of the collection.")
    hostname:     str           = Field(description="The unique hostname for the collection service. The hostname part of the fqdn")
    fqdn:         str           = Field(description="The FQDN for the collection service")
    org_id:       int           = Field(description='The Org that owns this Service.')
    created_by:   int           = Field(description='The user_id that created this item.')
    updated_by:   int           = Field(description='The user_id that last modified this item.')
    created_at:   float         = Field(description='The epoch timestamp when the collection was created.')
    updated_at:   float         = Field(description='The epoch timestamp when the collection was created.')

