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

    cb1 = pn.widgets.Button(name="change data")

    @pn.depends(cb1, watch=True)
    def uu1(val):
        global counter
        counter += 1
        ft.data = A if counter % 2 == 0 else B

    @pn.depends(text_input, watch=True)
    def text_box_cb(val):
        ft.value = [val]

    return pn.Column(
        # df_pane,
        # checkboxes,
        text_input,
        pn.Card(ft, title="File Picker"),
        # ft,
        cb1,
    )


if __name__.startswith("bokeh"):
    view().servable()

if __name__ == "__main__":
    pn.serve({Path(__file__).name: view}, port=5009, show=False)