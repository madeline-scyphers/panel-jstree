from pathlib import Path

import panel as pn

from panel_jstree import Tree

pn.extension("tree", sizing_mode="stretch_width")

data = [
    {
        'text': 'Root node 2',
        'children': [
            {'text': 'Child 1',
             'children': [
                 {'text': 'Child 1.1',
                  "children": [
                      {"text": "Child 1.1.1",
                       "children": [
                           {"text": "Child 1.1.1.1",
                            "children": [
                                {"text": "Child 1.1.1.1.1",
                                 "children": [
                                     {"text": "Child 1.1.1.1.1.1"},
                                 ],
                                 'state': {'opened': True},

                                 },
                            ],
                            'state': {'opened': True},
                            },
                       ],
                       'state': {'opened': True},
                       },
                  ],
                  'state': {'opened': True},

                  },
             ],
             'state': {'opened': True},
             }
        ],
        'state': {'opened': True},
    }
]


def test_base_tree_app():
    """Construct a BaseTree for manual testing"""
    tree = Tree(
        data=data,
        sizing_mode="stretch_both",
        cascade=False
    )

    settings = pn.Param(
        tree,
        parameters=[
            "select_multiple",
            "show_icons",
            "show_dots",
            "checkbox",
        ]
    )

    return pn.template.FastListTemplate(
        site="Taxonomy jsTree",
        title="Taxonomy Tree",
        main=[pn.Column(tree)],
        sidebar=[settings],
    )


if __name__.startswith("bokeh"):
    test_base_tree_app().servable()

if __name__ == "__main__":
    pn.serve({Path(__file__).name: test_base_tree_app()}, port=5012, show=False)
