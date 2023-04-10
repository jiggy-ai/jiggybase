import gpt_gateway as gptg


from gpt_gateway.models import (
    ApiKey,
    ChatModelName,
    ChunkConfig,
    Collection,
    CollectionPatchRequest,
    CollectionPostRequest,
    EmbeddingConfig,
    EmbeddingModelName,
    ExtractMetadataConfig,
    Org,
    OrgMember,
    OrgMemberPostRequest,
    OrgPatchRequest,
    OrgPostRequest,
    OrgRole,
    PatchPluginOAuthConfigRequest,
    PluginAuthConfigOAuth,
    PluginAuthType,
    PluginBearerTokenConfig,
    PluginConfig,
    User,
    UserPostPatchRequest,
    UserPostRequest,
)




if __name__ == "__main__":
    gptg = gptg.GPTGateway()
    orgs = gptg.orgs()
    for org in orgs:
        print(f'Org: {org}')
        for c in org.collections():
            print(f'   Collection: {c}')    
    collections = gptg.collections()