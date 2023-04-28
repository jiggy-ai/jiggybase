# GPT-Gateway

This is a Python package for the GPT-Gateway providing a simple and convenient way to utilize core Org, Collection, and User functions. GPT-Gateway is a management system for your manageable collections of searchable documents exposed via a powerful ChatGPT plugin and a user-friendly REST API.

## Features

1. Manage Organizations (Org)
2. Manage Collections
3. Manage Users and their API keys
4. Manage authentication for accessing the ChatGPT plugin

## Installation

Please follow the instructions to install this package using `pip`:

```bash
pip install gpt-gateway
```

## Usage

Here is a brief overview of the core functionality available in this package.

### 1. Orgs Management

To manage your organizations, you can use the available Org class methods. Here is a summary of some of those methods:

- `orgs`: Returns a list of all Orgs that the user is a member of.
- `create_org`: Create a new Org with the specified name.
- `members`: Returns a list of all members in an Org.
- `add_member`: Add a new member to the Org with specified email and role.
- `delete_member`: Remove a member from the Org using their email.
- `update`: Update the name or description of the Org.

### 2. Collections Management

The Collection class provides methods to manage your collections within an organization. Here is a summary of some key methods:

- `create_collection`: Create a new Collection with the specified name, plugin_auth and description.
- `collections`: Returns a list of all Collections in all Orgs that the user is a member of.
- `set_description`: Update the description of an existing collection.
- `set_oauth_verification_token`: Set the OpenAI verification token for this collection's plugin.
- `plugin_oauth_config`: Get the OAuth configuration for this collection's plugin.
- `delete`: Delete a collection. Warning: this is permanent.

### 3. Users and API Keys Management

This package allows managing User information and their API keys. Some of the key functions include:

- `api_keys`: Return a list of the user's API keys.
- `authenticated_users`: Returns the authenticated user's User object.
- `create_user`: Create a user with specified name and description.
- `update_user`: Update the name and/or description of the user.

## Examples

```
from gpt_gateway import GPTGateway

# Initialize the GPTGateway
gateway = GPTGateway()

# Create a new organization
new_org = gateway.create_org("My New Org")

# Get all organizations
orgs = gateway.orgs()

# Create a new collection in the organization
new_collection = new_org.create_collection("My New Collection")

# Get all collections in the organization
all_collections = new_org.collections()

# Get the authenticated user
current_user = gateway.authenticated_user()

# Get all API keys for the user
api_keys = gateway.api_keys()

# Update the name and/or description of the organization
new_org = new_org.update(name="Updated Org Name", description="Updated Org Description")
```

# Example for creating plugin with Oauth user authentication

```
from gpt_gateway import GPTGateway

# Initialize the GPTGateway
gateway = GPTGateway()

# Create a new organization
new_org = gateway.create_org("My New Org")

# Create a new collection with OAuth authentication
new_collection = new_org.create_collection("My OAuth Collection", plugin_auth="oauth")

# Get the OAuth configuration for the collection's plugin
oauth_config = new_collection.plugin_oauth_config()

print("OAuth Configuration:")
print(f"Client ID: {oauth_config.client_id}")
print(f"Client Secret: {oauth_config.client_secret}")

# Set the OpenAI verification token for the collection's plugin

new_config = new_collection.set_oauth_verification_token("your_openai_verification_token")

```
