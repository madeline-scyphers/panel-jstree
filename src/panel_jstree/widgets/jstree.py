"""
Defines various Select widgets which allow choosing one or more items
from a list of options.
"""
from __future__ import annotations

import copy
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, AnyStr, ClassVar, Optional, Type

import param
from panel.util import fullpath
from panel.widgets.base import Widget
from panel.widgets.file_selector import _scan_path

from ..bokeh_extensions.jstree import jsTreePlot

if TYPE_CHECKING:
    from bokeh.model import Model

logger = logging.getLogger(__file__)


class _TreeBase(Widget):
    """
    jsTree widget allow editing a tree in an jsTree editor.
    """

    value = param.List(default=[], doc="List of currently selected leaves and nodes")

    data = param.List(
        default=[],
        doc="Hierarchical tree structure of data. See "
        " `jsTree <https://www.jstree.com>`_ for more"
        " details on formatting",
    )

    select_multiple = param.Boolean(
        default=True, doc="Whether multiple nodes can be selected or not"
    )

    show_icons = param.Boolean(default=True, doc="Whether to use icons or not")

    show_dots = param.Boolean(
        default=True, doc="Whether to show dots on the left as part of the tree"
    )

    checkbox = param.Boolean(default=True, doc="Whether to to use checkboxes as selectables")

    plugins = param.List(
        doc="Configure which additional plugins will be active. "
        "Should be an array of strings, where each element is a plugin name that are passed"
        "to jsTree."
    )

    _last_opened = param.Dict(doc="last opened node")

    _new_nodes = param.List(doc="Children to push to tree")

    _flat_tree = param.List(doc="Flat representation of tree")

    _rename = {"select_multiple": "multiple"}

    _widget_type: ClassVar[Type[Model]] = jsTreePlot

    @property
    def flat_tree(self):
        return self._flat_tree

    @property
    def _values(self):
        return [os.path.normpath(p) for p in self.value]

    def _process_param_change(self, msg: dict[str, Any]) -> dict[str, Any]:
        """
        Transform parameter changes into bokeh model property updates.
        Should be overridden to provide appropriate mapping between
        parameter value and bokeh model change. By default uses the
        _rename class level attribute to map between parameter and
        property names.
        """
        properties = super()._process_param_change(msg)

        properties.pop("title", None)
        if not properties.get("height") and (
            self.sizing_mode is None or "width" in self.sizing_mode
        ):
            properties["height"] = 400
        if properties.get("height") and properties["height"] < 100:
            properties["height"] = 100

        if properties.pop("checkbox", None):
            properties.get("plugins", []).append("checkbox")

        properties["value"] = self._values
        return properties


class FileTree(_TreeBase):
    """"""

    directory = param.String(
        default=str(Path.cwd()),
        doc="""
        The directory to explore.""",
    )

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
        return msg

    def __init__(self, directory: AnyStr | os.PathLike | None = None, **params):
        if directory is not None:
            params["directory"] = fullpath(directory)
        self._file_icon = "jstree-file"
        self._folder_icon = "jstree-folder"
        super().__init__(**params)
        self.data = self._get_child_json(self.directory, depth=1)
        self.param.watch(self._add_node_children, "_last_opened")
        self.param.watch(self._new_nodes_on_value_update, "value")

    def _new_nodes_on_value_update(self, event):
        def transverse(d: list, value):
            parents = Path(value).parents
            for node in d:
                if Path(node["id"]) == Path(value):
                    break
                if Path(node["id"]) in parents:
                    node.setdefault("state", {})["opened"] = True
                    if node.get("children"):
                        transverse(node["children"], value)
                    else:
                        node["children"] = self._get_child_json(
                            node["id"], add_parent=True, state={"opened": True}, depth=2
                        )
                        [
                            transverse([n], value)
                            for n in node["children"]
                            if Path(n["id"]) in parents
                        ]
                    break

        ids = [node["id"] for node in self._flat_tree]
        values = [value for value in self._values if value not in ids]
        if values:
            data = copy.deepcopy(event.obj.data[:])

            for value in values:
                transverse(data, value)
            self.data = data

    def _add_node_children(self, event: param.parameterized.Event = None, dirs=None, **kwargs):
        new_nodes = []
        kw = {}
        if not dirs:
            if event:
                nodes_already_sent = event.new.get("children_d", [])
                dirs = event.new["children"]
                kw = dict(
                    add_parent=True,
                    children_to_skip=nodes_already_sent,
                )
            else:
                dirs = [self.directory]
                kw = dict(depth=1)
        for dir_ in dirs:
            children = self._get_child_json(dir_, **{**kwargs, **kw})
            if children:
                new_nodes.extend(children)
        self._new_nodes = new_nodes

    def _get_child_json(
        self, directory: str, add_parent=False, depth=0, children_to_skip=(), **kwargs
    ):
        directory = str(directory)
        parent = directory if add_parent else None
        jsn = []
        if not os.path.isdir(directory):
            return []
        dirs, files = self._get_paths(directory, children_to_skip=children_to_skip)
        for dir in dirs:
            if depth > 0:
                children = self._get_child_json(dir, add_parent=add_parent, depth=depth - 1)
            else:
                children = None
            jsn.append(
                self._get_json(
                    dir, parent=parent, children=children, icon=self._folder_icon, **kwargs
                )
            )
        jsn.extend(
            self._get_json(file, parent=parent, icon=self._file_icon, **kwargs) for file in files
        )
        return jsn

    @staticmethod
    def _get_paths(directory, children_to_skip=()):
        dirs_, files = _scan_path(directory, file_pattern="[!.]*")
        dirs = []
        for d in dirs_:
            if not Path(d).name.startswith(".") and d not in children_to_skip:
                try:
                    if os.listdir(d):
                        dirs.append(d)
                except OSError as e:
                    print(repr(e), d)

        # dirs = [d for d in dirs if not Path(d).name.startswith(".") and d not in children_to_skip]
        files = [f for f in files if f not in children_to_skip]
        return dirs, files

    def _get_json(
        self, txt, parent: str = None, children: Optional[list] = None, icon: str = None, **kwargs
    ):
        jsn = dict(id=txt, text=Path(txt).name, **kwargs)
        if parent:
            jsn["parent"] = parent
        if children:
            jsn["children"] = children
        if icon:
            jsn["icon"] = icon
        return jsn
