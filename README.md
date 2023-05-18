# ✨ panel-jstree

We want to


You can install and use the package as simple as.

clone the repo and run:

```bash
conda env create
```

and run:

```bash
panel build src/panel_jstree
```


Example

```python
import panel as pn
from panel_jstree.widgets.jstree import jsTree

pn.extension("tree")

tree = jsTree(
        data = [
           'Simple root node',
           {
             'text' : 'Root node 2',
             'state' : {
               'opened' : True,
               'selected' : True
             },
             'children' : [
               { 'text' : 'Child 1' },
               'Child 2'
             ]
          }
        ]
    )
pn.Column(tree)
```

Run example:

```bash
python -m apps.app
```