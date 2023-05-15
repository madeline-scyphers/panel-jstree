"""# Awesome Panel Starter Project

This project was created with the [awesome-panel-cli](https://github.com/awesome-panel/awesome-panel-cli)
"""
import panel as pn
from panel_jstree.widgets import FileTree

pn.extension("tree")


def file_tree():
    ft = FileTree(
        directory="~/Documents",
        checkbox=True
    )
    return pn.Column(ft)


if __name__ == "__main__":
    pn.serve({"file_tree": file_tree}, port=5006, show=False)
