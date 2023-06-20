from pathlib import Path

import panel as pn

from panel_jstree.widgets import FileTree

pn.extension("tree")


def view():
    ft = FileTree(
        directory="..",
    )
    return pn.Column(ft)


if __name__.startswith("bokeh"):
    view().servable()

if __name__ == "__main__":
    pn.serve({Path(__file__).name: view}, port=5006, show=False)
