# ✨ panel-jstree

panel-jstree is a wrapper python wrapper around the javascript library [jstree](https://www.jstree.com) for use in [panel](https://panel.holoviz.org/). This allows for JSON-like representations of tree data. One very useful implementation provided is a server-side file browser.

You can install and use the package as simple as.

```bash
pip install panel-jstree
```

```python
import panel as pn
from panel_jstree import FileTree

pn.Column(FileTree())
```

![Project Intro](https://github.com/madeline-scyphers/panel-jstree/blob/c0c182e09f028fe0fdb963d82ab2cdaad5128a1b/assets/videos/project-intro.gif)

## 🚀 Get started in under a minute

```bash
pip install  panel-jstree
```

Run the examples

```bash
panel serve examples/*.py --show
```

Here are some of the examples. You can see a small FileTree app with a text field and controls to directly input a file path, and turn off and on some of the controls.

![FileTree App Example](https://github.com/madeline-scyphers/panel-jstree/blob/777b299badf308746ff2ea0843755a12fe6158b4/assets/videos/file-tree.gif)

You can also see a generic Tree app with a custom callback to generate random nodes.

![Randomw Tree App Example](https://github.com/madeline-scyphers/panel-jstree/blob/777b299badf308746ff2ea0843755a12fe6158b4/assets/videos/random-tree.gif)


## ⭐ Support

Please support [Panel](https://panel.holoviz.org) and
[panel-jstree](https://github.com/madeline-scyphers/panel-jstree) by giving the projects a star on Github.

Thanks

## ❤️ Contribute

If you are looking to contribute to this project you can find ideas in the [issue tracker](https://github.com/madeline-scyphers/panel-jstree/issues). To get started check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

I would love to support and receive your contributions. Thanks.

## Monitor

[![PyPI version](https://badge.fury.io/py/panel-jstree.svg)](https://pypi.org/project/panel-jstree/)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)

