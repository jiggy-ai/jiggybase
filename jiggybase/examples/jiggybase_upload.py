#! /usr/bin/env python3

import os
import sys
import argparse
import jiggybase

jb = jiggybase.JiggyBase()

JIGGYBASE_ORG = os.environ.get("JIGGYBASE_ORG")
JIGGYBASE_COLLECTION = os.environ.get("JIGGYBASE_COLLECTION")


def upload_file(collection : jiggybase.models.Collection, filename : str):
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
    

def upload_directory(collection : jiggybase.models.Collection, dirname : str):
    for fn in os.listdir(dirname):
        fn = os.path.join(dirname, fn)
        upload_file(collection, fn)


epilog = "If neither '--file' nor '--dir' options are provided, the script will automatically process other arguments as a file or directory"


def main():
    parser = argparse.ArgumentParser(description="Upload a file or directory to a JiggyBase collection",  epilog=epilog )    
    parser.add_argument("--org", type=str, help="The name of your JiggyBase organization.  Alternatively, set JIGGYBASE_ORG environment variable or be a member of a single Org.")
    parser.add_argument("--collection", type=str, help="The name of your JiggyBase collection. Alternatively, set JIGGYBASE_COLLECTION environment variable or have a single collection in your org.")
    parser.add_argument("--dir", type=str, help="The directory you want to upload.")
    parser.add_argument("--file", type=str, help="The file you want to upload")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args, unknown_args = parser.parse_known_args(sys.argv[1:])
    if not parsed_args.org:
        orgs = jb.orgs()
        if len(orgs) > 1:
            print("Please provide an organization name using the --org option")
            sys.exit(1)
        elif JIGGYBASE_ORG:
            org = jb.get_org(JIGGYBASE_ORG)
        else:
            org = orgs[0]
    else:
        org = jb.get_org(parsed_args.org)

    if not parsed_args.collection:
        collections = org.collections()
        if len(collections) > 1:
            print("Please provide a collection name using the --collection option")
            sys.exit(1)
        elif JIGGYBASE_COLLECTION:
            collection = org.collection(JIGGYBASE_COLLECTION)
        else:
            collection = collections[0]
    else:
        collection = org.collection(parsed_args.collection)

    if parsed_args.dir:
        upload_directory(collection, parsed_args.dir)
    elif parsed_args.file:
        upload_file(collection, parsed_args.file)
    elif unknown_args:
        for arg in unknown_args:
            if os.path.isfile(arg):
                upload_file(collection, arg)
            elif os.path.isdir(arg):
                upload_directory(collection, arg)
            else:
                print(f"Skipping unknown argument: {arg}")
    else:
        print("Please provide a valid file or directory to upload")
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
