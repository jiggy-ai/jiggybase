#! /usr/bin/env python3

import os
import sys
import argparse
import jiggybase

jb = jiggybase.JiggyBase()

JIGGYBASE_ORG = os.environ.get("JIGGYBASE_ORG")
JIGGYBASE_COLLECTION = os.environ.get("JIGGYBASE_COLLECTION")


def upload_directory(collection : jiggybase.models.Collection, dirname : str):
    for fn in os.listdir(dirname):
        fn = os.path.join(dirname, fn)
        print(f'uploading {fn}')
        try:
            upsert_rsp = collection.upsert_file(fn)
        except Exception as e:            
            print(f'error on {fn}: {e}')
            continue
        doc_id = upsert_rsp.ids[0]
        dcl =  collection.get_doc(doc_id)
        text_len = len(" ".join([dc.text for dc in dcl]))
        print(f'uploaded {fn} as {doc_id}: chunk count {len(dcl)} text length {text_len} metadata {dcl[0].metadata}')


def main(args):
    parser = argparse.ArgumentParser(description="Upload a directory to a JiggyBase collection")
    parser.add_argument("--org", type=str, help="The name of your JiggyBase organization")
    parser.add_argument("--collection", type=str, help="The name of your JiggyBase collection")
    parser.add_argument("--dir", type=str, help="The directory you want to upload")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args = parser.parse_args(args)

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

    upload_directory(collection, parsed_args.dir)


if __name__ == "__main__":
    main(sys.argv[1:])
