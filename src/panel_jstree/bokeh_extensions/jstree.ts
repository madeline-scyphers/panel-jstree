import * as p from "@bokehjs/core/properties"
import { div } from "@bokehjs/core/dom"
import {HTMLBox, HTMLBoxView, set_size} from "./layout"

type Node = {
  [key: string]: any;
};

declare function jQuery(...args: any[]): any

function ID() {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substring(2, 11);
}

export class jsTreePlotView extends HTMLBoxView {
    model: jsTreePlot
    protected _container: HTMLDivElement
    protected _id: any
    protected _jstree: any
    protected _last_selected: string[]

    initialize(): void {
      super.initialize()
        this._last_selected = []
    }

    connect_signals(): void {
        console.log("connect")
        super.connect_signals()
        this.connect(this.model.properties._data.change, () => this._update_tree_from_data())
        this.connect(this.model.properties.value.change, () => this._update_selection_from_value())
        this.connect(this.model.properties._new_nodes.change, () => this._update_tree_from_new_nodes())
        this.connect(this.model.properties.checkbox.change, () => this.setCheckboxes())
        this.connect(this.model.properties.show_icons.change, () => this._setShowIcons())
        this.connect(this.model.properties.show_dots.change, () => this._setShowDots())
        this.connect(this.model.properties.multiple.change, () => this._setMultiple())
        console.log(this.model.show_dots)
        console.log(this.model.show_icons)
    }

    render(): void {
        super.render()
        this._id = ID()
        console.log(this._id)
        this._container = div({id: this._id, style: "overflow: auto; minHeight: 200px; minWidth: 200px;"},)
        set_size(this._container, this.model)
        this.shadow_el.appendChild(this._container);
        console.log(this._container)

        if (this.model.checkbox) {
            this.model.plugins.push("checkbox")
        }

        let kw = {"checkbox": {
            "three_state": false,
            "cascade": "undetermined"
        }}

        this._jstree = jQuery(this._container).jstree(
            { "core":
                {"data": this.model._data, "check_callback": true,
                 "multiple": this.model.multiple,
                 "themes": {
                    "dots": this.model.show_dots,
                    "icons": this.model.show_icons
                  }
                },
                "plugins": this.model.plugins,
                ...kw
            }
            );
        this.init_callbacks()
    }
    init_callbacks(): void {
        // Initialization

        // Rendering callbacks
        // TODO: do I need both of these?
        this._jstree.on('refresh.jstree', ({}, {}) => this._update_selection_from_value());

        // Sync state with model
        this._jstree.on('model.jstree', ({}, {}) => this.onNewData());
        this._jstree.on('activate_node.jstree', ({}, data: any) => this.selectNodeFromEditor({}, data));
        this._jstree.on('before_open.jstree', (e: any, data: any) => this._listen_for_node_open(e, data));

    }

    onNewData(): void {
        this.model._flat_tree = this._jstree.jstree(true).get_json(null, {"flat": true})
        console.log("flat tree: ", this.model._flat_tree)
    }

    selectNodeFromEditor({}, data: any): void {
        console.log("select pre", this.model.value)
        this.model.value = data.instance.get_selected();
        console.log("select post", this.model.value)
    }

    _update_selection_from_value(): void {
        console.log("update selection from value")
        this._jstree.jstree(true).select_node(this.model.value)
        // We sometimes have to fire this function more than once per value change because of
        // calling jstree.refresh, so we check to see if model.value has really changed
        // by comparing to last_selected
        if (this.model.value != this._last_selected) {
            let deselected = this._last_selected.filter(x => !this.model.value.includes(x));
            this._jstree.jstree(true).deselect_node(deselected)
        }
        // We choose get_selected
        this._last_selected = this.model.value;

    }

