from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

import jiggybase

jb = jiggybase.JiggyBase()

print()
print('JiggyBase ipython environment...')
print()
print(f"local variable 'jb' set to jiggybase.JiggyBase() instance")

orgs = jb.orgs()
collections = jb.collections()
print(f"local variables 'orgs' and 'collections' set to lists of orgs and collections")
print()