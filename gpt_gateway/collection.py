from typing import Optional
from pydantic import BaseModel, Field, BaseConfig, HttpUrl
from enum import Enum
from .models import collection


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

        
class Collection(collection.Collection):
    """
    derived from models.collection.Collection data model for purposes of adding management methods
    """
    class Config(BaseConfig):
        extra = "allow"

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        
    def set_description(self, description:str) -> "Collection":
        """
        Update an existing collection using its ID and the provided description.
        """
        patch_request = CollectionPatchRequest(description=description)
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}", model=patch_request)
        return Collection(**rsp.json())

    def set_oauth_verification_token(self, openai_verification_token: str) -> PluginAuthConfigOAuth:
        """
        Set the OpenAI verification token for this collection's plugin.
        This is the token that OpenAI provides during while registering a plugin configured to use Oauth.
        """
        patch_request = PatchPluginOAuthConfigRequest(openai_verification_token=openai_verification_token)
        rsp = self.session.patch(f"/orgs/{self.org_id}/collections/{self.id}/plugin_oauth", model=patch_request)
        return PluginAuthConfigOAuth(**rsp.json())

    def plugin_oauth_config(self) -> PluginAuthConfigOAuth:
        """
        Get the OAuth configuration for this collection's plugin.
        The client_id and client_secret returned here are configured with OpenAI while 
        registering a plugin configured to use Oauth.
        """
        rsp = self.session.get(f"/orgs/{self.org_id}/collections/{self.id}/plugin_oauth")
        return PluginAuthConfigOAuth(**rsp.json())

    def delete(self):
        """
        Delete a collection.  Warning: this is permanent.
        """
        self.session.delete(f"/orgs/{self.org_id}/collections/{self.id}")


