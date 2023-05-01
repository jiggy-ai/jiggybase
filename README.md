# JiggyBase

JiggyBase is a Python library for interacting with the JiggyBase service at https://jiggy.ai.

Use it to manage your JiggyBase organization and collections, including uploading documents into a collection.

## Requirements

- Python 3.6 or above

## Installation

```bash
pip install jiggybase
```

## Client Usage

To start using JiggyBase in your Python code, you first need to import it:

```python
import jiggybase
```

After importing, you need to create a JiggyBase client object:

```python
jb = jiggybase.JiggyBase()
```


### Client methods

Here are the available `JiggyBase` client methods:

- `orgs()` - Returns a list of `Org` objects the user is a member of.
- `get_org(name_or_id: str)` - Returns the `Org` object matching the given name or ID.
- `api_keys()` - Returns a list of the user's `ApiKey` objects.
- `authenticated_user()` - Returns the authenticated user's `User` object.
- `collections()` - Returns a list of all `Collection` objects in all organizations the user is a member of.
- `collection(name: str)` - Returns the `Collection` object matching the given name.

### Organization methods

For an `Org` object (e.g., `my_org = jb.get_org("<org_name>")`), you have access to the following methods:

- `collections()` - Returns a list of `Collection` objects within the organization.
- `collection(name: str)` - Returns the `Collection` object matching the given name.

- `update([name: Optional[str] = None, description: Optional[str] = None])` - Updates the organization's name or description.


### Collection methods

For a `Collection` object (e.g., `my_collection = jb.collection("<collection_name>")`), you have access to the following methods:

(adapt the usage code for each method accordingly)

- `set_description(self, description: str)` - Updates the description of the collection.
- `set_oauth_verification_token(self, openai_verification_token: str)` - Sets the OpenAI verification token for the collection's plugin.
- `plugin_oauth_config()` - Retrieves the OAuth configuration for the collection's plugin.
- `delete()` - Deletes the collection permanently.
- `get_chat_config()` - Retrieves the chat configuration for the collection.
- `update_chat_config(model: str, prompt_task_id: int)` - Updates the chat configuration for the collection.
- `upsert_file(file_path: str[, mimetype: str = None])` - Uploads a file to the collection.
- `upsert(documents: List[Document])` - Adds a list of `Document` objects to the collection.
- `query(queries: Union[str, List[str], Query][, top_k : int = 10])` - Queries the collection and returns a `QueryResponse` object.
- `get_doc(id: str)` - Retrieves a document by its ID.
- `get_chunks([start: int = 0, limit: int = 10, reverse: bool = True])` - Iterates through the chunks in a collection.
- `delete_docs([ids: Optional[List[str]] = None, document_metadata_filter: Optional[DocumentMetadataFilter] = None, delete_all: Optional[bool] = False])` - Deletes items in the collection by document IDs, metadata filter, or deletes all documents.

### Organization User Management

- `members()` - Returns a list of `OrgMember` objects within the organization.
- `add_member(email: str, role: OrgRole)` - Adds a new member to the organization with the given email and role.
- `delete_member(email: str)` - Deletes a member from the organization using the given email.

### Organization Prompt Management

- `prompt_tasks([name=None, version=None])` - Returns a list of `PromptTask` objects, optionally filtering by name and version.
- `create_prompt_task(name: str, version: int, prompts: List[PromptMessage][, type: Optional[PromptTaskType] = None, description: Optional[str] = None])` - Creates a new `PromptTask` object with the specified parameters.
- `update_prompt_task(name: str, prompts: List[PromptMessage])` - Updates the specified prompt task's prompts.
- `get_prompt_task(prompt_task_id: int)` - Retrieves a `PromptTask` object using the given prompt_task_id.
- `delete_prompt_task(prompt_task_id: int)` - Deletes a `PromptTask` object using the given prompt_task_id.