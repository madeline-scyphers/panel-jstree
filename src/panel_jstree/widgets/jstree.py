# """
# Defines various Select widgets which allow choosing one or more items
# from a list of options.
# """
# from __future__ import absolute_import, division, unicode_literals, annotations
#
# import copy
# import os
# from abc import abstractmethod
#
# from typing import (
#     AnyStr, TYPE_CHECKING, ClassVar, Type, Any, Optional
# )
# import numpy as np
# from pathlib import Path
#
# import param
# from panel.models import Location
#
# #from ..models.enums import ace_themes
# from panel.widgets.base import Widget
# from panel.viewable import Layoutable
# from panel.io.state import state
# from panel.io import PeriodicCallback
# from panel.util import fullpath
# from panel.widgets.file_selector import _scan_path
# from ..bokeh_extensions.jstree import jsTreePlot
# from panel.io.server import serve
# if TYPE_CHECKING:
#     from bokeh.model import Model
#
#
#
# class _jsTreeBase(Widget):
#     """
#     jsTree widget allow editing a tree in an jsTree editor.
#     """
#
#     value = param.List(default=[], doc="List of currently selected leaves and nodes")
#
#     data = param.List(default=[], doc="Hierarchical tree structure of data. See "
#                                       " `jsTree <https://www.jstree.com>`_ for more"
#                                       " details on formatting")
#
#     select_multiple = param.Boolean(default=True, doc="Whether multiple nodes can be selected or not")
#
#     show_icons = param.Boolean(default=True, doc="""
#         Whether to use icons or not""")
#
#     show_dots = param.Boolean(default=True, doc="Whether to show dots on the left as part of the tree")
#
#     checkbox = param.Boolean(default=True, doc="Whether to to use checkboxes as selectables")
#
#     select_only_leaves = param.Boolean(default=False, doc="")  # TODO fill this in
#
#     plugins = param.List(doc="Selected callback data")
#
#     url = param.String(doc="ajax url")  # TODO figure out how to just get the url
#
#     _last_opened = param.Dict(doc="last opened node")
#
#     _new_nodes = param.List(doc="Children to push to tree")
#
#     _rename = {"select_multiple": "multiple"}
#
#     _widget_type: ClassVar[Type[Model]] = jsTreePlot
#
#     # def _get_model(self, doc, root=None, parent=None, comm=None):
#     #     if self._widget_type is not None:
#     #         pass
#     #     elif "panel.models.jstree" not in sys.modules:
#     #         if isinstance(comm, JupyterComm):
#     #             self.param.warning(
#     #                 "jsTreePlot was not imported on instantiation "
#     #                 "and may not render in a notebook. Restart "
#     #                 "the notebook kernel and ensure you load "
#     #                 "it as part of the extension using:"
#     #                 "\n\npn.extension('jstree')\n"
#     #             )
#     #         from ..models.jstree import jsTreePlot
#     #
#     #     else:
#     #         jsTreePlot = getattr(sys.modules["panel.models.jstree"], "jsTreePlot")
#     #
#     def _process_param_change(self, msg: dict[str, Any]) -> dict[str, Any]:
#         """
#         Transform parameter changes into bokeh model property updates.
#         Should be overridden to provide appropriate mapping between
#         parameter value and bokeh model change. By default uses the
#         _rename class level attribute to map between parameter and
#         property names.
#         """
#         properties = super()._process_param_change(msg)
#         if not properties.get("height") and (self.sizing_mode is None or "width" in self.sizing_mode):
#             properties["height"] = 400
#         if properties.get("height") and properties["height"] < 100:
#             properties["height"] = 100
#             properties['min_height'] = 100
#
#         checkbox = properties.pop("checkbox", None)
#         if checkbox:
#             properties.get("plugins", []).append("checkbox")
#         return properties
#
#     def add_node_children(self, event: param.parameterized.Event = None):
#         """TODO write this"""
#         new_nodes = []
#
#         if event:
#             dirs = event.new["children"]
#             nodes_already_sent = event.new.get("children_d", [])
#             kw = dict(add_parent=True, children_to_skip=nodes_already_sent)
#         else:
#             dirs = [self.directory]
#             kw = dict(depth=1)
#         for dir_ in dirs:
#             children = self._get_child_json(dir_, **kw)
#             if children:
#                 new_nodes.extend(children)
#         self._new_nodes = new_nodes
#         return new_nodes
#
#     @staticmethod
#     @abstractmethod
#     def get_child_nodes(directory, children_to_skip=()):
#         """TODO write this"""
#
#     def _get_child_json(self, base: str, add_parent=False, depth=0, children_to_skip=()):
#         parent = base if add_parent else None
#         jsn = []
#         nodes, leaves = self.get_child_nodes(base, children_to_skip=children_to_skip)
#         for leaf in nodes:
#             if depth > 0:
#                 children = self._get_child_json(leaf, add_parent=add_parent, depth=depth - 1)
#             else:
#                 children = None
#             jsn.append(self._format_json(leaf, parent=parent, children=children, icon=self._node_icon))
#         jsn.extend(self._format_json(file, parent=parent, icon=self._leaf_icon) for file in leaves)
#         return jsn
#
#     # todo, this can be made to be used as the generic version for the base one,
#     # but if needs to be unique or it has to have a flallback
#     def _format_json(self, txt, parent: str = None, children: Optional[list] = None, icon: str = None):
#         jsn = dict(id=txt, text=Path(txt).name)
#         if parent:
#             jsn["parent"] = parent
#         if children:
#             jsn["children"] = children
#         if icon:
#             jsn["icon"] = icon
#         return jsn
#
# class jsTree(_jsTreeBase):
#     """
#     jsTree widget allow editing a tree in an jsTree editor.
#     """
#
#
# class FileTree(_jsTreeBase):
#     """"""
#     directory = param.String(default=str(Path.cwd()), doc="""
#         The directory to explore.""")
#
#     def _process_param_change(self, msg: dict[str, Any]) -> dict[str, Any]:
#         """
#         Transform parameter changes into bokeh model property updates.
#         Should be overridden to provide appropriate mapping between
#         parameter value and bokeh model change. By default uses the
#         _rename class level attribute to map between parameter and
#         property names.
#         """
#         msg = super()._process_param_change(msg)
#         msg.pop("directory", None)
#         msg.pop("title", None)
#         return msg
#
#     def __init__(self, directory: AnyStr | os.PathLike | None = None, **params):
#         if directory is not None:
#             params['directory'] = fullpath(directory)
#         self._leaf_icon = "jstree-file"
#         self._node_icon = "jstree-folder"
#         super().__init__(**params)
#         self.data = self.add_node_children()
#         self.param.watch(self.add_node_children, "_last_opened")
#         self.param.watch(self._print_value, "value")
#
#     @property
#     def base(self):
#         return self.directory
#
#     def _print_value(self, *events):
#         print(self.value)
#
#
#     @staticmethod
#     def get_child_nodes(directory, children_to_skip=()):
#         dirs, files = _scan_path(directory, file_pattern='[!.]*')
#         dirs = [d for d in dirs if not Path(d).name.startswith(".") and d not in children_to_skip]
#         files = [f for f in files if f not in children_to_skip]
#         return dirs, files
#
#
#




