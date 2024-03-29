# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

Please note that this project is released with a [Contributor Code of Conduct](code-of-conduct.md).
By participating in this project you agree to abide by its terms.

## 🧳 Prerequisites

- A working [Python](https://www.python.org/downloads/) environment.
- git
- preferbly conda

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will need to create a new environment

Then run

```bash
git clone https://github.com/madeline-scyphers/panel-jstree.git
cd panel-jstree
conda create
conda activate panel-jstree
```


Please run this command and fix any failing tests if possible before you `git push`.

### 🚢 Release a new package on Pypi

Run all tests
```bash
pytest tests
```

Update the version in [__init__.py](src/panel_jstree/__init__.py).
And update the version in [package.json](src/panel_jstree/package.json) (example listed v1.0.0).

**and commit your changes**

```bash
git add src/panel_jstree/__init__.py src/panel_jstree/package.json
git commit -m "Version 1.0.0"
git push
```

Then tag a new version (example listed v1.0.0)

```bash
git tag -a v1.0.0 -m "Version 1.0.0 Release"
git push origin v1.0.0
```

This will release a new version to PyPI when pushed. 