"""
Defines custom jsTree bokeh model to render Ace editor.
"""
from __future__ import absolute_import, division, unicode_literals

import pathlib

from bokeh.core.properties import JSON, Any, Bool, Dict, Enum, List, Override, String
from bokeh.models.layouts import LayoutDOM

# from .layout import HTMLBox
from bokeh.util.compiler import TypeScript
from panel import extension
from panel.io.resources import JS_URLS, bundled_files
from panel.util import classproperty

# pylint: disable=protected-access

extension._imports["tree"] = "panel_jstree.bokeh_extensions.jstree"
# pylint: enable=protected-access


class HTMLBox(LayoutDOM):
    """ """


class jsTreePlot(HTMLBox):
    """
    A Bokeh model that wraps around a jsTree editor and renders it inside
    a Bokeh plot.
    """

    __css__ = ["https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css"]

    __javascript__ = [
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js",
    ]

    plugins = List(Any)
    checkbox = Bool(default=True)
    multiple = Bool(default=True)
    show_icons = Bool(default=True)
    show_dots = Bool(default=True)
    _last_opened = Dict(String, Any)
    _new_nodes = List(Any)
    _flat_tree = List(Any)

    # Callback properties
    value = List(Any)
    _data = List(Any)

    checkbox = Bool()
    directory = String()
