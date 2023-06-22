from pathlib import Path

import panel as pn

from panel_jstree import Tree

pn.extension("tree")


A = [
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

B = [
       'B',
       {
         'text' : 'D',
         'state' : {
           'opened' : True,
           'selected' : True
         },
         'children' : [
           { 'text' : 'CD' },
           'FG'
         ]
      }
    ]

counter = 0

def view():
    text_input = pn.widgets.TextInput(name="Text Input", placeholder="Enter a string here...")
    ft = Tree(
        data=A
    )
    checkboxes2 = pn.widgets.ToggleGroup(
        options=["a", "b", "c"],
    )

    cb1 = pn.widgets.Button(name="change data")
    cb2 = pn.widgets.Checkbox(name="select multiple", value=False)
    cb3 = pn.widgets.Checkbox(name="show dots", value=True)

    @pn.depends(cb1, watch=True)
    def uu1(val):
        global counter
        counter += 1
        ft.data = A if counter % 2 == 0 else B

    @pn.depends(cb2, watch=True)
    def uu2(val):
        ft.select_multiple = val

    @pn.depends(cb3, watch=True)
    def uu3(val):
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
    pn.serve({Path(__file__).name: view}, port=5009, show=False)