#!/usr/bin/env python3

import jiggybase
try:
    import IPython
except:
    raise Exception("'pip install IPython' run this command first")

def main():
    
    print("\nStarting JiggyBase IPython environment\n")

    jb = jiggybase.JiggyBase()
    orgs = jb.orgs()
    collections = jb.collections()
    
    print(f"'jb'          set to jiggybase.JiggyBase() instance")
    print(f"'orgs'        set to list of your orgs")
    print(f"'collections' set to list of your collections")    
    print()    
    IPython.start_ipython(argv=[], user_ns={"jb": jb, "orgs": orgs, "collections": collections})
    

if __name__ == '__main__':
    main()
