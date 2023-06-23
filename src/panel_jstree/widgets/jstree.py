"""
Defines various Select widgets which allow choosing one or more items
from a list of options.
"""
from __future__ import annotations

import copy
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, AnyStr, ClassVar, Optional, Type, Mapping

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

    _data = param.List(
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

    _get_children_cb = param.Callable(
        doc="Function that is called to load new children nodes. "
            "First argument should be the text representation of the parent,"
            "The second argument should be the unique id of the parent"  # TODO write this out more
    )

    _get_parents_cb = param.Callable(
        doc="Function that is called on a value to load all the parents"  # TODO write this out more
    )

    # Add a cb for getting parents (fileselector: map(str, Path(value).parents))

    _last_opened = param.Dict(doc="Last opened node data (JSON)")

    _new_nodes = param.List(doc="Children to push to tree")

    _flat_tree = param.List(doc="Flat representation of tree")

    _rename: ClassVar[Mapping[str, str | None]] = {
        "select_multiple": "multiple",
        "_get_children_cb": None,
        "_get_parents_cb": None,
    }

    _widget_type: ClassVar[Type[Model]] = jsTreePlot

    def __init__(self, **params):
        super().__init__(**params)
        if self._get_children_cb:
            self._get_children_cb = self._get_children_cb_wrapper(self._get_children_cb)
            self.param.watch(self.add_children_on_node_open, "_last_opened")
            if self._get_parents_cb:
                self.param.watch(self.add_children_on_new_values, "value", onlychanged=False)

    @property
    def flat_tree(self):
        return self._flat_tree

    @property  # TODO this is only need in File tree b/c it does special value processing
    def _values(self):
        return self.value

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

        properties["value"] = self._values
        return properties

    def add_children_on_new_values(self, *event):
        def transverse(d: list, value):
            parents = self._get_parents_cb(value)
            for node in d:
                if node["id"] == value:
                    break
                if node["id"] in parents:
                    node.setdefault("state", {})["opened"] = True
                    if node.get("children"):
                        transverse(node["children"], value)
                    else:
                        node["children"] = self._get_children_cb(
                            node["text"], node["id"], depth=2
                        )
                        for n in node["children"]:
                            if n["id"] in parents:
                                transverse([n], value)
                    break

        ids = [node["id"] for node in self._flat_tree]
        values = [value for value in self._values if value not in ids]
        if values:
            # data = copy.deepcopy(event.obj._data[:])
            data = copy.deepcopy(self._data[:])

            for value in values:
                transverse(data, value)
            self._data = data

    def add_children_on_node_open(self, event: param.parameterized.Event, **kwargs):  # rename to add grandchildren?
        new_nodes = []
        nodes_already_sent = event.new.get("children_d", [])
        # data = event.new["children"]
        children_nodes = event.new["children_nodes"]
        for node in children_nodes:
            children = self._get_children_cb(
                node["text"],
                node["id"],
                **{"children_to_skip": nodes_already_sent, **kwargs}
            )
            if children:
                new_nodes.extend(children)
        self._new_nodes = new_nodes

    @staticmethod
    def to_json(
            id_, label, parent: str = None, children: Optional[list] = None, icon: str = None, **kwargs
    ):
        jsn = dict(id=id_, text=label, **kwargs)
        if parent:
            jsn["parent"] = parent
        if children:
            jsn["children"] = children
        if icon:
            jsn["icon"] = icon
        # jsn["icon"] = "jstree-leaf"
        return jsn

    def _get_children_cb_wrapper(self, get_children_cb):
        def inner(text, id_, *args, **kwargs):
            jsn = get_children_cb(text, id_, *args, **kwargs)
            # TODO this doesn't work right now b/c of comparisons of value to id
            # if self._data:  # we already have a tree
            #     for node in jsn:





            #     if "id" not in node:
            #         node["id"] = uuid.uuid4().hex
            return jsn
        return inner


class Tree(_TreeBase):
    """"""
    def __init__(self, data, **params):
        if "get_children_cb" in params:
            params["_get_children_cb"] = params.pop("get_children_cb")
        super().__init__(_data=data, **params)

    @property
    def data(self):
        """When swapping out data, you are not able to input selections data on nodes.
        All nodes will start out deselected.
        """
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def get_children_cb(self):
        return self._get_children_cb

    @get_children_cb.setter
    def get_children_cb(self, value):
        self._get_children_cb = value


class FileTree(_TreeBase):
    """"""

    directory = param.String(
        default=str(Path.cwd()),
        doc="""
        The directory to explore.""",
    )

    @property
    def _values(self):
        # normpath removes any ending slashes that mess up jstree
        # expand user lets people use things like ~ for home
        values = [os.path.expanduser(os.path.normpath(p)) for p in self.value]

        # This lets people use paths relative to self.directory
        for i, value in enumerate(values):
            value = Path(value)
            if not value.is_absolute():
                values[i] = str(Path(self.directory).parent / value)

        return values

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

        super().__init__(_get_children_cb=self._get_children, _get_parents_cb=lambda value: list(map(str, Path(value).parents)), **params)
        self._data = [{"id": self.directory,
                       "text": Path(self.directory).name,
                       "icon": self._folder_icon,
                       "state": {"opened": True},
                       "children": self._get_children_cb(Path(self.directory).name, self.directory,  depth=1)
                       }]

    def _get_children(
        self, text: str, directory: str, depth=0, children_to_skip=(), **kwargs
    ):
        directory = str(directory)
        parent = directory
        jsn = []
        if not os.path.isdir(directory):
            return []
        dirs, files = self._get_paths(directory, children_to_skip=children_to_skip)
        for dir in dirs:
            if depth > 0:
                children = self._get_children(Path(dir).name, dir, depth=depth - 1)
            else:
                children = None
            jsn.append(
                self.to_json(
                    id_=dir, label=Path(dir).name, parent=parent, children=children, icon=self._folder_icon, **kwargs
                )
            )
        jsn.extend(
            self.to_json(id_=file, label=Path(file).name, parent=parent, icon=self._file_icon, **kwargs) for file in files
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

