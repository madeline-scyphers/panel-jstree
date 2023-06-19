import * as p from "@bokehjs/core/properties"
import { div } from "@bokehjs/core/dom"
import {HTMLBox, HTMLBoxView, set_size} from "./layout"


declare function jQuery(...args: any[]): any

function ID() {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
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
        this.connect(this.model.properties.data.change, () => this._update_tree_from_data())
        this.connect(this.model.properties.value.change, () => this._update_selection_from_value())
        this.connect(this.model.properties._new_nodes.change, () => this._update_tree_from_new_nodes())
        this.connect(this.model.properties.show_icons.change, () => this._setShowIcons())
        this.connect(this.model.properties.show_dots.change, () => this._setShowDots())
        this.connect(this.model.properties.multiple.change, () => this._setMultiple())
        console.log(this.model.show_dots)
        console.log(this.model.show_icons)
    }
    //
    render(): void {
        super.render()
        this._id = ID()
        console.log(this._id)
        this._container = div({id: this._id, style: "overflow: auto; minHeight: 200px; minWidth: 200px;"},)
        set_size(this._container, this.model)
        this.shadow_el.appendChild(this._container);
        console.log(this._container)

        let kw = {"checkbox": {
            "three_state": false,
            "cascade": "undetermined"}}

        this._jstree = jQuery(this._container).jstree(
            { "core":
                {"data": this.model.data, "check_callback": true,
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
        // Rendering callbacks
        // TODO: do I need both of these?
        this._jstree.on('refresh.jstree', ({}, {}) => this._update_selection_from_value());

        // Sync state with model
        this._jstree.on('changed.jstree', (e: any, data: any) => this._update_code_from_editor(e, data));
        this._jstree.on('before_open.jstree', (e: any, data: any) => this._listen_for_node_open(e, data));

    }

    _update_code_from_editor({}, data: any): void {
        this.model.value = data.instance.get_selected();
    }
    _update_selection_from_value(): void {
        console.log("last selected: ", this._last_selected)
        let deselected = this._last_selected.filter(x => !this.model.value.includes(x));
        console.log("values: ", this.model.value)
        this._jstree.jstree(true).select_node(this.model.value)
        console.log("deselected: ", deselected)
        this._jstree.jstree(true).deselect_node(deselected)
        this._last_selected = this.model.value
    }

    _update_tree_from_new_nodes(): void {
        console.log("new nodes: ", this.model._new_nodes)
        for (let node of this.model._new_nodes){
            this._jstree.jstree(true).create_node(node["parent"], node, "first")
        }
        this._jstree.jstree(true).settings.core.data = this._jstree.jstree(true).get_json(null, {no_li_attr: true, no_a_attr: true, no_data: true})
        this.model.data = this._jstree.jstree(true).settings.core.data
        // this._update_selection_from_value()
    }

    _update_tree_from_data(): void {
        console.log("updating data")
        this._jstree.jstree(true).settings.core.data = this.model.data;
        console.log("flat tree: ", this.model._flat_tree)
        this.model._flat_tree = this._jstree.jstree(true).get_json(null, {"flat": true})
    }


    _setShowIcons(): void {
        if (this.model.show_icons) {
            this._jstree.jstree(true).show_icons ( );
        }
        else {
            this._jstree.jstree(true).hide_icons ( );
        }
    }
    _setShowDots(): void {
        if (this.model.show_dots) {
            this._jstree.jstree(true).show_dots ( );
        }
        else {
            this._jstree.jstree(true).hide_dots ( );
        }
    }

    _setMultiple(): void {
        this._jstree.jstree(true).settings.core.multiple = this.model.multiple
    }

    _update_tree_theme_from_model(): void {
        this._jstree.jstree(true).refresh(false, true);
    }

    _listen_for_node_open({}, data: any): void {
        console.log("node opened")
        console.log("openeing node: ", data.node)
        this.model._last_opened = data.node
    }

}

export namespace jsTreePlot {
  export type Attrs = p.AttrsOf<Props>
  export type Props = HTMLBox.Props & {
    data: p.Property<any>
    plugins: p.Property<any>
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
        data:          [ Array(Any), []     ],
        plugins:       [ Array(Any), []     ],
        multiple:      [ Boolean, true ],
        show_icons:    [ Boolean, true ],
        show_dots:     [ Boolean, true ],
        _last_opened: [ Any, {} ],
        _new_nodes: [ Any, {} ],
        _flat_tree: [ Array(Any), []     ],
      }))
    }
}
