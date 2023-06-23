import panel as pn
import shutil
import itertools
from pathlib import Path
from contextlib import contextmanager

from panel_jstree import FileTree


pn.extension("tree", sizing_mode="stretch_width")

FT_TEST_DIR = Path(__file__).parent / "test_dir"


@contextmanager
def ft_test_dir():
    # make a bunch of dummy directories inside the test directory
    seq = "abcde"
    for tup in itertools.product(seq, repeat=len(seq)):
        (FT_TEST_DIR / "/".join(char for char in tup)).mkdir(parents=True, exist_ok=True)
    yield FT_TEST_DIR
    shutil.rmtree(FT_TEST_DIR, ignore_errors=True)


def test_filetree_can_construct():
    FileTree()


def test_flat_tree_app(test_dir="."):
    """Construct a FileTree for manual testing"""
    ft = FileTree(test_dir)

    settings = pn.Param(
        ft,
        parameters=[
            "select_multiple",
            "show_icons",
            "show_dots",
            "checkbox",
        ]
    )
    text_input = pn.widgets.TextInput(name="Text Input", placeholder="Enter a file path here...")

    @pn.depends(text_input, watch=True)
    def text_box_cb(val):
        ft.value = [val]

    return pn.template.FastListTemplate(
        site="Panel jsTree",
        title="FileTree Editor",
        main=[ft, text_input],
        sidebar=[settings],
    )


if __name__.startswith("bokeh"):
    test_flat_tree_app().servable()

if __name__ == "__main__":
    with ft_test_dir() as test_dir:
        pn.serve({Path(__file__).name: test_flat_tree_app(test_dir)}, port=5007, show=False)
