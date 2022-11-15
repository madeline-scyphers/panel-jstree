import panel as pn
pn.__version__ = "0.14.0"  # hv needs this and I am using a dev install
import numpy as np
from panel_jstree.widgets.jstree import FileTree
import pandas as pd
from bokeh.sampledata.autompg import autompg
pn.extension('tabulator')

# import holoviews as hv

# pn.extension("jstree")


def view():
    # distributions = {
    #     'NORMAL': np.random.normal,
    #     'UNIFORM': np.random.uniform,
    #     'LOG-NORMAL': np.random.lognormal,
    #     'EXPONENTIAL': np.random.exponential
    # }

    checkboxes = pn.widgets.ToggleGroup(options=["a", "b", "c"],)
    # slider = pn.widgets.IntSlider(name='Number of observations', value=500, start=0, end=2000)
    ft = FileTree()

    # df = pd.util.testing.makeDataFrame()
    df_pane = pn.widgets.Tabulator(autompg, groupby=['yr', 'origin'])

    # @pn.depends(checkboxes.param.value, slider.param.value)
    # def tabs(distribution, n):
    #     values = hv.Dataset(distribution(size=n), 'values')
    #     return pn.Tabs(
    #         ('Plot', values.hist(adjoin=False).opts(
    #             responsive=True, max_height=500, padding=0.1, color="#00aa41")),
    #         ('Summary', values.dframe().describe().T),
    #         ('Table', hv.Table(values)),
    #     )


    ft = FileTree("/Users/madelinescyphers/Documents/projs_.nosync/panel-jstree", sizing_mode="stretch_both")
    checkboxes2 = pn.widgets.ToggleGroup(options=["a", "b", "c"],)
    # slider = pn.widgets.IntSlider(name='Number of observations', value=500, start=0, end=2000)

    cb1 = pn.widgets.Checkbox(name='Show icons', value=True)
    cb2 = pn.widgets.Checkbox(name='select multiple', value=False)


    @pn.depends(cb1, watch=True)
    def uu2(val):
        print(val)
        ft.show_icons = val

    @pn.depends(cb2, watch=True)
    def uu1(val):
        print(val)
        ft.select_multiple = val


    # selections = pn.Column(ft, checkboxes, df_pane)
    selections = pn.Column(
        # df_pane,
        checkboxes,
        ft,
        checkboxes2,
        cb1,
        cb2
    )
    # pn.Row(selections)
    return selections
    #
    # ft = pn.widgets.FileTree(directory="/Users/madelinescyphers/Documents/school")
    # return pn.Column(ft).servable()


if __name__ == "__main__":
    pn.serve({"file_tree_lo": view}, port=5007, show=False)
