// import * as p from "core/properties"
// import { HTMLBox, HTMLBoxView } from "models/layouts/html_box"
// import { div } from "core/dom"

import * as p from "@bokehjs/core/properties"
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box"
import { div } from "@bokehjs/core/dom"


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
  // protected _jstree: any

  initialize(): void {
    super.initialize()
    this._id = ID()
    console.log(this._id)

    this._container = div({
      id: this._id
    })
  }

  connect_signals(): void {
    super.connect_signals()
    this.connect(this.model.properties.data.change, () => this._update_tree_from_data())
    this.connect(this.model.properties._new_nodes.change, () => this._update_tree_from_new_nodes())
    this.connect(this.model.properties.show_icons.change, () => this._update_tree_theme_from_model())
    this.connect(this.model.properties.show_dots.change, () => this._update_tree_theme_from_model())
  }

  render(): void {
    super.render()
    if (!(this._container === this.el.childNodes[0]))
      this.el.appendChild(this._container);

      jQuery('#'+this._id).jstree({ "core": { "data": this.model.data, "check_callback": true}, plugins: this.model.plugins});
      jQuery('#'+this._id).on('changed.jstree', (e: any, data: any) => this._update_code_from_editor(e, data));
      jQuery('#'+this._id).on('before_open.jstree', (e: any, data: any) => this._listen_for_node_open(e, data));

  }

  _update_code_from_editor({}, data: any): void {
    this.model.value = data.instance.get_selected();
  }

  _update_tree_from_new_nodes(): void {
    for (let node of this.model._new_nodes){
        jQuery('#'+this._id).jstree(true).create_node(node["parent"], node, "first")

    }
  }

  _update_tree_from_data(): void {
    jQuery('#'+this._id).jstree(true).settings.core.data = this.model.data;
    jQuery('#'+this._id).jstree(true).refresh();
  }


  _update_tree_theme_from_model(): void {
    if (this.model.show_icons) {
        jQuery('#'+this._id).jstree(true).show_icons ( );
    } else {
        jQuery('#'+this._id).jstree(true).hide_icons ( );
    }
    if (this.model.show_dots) {
        jQuery('#'+this._id).jstree(true).show_dots ( );
    } else {
        jQuery('#'+this._id).jstree(true).hide_dots ( );
    }
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
    show_icons: p.Property<boolean>
    show_dots: p.Property<boolean>
    value: p.Property<any>
    url: p.Property<string>
    _last_opened: p.Property<any>
    _new_nodes: p.Property<any>
  }
}

export interface jsTreePlot extends jsTreePlot.Attrs {}

export class jsTreePlot extends HTMLBox {
  properties: jsTreePlot.Props

  constructor(attrs?: Partial<jsTreePlot.Attrs>) {
    super(attrs)
  }

  static __module__ = "panel_jstree.bokeh_extensions.jstree"

  static init_jsTreePlot(): void {
    this.prototype.default_view = jsTreePlotView

    this.define<jsTreePlot.Props>(({Array, Any, Boolean, String}) => ({
      data:          [ Array(Any), []     ],
      plugins:       [ Array(Any), []     ],
      show_icons:    [ Boolean, true ],
      show_dots:     [ Boolean, true ],
      value: [ Array(Any), []     ],
      url: [ String, "" ],
      _last_opened: [ Any, {} ],
      _new_nodes: [ Any, {} ]
    }))

  }
}