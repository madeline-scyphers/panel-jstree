# ✨ panel-jstree

panel-jstree is a wrapper python wrapper around the javascript library [jstree](https://www.jstree.com) for use in [panel](https://panel.holoviz.org/). This allows for JSON-like representations of tree data. One very useful implementation provided is a server-side file browser.

You can install and use the package as simple as.

```bash
conda install -c conda-forge panel-jstree
```

or with pip

```bash
pip install panel-jstree
```

Add this into a python file to play with the FileTree

```python
from panel_jstree import FileTree

FileTree().servable()
```

run it with `panel serve name_of_app.py`

It should run exploring the directory of the file.

![Project Intro](https://raw.githubusercontent.com/madeline-scyphers/panel-jstree/main/assets/videos/project-intro.gif)

## 🚀 Get started in under a minute

```bash
pip install  panel-jstree
```

Run the examples

```bash
panel serve tests/*tree.py --show
```

Here are some of the examples. You can see a small FileTree app with a text field and controls to directly input a file path, and turn off and on some of the controls.

![FileTree App Example](https://raw.githubusercontent.com/madeline-scyphers/panel-jstree/main/assets/videos/file-tree.gif)

You can make a simple tree where you swap out the data.

![Randomw Tree App Example](https://raw.githubusercontent.com/madeline-scyphers/panel-jstree/main/assets/videos/simple-tree.gif)

You can also see a generic Tree app with a custom callback to generate random nodes.

![Randomw Tree App Example](https://raw.githubusercontent.com/madeline-scyphers/panel-jstree/main/assets/videos/random-tree.gif)


## ⭐ Support

Please support [Panel](https://panel.holoviz.org) and
[panel-jstree](https://github.com/madeline-scyphers/panel-jstree) by giving the projects a star on Github.

Thanks

## ❤️ Contribute

If you are looking to contribute to this project you can find ideas in the [issue tracker](https://github.com/madeline-scyphers/panel-jstree/issues). To get started check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

I would love to support and receive your contributions. Thanks.

## Monitor

|                 |                                                                                                                                                                         |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Conda Install   | [![Conda Version](https://anaconda.org/conda-forge/panel-jstree/badges/version.svg)](https://anaconda.org/conda-forge/panel-jstree)                                     |
| PyPI Install    | [![PyPI version](https://badge.fury.io/py/panel-jstree.svg)](https://badge.fury.io/py/panel-jstree)                                                                     |
| Github release  | [![Github tag](https://img.shields.io/github/v/tag/madeline-scyphers/panel-jstree.svg?label=tag&colorB=11ccbb)](https://github.com/madeline-scyphers/panel-jstree/tags) |
| Python Versions | ![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)                                                                               |
| License         | [![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)                                                              |
