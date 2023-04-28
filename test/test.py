import jiggybase


from jiggybase.models import (
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
    PromptTask
)




if __name__ == "__main__":
    jb = jiggybase.JiggyBase()
    orgs = jb.orgs()
    for org in orgs:
        print(f'Org: {org}')
        print(org.prompt_tasks())
        for c in org.collections():
            print(f'   Collection: {c}')    
    collections = jb.collections()