"""
Defines various Select widgets which allow choosing one or more items
from a list of options.
"""
from __future__ import absolute_import, division, unicode_literals, annotations

import copy
import os
from abc import abstractmethod

from typing import (
    AnyStr, TYPE_CHECKING, ClassVar, Type, Any, Optional
)
import numpy as np
from pathlib import Path

import param
from panel.models import Location

#from ..models.enums import ace_themes
from panel.widgets.base import Widget
from panel.viewable import Layoutable
from panel.io.state import state
from panel.io import PeriodicCallback
from panel.util import fullpath
from panel.widgets.file_selector import _scan_path
from ..bokeh_extensions.jstree import jsTreePlot
from panel.io.server import serve
if TYPE_CHECKING:
    from bokeh.model import Model



class _jsTreeBase(Widget):
    """
    jsTree widget allow editing a tree in an jsTree editor.
    """

    value = param.List(default=[], doc="List of currently selected leaves and nodes")

    data = param.List(default=[], doc="Hierarchical tree structure of data. See "
                                      " `jsTree <https://www.jstree.com>`_ for more"
                                      " details on formatting")

    select_multiple = param.Boolean(default=True, doc="Whether multiple nodes can be selected or not")

    show_icons = param.Boolean(default=True, doc="""
        Whether to use icons or not""")

    show_dots = param.Boolean(default=True, doc="Whether to show dots on the left as part of the tree")

    checkbox = param.Boolean(default=True, doc="Whether to to use checkboxes as selectables")

    select_only_leaves = param.Boolean(default=False, doc="")  # TODO fill this in

    plugins = param.List(doc="Selected callback data")

    url = param.String(doc="ajax url")  # TODO figure out how to just get the url

    _last_opened = param.Dict(doc="last opened node")

    _new_nodes = param.List(doc="Children to push to tree")

    _rename = {"select_multiple": "multiple"}

    _widget_type: ClassVar[Type[Model]] = jsTreePlot

    # def _get_model(self, doc, root=None, parent=None, comm=None):
    #     if self._widget_type is not None:
    #         pass
    #     elif "panel.models.jstree" not in sys.modules:
    #         if isinstance(comm, JupyterComm):
    #             self.param.warning(
    #                 "jsTreePlot was not imported on instantiation "
    #                 "and may not render in a notebook. Restart "
    #                 "the notebook kernel and ensure you load "
    #                 "it as part of the extension using:"
    #                 "\n\npn.extension('jstree')\n"
    #             )
    #         from ..models.jstree import jsTreePlot
    #
    #     else:
    #         jsTreePlot = getattr(sys.modules["panel.models.jstree"], "jsTreePlot")
    #
    def __init__(self, **params):
        self._ids = {}
        super().__init__(**params)

    def _process_param_change(self, msg: dict[str, Any]) -> dict[str, Any]:
        """
        Transform parameter changes into bokeh model property updates.
        Should be overridden to provide appropriate mapping between
        parameter value and bokeh model change. By default uses the
        _rename class level attribute to map between parameter and
        property names.
        """
        properties = super()._process_param_change(msg)
        if not properties.get("height") and (self.sizing_mode is None or "width" in self.sizing_mode):
            properties["height"] = 400
        if properties.get("height") and properties["height"] < 100:
            properties["height"] = 100
            properties['min_height'] = 100

        checkbox = properties.pop("checkbox", None)
        if checkbox:
            properties.get("plugins", []).append("checkbox")
        return properties

    def add_node_children(self, event: param.parameterized.Event = None):
        """TODO write this"""
        new_nodes = []

        if event:
            dir_ids = event.new["children"]
            nodes_already_sent_ids = event.new.get("children_d", [])
            dirs = [self._ids[id_] for id_ in dir_ids]
            nodes_already_sent = [self._ids[id_] for id_ in nodes_already_sent_ids]
            kw = dict(add_parent=True, children_to_skip=nodes_already_sent, )
        else:
            dirs = [self.directory]
            dir_ids = ["#"]  # means parent
            kw = dict(depth=1)
        for dir_, id_ in zip(dirs, dir_ids):
            children = self._get_child_json(dir_, id_=id_, **kw)
            if children:
                new_nodes.extend(children)
        self._new_nodes = new_nodes
        return new_nodes

    @staticmethod
    @abstractmethod
    def get_child_nodes(directory, children_to_skip=()):
        """TODO write this"""

    def _get_child_json(self, base: str, add_parent=False, depth=0, children_to_skip=(), id_: str = None):
        parent = id_ or base if add_parent else None
        jsn = []
        nodes, leaves = self.get_child_nodes(base, children_to_skip=children_to_skip)
        for leaf in nodes:
            if depth > 0:
                children = self._get_child_json(leaf, add_parent=add_parent, depth=depth - 1)
            else:
                children = None
            jsn.append(self._format_json(leaf, parent=parent, children=children, icon=self._node_icon))
        jsn.extend(self._format_json(file, parent=parent, icon=self._leaf_icon) for file in leaves)
        return jsn

    # todo, this can be made to be used as the generic version for the base one,
    # but if needs to be unique or it has to have a flallback
    def _format_json(self, txt, parent: str = None, children: Optional[list] = None, icon: str = None):
        id = str(np.random.randint(0, 100000000))
        text = Path(txt).name
        self._ids[id] = txt
        jsn = dict(id=id, text=text)
        if parent:
            jsn["parent"] = parent
        if children:
            jsn["children"] = children
        if icon:
            jsn["icon"] = icon
        return jsn

