import gpt_gateway as gptg


from gpt_gateway.models import (
    PluginAuthConfigOAuth,
    PluginBearerTokenConfig,
    ChatModelName,
    ChunkConfig,
    PluginAuthType,
    CollectionPostRequest,
    CollectionPatchRequest,
    PatchPluginOAuthConfigRequest,
    Collection,
    EmbeddingModelName,
    EmbeddingConfig,
    ExtractMetadataConfig,
    OrgRole,
    OrgPostRequest,
    OrgPatchRequest,
    OrgMemberPostRequest,
    OrgMember,
    Org,
    PluginConfig,
    ApiKey,
    User,
    UserPostRequest,
    UserPostPatchRequest,
)




if __name__ == "__main__":
    gptg = gptg.GPTGateway()
    orgs = gptg.orgs()
    for org in orgs:
        print(f'Org: {org}')
        for c in org.collections():
            print(f'   Collection: {c}')    
    collections = gptg.collections()