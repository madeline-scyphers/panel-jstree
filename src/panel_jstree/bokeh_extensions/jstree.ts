import * as p from "@bokehjs/core/properties"
import { div } from "@bokehjs/core/dom"
import {HTMLBox, HTMLBoxView} from "./layout"


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
    protected _editor: any
    protected _jstree: any

    // initialize(): void {
    //   super.initialize()
    //   this._id = ID()
    //   console.log(this._id)
    //
    //   this._container = div({
    //     id: this._id
    //   })
    // }

    connect_signals(): void {
        super.connect_signals()
        this.connect(this.model.properties.data.change, () => this._update_tree_from_data())
        this.connect(this.model.properties.value.change, () => this._update_selection_from_value())
        this.connect(this.model.properties._new_nodes.change, () => this._update_tree_from_new_nodes())
        this.connect(this.model.properties.show_icons.change, () => this._update_tree_theme_from_model())
        this.connect(this.model.properties.show_dots.change, () => this._update_tree_theme_from_model())
        console.log(this.model.show_dots)
        console.log(this.model.show_icons)
    }
    //
    render(): void {
        super.render()

        this._id = ID()
        console.log(this._id)

        // this._container = div({id: this._id})
        this._container = div({id: this._id, })
        // applyStyle(this._container, JSTREE_DIV_STYLES)


        // this._jstree = jQuery('#'+this._id).jstree({ "core": { "data": this.model.data, "check_callback": true}, plugins: this.model.plugins});
        // applyStyle(this.el, JSTREE_DIV_STYLES)
        // set_size(this.el, this.model)
        //if (!(this._container === this.el.childNodes[0]))
        this.shadow_el.appendChild(this._container);

        let kw = {}
        if (!this.model.multiple) {
            kw = {"checkbox": {
                        "three_state": false,
                        "cascade": "undetermined"}}
        }

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

        // jQuery('#'+this._id).jstree({ "core": { "data": this.model.data, "check_callback": true}, plugins: this.model.plugins});
        jQuery('#'+this._id).on('changed.jstree', (e: any, data: any) => this._update_code_from_editor(e, data));
        jQuery('#'+this._id).on('before_open.jstree', (e: any, data: any) => this._listen_for_node_open(e, data));
        jQuery('#'+this._id).on('refresh.jstree', ({}, {}) => this._update_selection_from_value());
        jQuery('#'+this._id).on('create_node.jstree', ({}, {}) => this._update_selection_from_value());

    }
    //
    //   fit() {
    //     const sizing = this.box_sizing();
    //     const vert_margin = sizing.margin == null ? 0 : sizing.margin.top + sizing.margin.bottom;
    //     const horz_margin = sizing.margin == null ? 0 : sizing.margin.left + sizing.margin.right;
    //     const width = (this.layout.inner_bbox.width || this.model.width || 0) - horz_margin;
    //     const height = (this.layout.inner_bbox.height || this.model.height || 0) - vert_margin;
    //     const renderer = this.term._core._renderService;
    //     const cell_width = renderer.dimensions.actualCellWidth || 9;
    //     const cell_height = renderer.dimensions.actualCellHeight || 18;
    //     if (width == null || height == null || width <= 0 || height <= 0)
    //         return;
    //     const cols = Math.max(2, Math.floor(width / cell_width));
    //     const rows = Math.max(1, Math.floor(height / cell_height));
    //     if (this.term.rows !== rows || this.term.cols !== cols)
    //         this.term.resize(cols, rows);
    //     this.model.ncols = cols;
    //     this.model.nrows = rows;
    //     this._rendered = true;
    // }

    _update_code_from_editor({}, data: any): void {
        this.model.value = data.instance.get_selected();
    }
    _update_selection_from_value(): void {
        console.log(this.model.value)
        jQuery('#'+this._id).jstree(true).select_node(this.model.value)
    }

    _update_tree_from_new_nodes(): void {
        console.log(this.model._new_nodes)
        for (let node of this.model._new_nodes){
            jQuery('#'+this._id).jstree(true).create_node(node["parent"], node, "first")
        }
        jQuery('#'+this._id).jstree(true).settings.core.data = jQuery('#'+this._id).jstree(true).get_json(null, {no_li_attr: true, no_a_attr: true, no_data: true})
        this.model.data = jQuery('#'+this._id).jstree(true).settings.core.data
        // this._update_selection_from_value()
    }

    _update_tree_from_data(): void {
        console.log("updating data")
        jQuery('#'+this._id).jstree(true).settings.core.data = this.model.data;
        this.model._flat_tree = jQuery('#'+this._id).jstree(true).get_json(null, {"flat": true})
        console.log("tfd", this.model._flat_tree)

        jQuery('#'+this._id).jstree(true).refresh(false, true);
        // this._update_selection_from_value()

    }


    _update_tree_theme_from_model(): void {
        console.log(this.model.show_dots)
        if (this.model.show_icons) {
            jQuery('#'+this._id).jstree(true).show_icons ( );
        }
        else {
            jQuery('#'+this._id).jstree(true).hide_icons ( );
        }
        if (this.model.show_dots) {
            jQuery('#'+this._id).jstree(true).show_dots ( );
        }
        else {
            jQuery('#'+this._id).jstree(true).hide_dots ( );
        }
        jQuery('#'+this._id).jstree(true).settings.core.multiple = this.model.multiple
        jQuery('#'+this._id).jstree(true).refresh(false, true);
    }

    _listen_for_node_open({}, data: any): void {
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
    url: p.Property<string>
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

      this.define<jsTreePlot.Props>(({Array, Any, Boolean, String}) => ({
        value:          [ Array(Any), []     ],
        data:          [ Array(Any), []     ],
        plugins:       [ Array(Any), []     ],
        multiple:      [ Boolean, true ],
        show_icons:    [ Boolean, true ],
        show_dots:     [ Boolean, true ],
        url: [ String, "" ],
        _last_opened: [ Any, {} ],
        _new_nodes: [ Any, {} ],
        _flat_tree: [ Array(Any), []     ],
      }))
    }
}
