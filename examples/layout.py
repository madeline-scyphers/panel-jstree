from pathlib import Path

import panel as pn

from panel_jstree.widgets.jstree import FileTree

pn.extension("tree")


def view():
    text_input = pn.widgets.TextInput(name="Text Input", placeholder="Enter a string here...")
    ft = FileTree(
        "..",
        select_multiple=True,
        # checkbox=False,
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
    pn.serve({Path(__file__).name: view}, port=5007, show=False)