class jsTree(_jsTreeBase):
    """
    jsTree widget allow editing a tree in an jsTree editor.
    """


class FileTree(_jsTreeBase):
    """"""
    directory = param.String(default=str(Path.cwd()), doc="""
        The directory to explore.""")

    def _process_param_change(self, msg: dict[str, Any]) -> dict[str, Any]:
        """
        Transform parameter changes into bokeh model property updates.
        Should be overridden to provide appropriate mapping between
        parameter value and bokeh model change. By default uses the
        _rename class level attribute to map between parameter and
        property names.
        """
        msg = super()._process_param_change(msg)
        msg.pop("directory", None)
        msg.pop("title", None)
        return msg

    def __init__(self, directory: AnyStr | os.PathLike | None = None, **params):
        if directory is not None:
            params['directory'] = fullpath(directory)
        self._leaf_icon = "jstree-file"
        self._node_icon = "jstree-folder"
        super().__init__(**params)
        self.data = self.add_node_children()
        self.param.watch(self.add_node_children, "_last_opened")
        self.param.watch(self._print_value, "value")

    @property
    def base(self):
        return self.directory

    def _print_value(self, *events):
        print(self.value)


    @staticmethod
    def get_child_nodes(directory, children_to_skip=()):
        dirs, files = _scan_path(directory, file_pattern='[!.]*')
        dirs = [d for d in dirs if not Path(d).name.startswith(".") and d not in children_to_skip]
        files = [f for f in files if f not in children_to_skip]
        return dirs, files