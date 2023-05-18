"""
Having problems getting this to render in panel>1/bokeh>3
but this works fine in panel<1/bokeh<3 (as long as you change the
HTMLBox and HTMLBoxView import from bokeh in panel<1 to from layout.ts in panel>1
in the jstree.ts file.
In panel>1 you can still get jstree to work by running the jQuery below on
a different div id. I don't know if in bokeh>3 it is putting things in
shadow elements and that is interfering with jstree, or something else.

Once the app is running, you can recreate what this does in the developer
console in your browser by entering (replace id-of-div with the id of your div):
jQuery('#`id-of-div`').jstree({ 'core' : {
        'data' : [
           'Simple root node',
           {
             'text' : 'Root node 2',
             'state' : {
               'opened' : true,
               'selected' : true
             },
             'children' : [
               { 'text' : 'Child 1' },
               'Child 2'
             ]
          }
        ]
    } });
"""
import panel as pn
from panel_jstree.widgets.jstree import jsTree

pn.extension("tree")


def show_tree():
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
    return pn.Column(tree)


if __name__ == "__main__":
    pn.serve({"file_tree": show_tree}, port=5006)
