import panel as pn
from pathlib import Path

from panel_jstree import Tree

pn.extension("tree", sizing_mode="stretch_width")


A = [
       'Simple root node',
       {
         'text' : 'Root node 2',
         'state' : {
           'opened' : True,
         },
         'children' : [
           { 'text' : 'Child 1' },
           'Child 2'
         ]
      }
    ]

B = [
       'B',
       {
         'text' : 'D',
         'state' : {
           'opened' : True,
         },
         'children' : [
           { 'text' : 'CD' },
           'FG'
         ]
      }
    ]

counter = 0


def test_tree_can_construct():
    Tree(data=A)


def test_base_tree_app():
    """Construct a BaseTree for manual testing"""
    tree = Tree(data=A)

    settings = pn.Param(
        tree,
        parameters=[
            "select_multiple",
            "show_icons",
            "show_dots",
            "checkbox",
        ]
    )
    button = pn.widgets.Button(name="change data")

    @pn.depends(button, watch=True)
    def cb(*event):
        global counter
        counter += 1
        tree.data = A if counter % 2 == 0 else B

    return pn.template.FastListTemplate(
        site="Panel jsTree",
        title="Simple Tree Editor",
        main=[tree, button],
        sidebar=[settings],
    )


if __name__.startswith("bokeh"):
    test_base_tree_app().servable()


if __name__ == "__main__":
    pn.serve({Path(__file__).name: test_base_tree_app()}, port=5007, show=False)
