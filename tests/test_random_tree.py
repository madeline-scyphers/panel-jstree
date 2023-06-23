import random

import panel as pn
from pathlib import Path

from panel_jstree import Tree

pn.extension("tree", sizing_mode="stretch_width")


def random_cb(text, id_, **kwargs):
    def get_random_text(n):
        return random.sample(list("abcdefghijklmnopqrstuvwxyz"), n)

    def get_random_nodes(pnt):
        children = [Tree.to_json(id_=f"{pnt}_{label}", label=label, parent=pnt)
                    for label in get_random_text(random.randint(0, 4))]
        return children

    nodes = get_random_nodes(id_)
    return nodes


def test_random_tree_app():
    """Construct a BaseTree for manual testing"""
    tree = Tree(
        data=[
       {
           'text': 'a',
           "id": "a",
           'children': [
               {'text': 'b',
                'id': 'a_b'},
               {'text': 'a',
                'id': 'a_a'}
         ]
      }
    ],
        get_children_cb=random_cb,
    )

    settings = pn.Param(
        tree,
        parameters=[
            "select_multiple",
            "show_icons",
            "show_dots",
            "checkbox",
        ]
    )

    text_input = pn.widgets.TextInput(name="Text Input", placeholder="Enter the uuid to node: a_b_c_d etc")

    @pn.depends(text_input, watch=True)
    def text_box_cb(val):
        tree.value = [val]

    return pn.template.FastListTemplate(
        site="Panel jsTree",
        title="Random Tree Editor",
        main=[tree, text_input],
        sidebar=[settings],
    )


if __name__.startswith("bokeh"):
    test_random_tree_app().servable()


if __name__ == "__main__":
    pn.serve({Path(__file__).name: test_random_tree_app()}, port=5008, show=False)
