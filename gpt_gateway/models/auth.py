
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