    _update_tree_from_new_nodes(): void {
        console.log("new nodes: ", this.model._new_nodes)
        for (let node of this.model._new_nodes){
            this._jstree.jstree(true).create_node(node["parent"], node, "first")
        }
        this._jstree.jstree(true).settings.core.data = this._jstree.jstree(true).get_json(null, {no_li_attr: true, no_a_attr: true, no_data: true})
        this.model._data = this._jstree.jstree(true).settings.core.data
        // this._update_selection_from_value()
    }

    _update_tree_from_data(): void {
        console.log("updating data")
        this._jstree.jstree(true).settings.core.data = this.model._data;
        console.log("data: ", this._jstree.jstree(true).settings.core.data)
        console.log("value after data", this.model.value)
        // This will redraw the tree if we swap out the data with new data
        // we set forget_state to true, so the current state is not reapplied
        // letting whatever state is set in the new data (open or closed, etc)
        // be the new state
        this._jstree.jstree(true).refresh(
            {"skip_loading": false,
            "forget_state": true});

        // selected state is not preserved correctly right now, so we then
        // deselect everything because that is better than getting it wrong
        this._jstree.jstree(true).deselect_all({"supress_event": true})

        console.log("value after refresh", this.model.value)
        console.log("data after refresh", this._jstree.jstree(true).settings.core.data)
    }

    _setShowIcons(): void {
        console.log("setShowIcons")
        if (this.model.show_icons) {
            this._jstree.jstree(true).show_icons ( );
        }
        else {
            this._jstree.jstree(true).hide_icons ( );
        }
    }
    _setShowDots(): void {
        console.log("setShowDots")
        if (this.model.show_dots) {
            this._jstree.jstree(true).show_dots ( );
        }
        else {
            this._jstree.jstree(true).hide_dots ( );
        }
    }

    setCheckboxes(): void {
        console.log("setCheckBoxes")
        if (this.model.checkbox) {
            this._jstree.jstree(true).show_checkboxes();
        }
        else {
            this._jstree.jstree(true).hide_checkboxes();
        }
    }

    _setMultiple(): void {
        console.log("setMultiple")
        this._jstree.jstree(true).settings.core.multiple = this.model.multiple
    }

    _update_tree_theme_from_model(): void {  // TODO can we remove this?
        this._jstree.jstree(true).refresh(false, true);
    }

    _listen_for_node_open({}, data: any): void {
        console.log("listen for node open")
        data.node = this.add_node_children(data.node)
        this.model._last_opened = data.node
    }

    add_node_children(node: Node): Node {
        console.log("add node children")
        node["children_nodes"] = [];
        for (let child of node.children){
            node.children_nodes.push(this._jstree.jstree(true).get_node(child))
        }
        return node
    }

}

export namespace jsTreePlot {
  export type Attrs = p.AttrsOf<Props>
  export type Props = HTMLBox.Props & {
    _data: p.Property<any>
    plugins: p.Property<any>
    checkbox: p.Property<boolean>
    multiple: p.Property<boolean>
    show_icons: p.Property<boolean>
    show_dots: p.Property<boolean>
    value: p.Property<any>
    _last_opened: p.Property<any>
    _new_nodes: p.Property<any>
    _flat_tree: p.Property<any>
  }
}

export interface jsTreePlot extends jsTreePlot.Attrs {}

export class jsTreePlot extends HTMLBox {
    properties: jsTreePlot.Props

    constructor(attrs?: Partial<jsTreePlot.Attrs>) {
        super(attrs)
    }

    static __module__ = "panel_jstree.bokeh_extensions.jstree"

    static {
      this.prototype.default_view = jsTreePlotView

      this.define<jsTreePlot.Props>(({Array, Any, Boolean}) => ({
        value:          [ Array(Any), []     ],
        _data:          [ Array(Any), []     ],
        plugins:       [ Array(Any), []     ],
        checkbox:      [ Boolean, true ],
        multiple:      [ Boolean, true ],
        show_icons:    [ Boolean, true ],
        show_dots:     [ Boolean, true ],
        _last_opened: [ Any, {} ],
        _new_nodes: [ Array(Any), [] ],
        _flat_tree: [ Array(Any), []     ],
      }))
    }
}
