#!/usr/bin/env python3
"""
Specification:

Sync the text content in a Confluence Space into a JiggyBase Collection


Takes the following config from the command line or via environment variables:

--user  or ATLASSIAN_USER   environment variable
--token or ATLASSIAN_TOKEN  environment variable   
--url   or CONFLUENCE_URL   environment variable   
--space or CONFLUENCE_SPACE environment variable   The space key, id, or name of the space to sync
--org   or JIGGYBASE_ORG    environment variable   The JiggyBase org to sync to


To create an Atlassian API token go to 
https://id.atlassian.com/manage-profile/security/api-tokens
and click on Create API token. Save the value into an environment variable.
E.g. on Macos
export ATLASSIAN_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


If a JiggyBase API token is not set then the JiggyBase SDK will open a web browser on the page to copy it from the JiggyBase dashboard.

Implementation notes:
Uses page['version']['when'] as document created_at timestamp and version indicator
Uses page['id'] as document id (unique within a collection)

If a given document ID exists in both confluence and jiggybase, check  
Re-uploads a page if the version has changed from what is in the metadata

"""

# pip install atlassian-python-api
from atlassian import Confluence
import os
import argparse
import jiggybase
import requests 


def upsert_file(collection : jiggybase.models.Collection, filename : str):
    print(f'Uploading {filename}')
    try:
        upsert_rsp = collection.upsert_file(filename)
    except Exception as e:            
        print(f'error on {filename}: {e}')
        return
    doc_id = upsert_rsp.ids[0]
    dcl =  collection.get_doc(doc_id)
    text_len = len(" ".join([dc.text for dc in dcl]))
    title = dcl[0].metadata.title if dcl[0].metadata.title else "Unnown Title"
    print(f'Processed {filename}: "{title}"  {text_len//1024} KB text ({len(dcl)} chunks)')


def save_attachment_to_file(confluence, attachment):
    title = attachment['title']
    download_link = attachment['_links']['download']
    download_url = f'{confluence.url}{download_link}'
    
    response = requests.get(download_url, auth=(confluence.username, confluence.password))
    
    if response.status_code == 200:
        with open(title, 'wb') as file:
            file.write(response.content)
        return title
    else:
        print(f"Error downloading attachment '{title}': {response.status_code}")
        return None



def sync_confluence_space_to_jiggybase_collection(confluence, space, org):
    """
    """
    try:
        space_collection = org.collection(space['name'])
        print(f"Found existing JiggyBase collection {space['name']}")
    except:
        space_collection = org.create_collection(space['name'])
        print(f"Created new JiggyBase collection {space['name']}")

    # Delete all documents in the collection
    print(f"Deleting all prior documents in JiggyBase collection {space['name']}")
    space_collection.delete_docs(delete_all=True)

    # Get all pages in the space
    pages = confluence.get_all_pages_from_space(space['key'])

    # Loop through each page and process it
    for page in pages:
        # Download page as Word document
        doc_content = confluence.get_page_as_word(page['id'])
        doc_filename = f"{page['title']}.doc"
        
        # Save the Word document locally
        with open(doc_filename, 'wb') as doc_file:
            doc_file.write(doc_content)
        
        # Upload the Word document to JiggyBase collection
        upsert_file(space_collection, doc_filename)
        os.remove(doc_filename)
        
        # Get all attachments from the page
        attachments = confluence.get_attachments_from_content(page['id'])['results']

        # Download and upload each attachment to JiggyBase collection
        for attachment in attachments:
            if attachment['title'].split('.')[-1] in ['svg']:
                # skip unsupported file types
                continue
            print(f"Downloading attachment {attachment['title']} from page {page['title']}")
            attachment_filename = save_attachment_to_file(confluence, attachment)
            if attachment_filename:
                upsert_file(space_collection, attachment_filename)            
            os.remove(attachment_filename)
                
        print(f"Finished syncing {page['title']} and its attachments.")


        

def main():
    # Handle command line arguments and environment variables
    parser = argparse.ArgumentParser(description="Sync Confluence Space to JiggyBase Collection")
    parser.add_argument('--user', default=os.environ.get('ATLASSIAN_USER'))
    parser.add_argument('--token', default=os.environ.get('ATLASSIAN_TOKEN'))
    parser.add_argument('--url', default=os.environ.get('CONFLUENCE_URL'))
    parser.add_argument('--space', default=os.environ.get('CONFLUENCE_SPACE'))
    parser.add_argument('--org', default=os.environ.get('JIGGYBASE_ORG'))
    
    args = parser.parse_args()

    jb = jiggybase.JiggyBase()

    orgs = jb.orgs()
        
   # Check if all required arguments are provided
    missing_args = []
    if not args.user:
        missing_args.append('--user  or ATLASSIAN_USER   environment variable')
    if not args.token:
        missing_args.append('--token or ATLASSIAN_TOKEN  environment variable')
    if not args.url:
        missing_args.append('--url   or CONFLUENCE_URL   environment variable')
    if not args.org and len(orgs) > 1:
        missing_args.append('--org   or JIGGYBASE_ORG   environment variable')
        
    if missing_args:
        print("\nError: The following required arguments are missing:")
        for arg in missing_args:
            print(f"- {arg}")
        print()
        parser.print_help()
        return
    
    # Connect to Confluence API
    confluence = Confluence(args.url, username=args.user, password=args.token)
    
    # Get all spaces and find the matching space
    all_spaces = confluence.get_all_spaces()
    matching_space = None
    
    for space in all_spaces['results']:
        if args.space in [space['key'], space['name'], str(space['id'])]:
            matching_space = space
            break

    if matching_space:
        print(f"Matched Space: {matching_space['name']} (ID: {matching_space['id']})")
    else:
        print("No matching space found. Available spaces:")
        for space in all_spaces['results']:
            print(f"- {space['name']:20}  (ID: {space['id']})  key = {space['key']}")
        return
    
    if len(orgs) == 1:
        org = orgs[0]
    else:
        org = jb.get_org(args.org)
    print(f"Using JiggyBase org {org.name} (ID: {org.id})")
    
    sync_confluence_space_to_jiggybase_collection(confluence, matching_space, org)

if __name__ == "__main__":
    main()

