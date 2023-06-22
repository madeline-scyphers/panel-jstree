from pathlib import Path
import random

import panel as pn

from panel_jstree import Tree

pn.extension("tree")

def view():
    def random_cb(text, id_, **kwargs):
        def get_random_text(n):
            return random.sample(list("abcdefghijklmnopqrstuvwxyz"), n)
        def get_random_nodes(pnt):
            children = [Tree.to_json(id_=f"{pnt}_{label}", label=label, parent=pnt)
                        for label in get_random_text(random.randint(0, 4))]
            return children
        nodes = get_random_nodes(id_)
        return nodes

    text_input = pn.widgets.TextInput(name="Text Input", placeholder="Enter a string here...")
    ft = Tree(
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
    checkboxes2 = pn.widgets.ToggleGroup(
        options=["a", "b", "c"],
    )

    cb1 = pn.widgets.Checkbox(name="Show icons", value=True)
    cb2 = pn.widgets.Checkbox(name="select multiple", value=False)
    cb3 = pn.widgets.Checkbox(name="show dots", value=True)

    @pn.depends(cb1, watch=True)
    def uu2(val):
        ft.show_icons = val

    @pn.depends(cb2, watch=True)
    def uu1(val):
        ft.select_multiple = val

    @pn.depends(cb3, watch=True)
    def uu1(val):
        ft.show_dots = val

    @pn.depends(text_input, watch=True)
    def text_box_cb(val):
        ft.value = [val]

    return pn.Column(
        # df_pane,
        # checkboxes,
        text_input,
        pn.Card(ft, title="File Picker"),
        # ft,
        checkboxes2,
        cb1,
        cb2,
        cb3,
    )


if __name__.startswith("bokeh"):
    view().servable()

if __name__ == "__main__":
    pn.serve({Path(__file__).name: view}, port=5008, show=False)