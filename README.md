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

Assuming you already created a collection 'my-collection', you can add files to the collection as follows:

```python
collection = jb.collection('my-collection')

collection.upsert_file('/path/to/my/doc')

```
The document is now available in the collection and can be accessed by the collection's ChatGPT plugin, via chat.jiggy.ai, or via the associated chat API endpoint.


### JiggyBase Client

These are the top level methods of th `JiggyBase` client, primarily used for getting the user's organizations or all collections across all organizations.

- `orgs()` - Returns a list of `Org` objects the user is a member of.
- `get_org(name_or_id: str)` - Returns the `Org` object matching the given name or ID.
- `api_keys()` - Returns a list of the user's `ApiKey` objects.
- `authenticated_user()` - Returns the authenticated user's `User` object.
- `collections()` - Returns a list of all `Collection` objects in all organizations the user is a member of.
- `collection(name: str)` - Returns the `Collection` object matching the given name.

### Organization

Organizations in JiggyBase are a mechanism for separating different customers within the JiggyBase service.   Users can be a member of mutiple unrelated organizations.  A new user who subscribes to a JiggyBase service tier has their own oganization that they control as administrator of the organization.  Users can also be invited to an organization by existing members of the organization.

For an `Org` object (e.g., `my_org = jb.get_org("<org_name>")`), you have access to the following methods:

- `collections()` - Returns a list of `Collection` objects within the organization.
- `collection(name: str)` - Returns the `Collection` object matching the given name.

- `update([name: Optional[str] = None, description: Optional[str] = None])` - Updates the organization's name or description.


### Collection

A collection is a group of documents that can be used to augment ChatGPT language models with your personalized information by using information from your collection to inform ChatGPT responses.   A collection can be exposed as a ChatGPT Plugin, via the JiggyBase ChatCompletion API, or via chat.jiggy.ai.   You have full control over who can access to your collection.  

For a `Collection` object (e.g., `my_collection = jb.collection("<collection_name>")`), you have access to the following methods:

- `upsert_file(file_path: str[, mimetype: str = None])` - Uploads a file to the collection.
- `upsert(documents: List[Document])` - Adds a list of `Document` objects to the collection.
- `query(queries: Union[str, List[str], Query][, top_k : int = 10])` - Queries the collection and returns a `QueryResponse` object.
- `get_doc(id: str)` - Retrieves a document by its ID.
- `get_chunks([start: int = 0, limit: int = 10, reverse: bool = True])` - Iterates through the chunks in a collection.
- `delete_docs([ids: Optional[List[str]] = None, document_metadata_filter: Optional[DocumentMetadataFilter] = None, delete_all: Optional[bool] = False])` - Deletes items in the collection by document IDs, metadata filter, or deletes all documents.
- `set_description(self, description: str)` - Updates the description of the collection.
- `delete()` - Deletes the collection permanently.
- `get_chat_config()` - Retrieves the chat configuration for the collection.

### Organization User Management

An organization supports multiple roles for members, including 'admin', 'member', and 'viewer'.   A viwer role can access the data in the collection for chat purposes.  A member can upload new documents to the collection.  

- `members()` - Returns a list of `OrgMember` objects within the organization.
- `add_member(email: str, role: OrgRole)` - Adds a new member to the organization with the given email and role.
- `delete_member(email: str)` - Deletes a member from the organization using the given email.

### Organization Prompt Management

JiggyBase supports user-customized prompts for the JiggyBase ChatCompletion API.   The following methods are provided to manage the customized prompts.

- `prompt_tasks([name=None, version=None])` - Returns a list of `PromptTask` objects, optionally filtering by name and version.
- `create_prompt_task(name: str, version: int, prompts: List[PromptMessage][, type: Optional[PromptTaskType] = None, description: Optional[str] = None])` - Creates a new `PromptTask` object with the specified parameters.
- `update_prompt_task(name: str, prompts: List[PromptMessage])` - Updates the specified prompt task's prompts.
- `get_prompt_task(prompt_task_id: int)` - Retrieves a `PromptTask` object using the given prompt_task_id.
- `delete_prompt_task(prompt_task_id: int)` - Deletes a `PromptTask` object using the given prompt_task_id.

## jiggybase_upload

This utility is installed via pip and allows you to upload files or directories to your JiggyBase collection using command-line arguments. It's included in the `jiggybase/examples` directory.

#### Usage

```bash
jiggybase_upload [--org <organization>] [--collection <collection>] [--dir <directory>] [--file <file>]
```

- `--org`: The name of your JiggyBase organization. Alternatively, set `JIGGYBASE_ORG` environment variable, or be a member of a single organization.
- `--collection`: The name of your JiggyBase collection. Alternatively, set the `JIGGYBASE_COLLECTION` environment variable, or have a single collection in your organization.
- `--dir`: The directory you want to upload.
- `--file`: The file you want to upload.

If neither `--file` nor `--dir` options are provided, the script will automatically process other arguments as a file or directory.

