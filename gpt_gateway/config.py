
# Add these imports in the import section
from models.collection import PluginAuthType
from models.config import PluginConfig, EmbeddingConfig, ChunkConfig, ExtractMetadataConfig, CollectionAuthConfig, PatchPluginConfigRequest, PatchEmbeddingConfigRequest, PatchChunkConfigRequest, PatchExtractMetadataConfigRequest, PatchAuthTokensRequest

# Existing classes and functions

# Add these new functions for Collection Configuration

def get_plugin_config(org_id: int, collection_id: int) -> PluginConfig:
    rsp = session.get(f"/orgs/{org_id}/collections/{collection_id}/plugin_config")
    return PluginConfig(**rsp.json())

def patch_plugin_config(org_id: int, collection_id: int, data: PatchPluginConfigRequest) -> PluginConfig:
    rsp = session.patch(f"/orgs/{org_id}/collections/{collection_id}/plugin_config", model=data)
    return PluginConfig(**rsp.json())

def get_embedding_config(org_id: int, collection_id: int) -> EmbeddingConfig:
    rsp = session.get(f"/orgs/{org_id}/collections/{collection_id}/embedding_config")
    return EmbeddingConfig(**rsp.json())

def patch_embedding_config(org_id: int, collection_id: int, data: PatchEmbeddingConfigRequest) -> EmbeddingConfig:
    rsp = session.patch(f"/orgs/{org_id}/collections/{collection_id}/embedding_config", model=data)
    return EmbeddingConfig(**rsp.json())

def get_chunk_config(org_id: int, collection_id: int) -> ChunkConfig:
    rsp = session.get(f"/orgs/{org_id}/collections/{collection_id}/chunk_config")
    return ChunkConfig(**rsp.json())

def patch_chunk_config(org_id: int, collection_id: int, data: PatchChunkConfigRequest) -> ChunkConfig:
    rsp = session.patch(f"/orgs/{org_id}/collections/{collection_id}/chunk_config", model=data)
    return ChunkConfig(**rsp.json())

def get_extract_metadata_config(org_id: int, collection_id: int) -> ExtractMetadataConfig:
    rsp = session.get(f"/orgs/{org_id}/collections/{collection_id}/extract_metadata_config")
    return ExtractMetadataConfig(**rsp.json())

def patch_extract_metadata_config(org_id: int, collection_id: int, data: PatchExtractMetadataConfigRequest) -> ExtractMetadataConfig:
    rsp = session.patch(f"/orgs/{org_id}/collections/{collection_id}/extract_metadata_config", model=data)
    return ExtractMetadataConfig(**rsp.json())

def get_auth_tokens(org_id: int, collection_id: int) -> CollectionAuthConfig:
    rsp = session.get(f"/orgs/{org_id}/collections/{collection_id}/tokens")
    return CollectionAuthConfig(**rsp.json())

def patch_auth_tokens(org_id: int, collection_id: int, data: PatchAuthTokensRequest) -> CollectionAuthConfig:
    rsp = session.patch(f"/orgs/{org_id}/collections/{collection_id}/tokens", model=data)
    return CollectionAuthConfig(**rsp.json())
