"""
Defines custom jsTree bokeh model to render Ace editor.
"""
from __future__ import absolute_import, division, unicode_literals

from bokeh.core.properties import String, Any, List, Bool
from panel.models.layout import HTMLBox


from panel import extension
# pylint: disable=protected-access
extension._imports["tree"] = "panel_jstree.bokeh_extensions.jstree"
# pylint: enable=protected-access


class jsTreePlot(HTMLBox):
    """
    A Bokeh model that wraps around a jsTree editor and renders it inside
    a Bokeh plot.
    """

    __css__ = [
        'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css'
    ]

    __javascript__ = [
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js'
    ]

    plugins = List(Any)
    multiple = Bool(default=True)
    show_icons = Bool(default=True)
    show_dots = Bool(default=True)
    url = String()
    _last_opened = Any()
    _new_nodes = Any()
    _flat_tree = List(Any)

    # Callback properties
    value = List(Any)
    data = List(Any)

    checkbox = Bool()
    directory = String()

