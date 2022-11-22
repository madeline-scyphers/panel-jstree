"""
Defines custom jsTree bokeh model to render Ace editor.
"""
from __future__ import absolute_import, division, unicode_literals

from bokeh.core.properties import String, Override, Dict, Any, List, Bool, Enum, JSON
from bokeh.models import HTMLBox
from bokeh.util.compiler import TypeScript

from panel.io.resources import bundled_files, JS_URLS
from panel.util import classproperty

import pathlib

from panel import extension
# pylint: disable=protected-access
extension._imports["jsme"] = "panel_chemistry.bokeh_extensions.jsme_editor"
# pylint: enable=protected-access


TS_CODE = r"""
// @ts-nocheck
import * as p from "core/properties"
// import { HTMLBox, HTMLBoxView } from "models/layouts/html_box"  // duplicated below for now
import { div } from "core/dom"



// I can't figure out how to get the compiled version working, 
// So I for now am only able to do imports form bokeh
// So this code from panel/models/layout.ts I am just copy pasting
// for now 
import {classes, content_size, extents, sized} from "core/dom"
import {color2css} from "core/util/color"
import {VariadicBox} from "core/layout/html"
import {Size, SizeHint, Sizeable} from "core/layout/types"
import {MarkupView} from "models/widgets/markup"
import {HTMLBox, HTMLBoxView} from "models/layouts/html_box"

const JSTREE_DIV_STYLES: {[key: string]: string} = {
    overflow: "auto",
    // height: "auto",
    // width: "auto",
    
    // border:"1px solid silver", 
    minHeight:"200px",
    minWidth:"200px",
     
}
// this one is copy pasted from vtk utils
export function applyStyle(el: HTMLElement, style: {[key: string]: string}) {
  Object.keys(style).forEach((key: any) => {
    el.style[key] = style[key]
  })
}

export function set_size(el: HTMLElement, model: HTMLBox): void {
  let width_policy = model.width != null ? "fixed" : "fit"
  let height_policy = model.height != null ? "fixed" : "fit"
  const {sizing_mode} = model
  if (sizing_mode != null) {
    if (sizing_mode == "fixed")
      width_policy = height_policy = "fixed"
    else if (sizing_mode == "stretch_both")
      width_policy = height_policy = "max"
    else if (sizing_mode == "stretch_width")
      width_policy = "max"
    else if (sizing_mode == "stretch_height")
      height_policy = "max"
    else {
      switch (sizing_mode) {
      case "scale_width":
        width_policy = "max"
        height_policy = "min"
        break
      case "scale_height":
        width_policy = "min"
        height_policy = "max"
        break
      case "scale_both":
        width_policy = "max"
        height_policy = "max"
        break
      default:
        throw new Error("unreachable")
      }
    }
  }
  if (width_policy == "fixed" && model.width)
    el.style.width = model.width + "px";
  else if (width_policy == "max")
    el.style.width = "100%";
  if (model.min_width != null)
    el.style.minWidth = model.min_width + "px";
  if (model.max_width != null)
    el.style.maxWidth = model.max_width + "px";

  if (height_policy == "fixed" && model.height)
    el.style.height = model.height + "px";
  else if (height_policy == "max")
    el.style.height = "100%";
  if (model.min_height != null)
    el.style.minHeight = model.min_height + "px";
  if (model.max_width != null)
    el.style.maxHeight = model.max_height + "px";
}

export class CachedVariadicBox extends VariadicBox {
  private readonly _cache: Map<string, SizeHint> = new Map()
  private readonly _cache_count: Map<string, number> = new Map()

  constructor(readonly el: HTMLElement, readonly sizing_mode: string | null, readonly changed: boolean) {
    super(el)
  }

  protected _measure(viewport: Size): SizeHint {
    const key = [viewport.width, viewport.height, this.sizing_mode]
    const key_str = key.toString()

    // If sizing mode is responsive and has changed since last render
    // we have to wait until second rerender to use cached value
    const min_count = (!this.changed || (this.sizing_mode == 'fixed') || (this.sizing_mode == null)) ? 0 : 1;
    const cached = this._cache.get(key_str);
    const cache_count = this._cache_count.get(key_str)
    if (cached != null && cache_count != null && (cache_count >= min_count)) {
      this._cache_count.set(key_str, cache_count + 1);
      return cached
    }

    const bounded = new Sizeable(viewport).bounded_to(this.sizing.size)
    const size = sized(this.el, bounded, () => {
      const content = new Sizeable(content_size(this.el))
      const {border, padding} = extents(this.el)
      return content.grow_by(border).grow_by(padding).map(Math.ceil)
    })
    this._cache.set(key_str, size);
    this._cache_count.set(key_str, 0);
    return size;
  }

  invalidate_cache(): void {
  }
}

export class PanelMarkupView extends MarkupView {
  _prev_sizing_mode: string | null

  _update_layout(): void {
    let changed = ((this._prev_sizing_mode !== undefined) &&
                   (this._prev_sizing_mode !== this.model.sizing_mode))
    this._prev_sizing_mode = this.model.sizing_mode;
    this.layout = (new CachedVariadicBox(this.el, this.model.sizing_mode, changed) as any)
    this.layout.set_sizing(this.box_sizing())
  }

  render(): void {
    super.render()
    set_size(this.markup_el, this.model)
  }
}

export class PanelHTMLBoxView extends HTMLBoxView {
  _prev_sizing_mode: string | null
  _prev_css_classes: string[]

  connect_signals(): void {
    super.connect_signals()

    // Note due to on_change hack properties must be defined in this order.
    const {css_classes, background} = this.model.properties
    this._prev_css_classes = this.model.css_classes
    this.on_change([css_classes, background], () => {
      // Note: This ensures that changes in the background and changes
      // to the loading parameter in Panel do NOT trigger a full re-render
      const css = []
      let skip = false
      for (const cls of this.model.css_classes) {
        if (cls === 'pn-loading')
          skip = true
        else if (skip)
          skip = false
        else
          css.push(cls)
      }
      const prev = this._prev_css_classes
      if (JSON.stringify(css) === JSON.stringify(prev)) {
        const {background} = this.model
        this.el.style.backgroundColor = background != null ? color2css(background) : ""
        classes(this.el).clear().add(...this.css_classes())
      } else {
        this.invalidate_render()
      }
      this._prev_css_classes = css
    })
  }

  on_change(properties: any, fn: () => void): void {
    // HACKALERT: LayoutDOMView triggers re-renders whenever css_classes change
    // which is very expensive so we do not connect this signal and handle it
    // ourself
    const p = this.model.properties
    if (properties.length === 2 && properties[0] === p.background && properties[1] === p.css_classes) {
      return
    }
    super.on_change(properties, fn)
  }

  _update_layout(): void {
    let changed = ((this._prev_sizing_mode !== undefined) &&
                   (this._prev_sizing_mode !== this.model.sizing_mode))
    this._prev_sizing_mode = this.model.sizing_mode;
    this.layout = new CachedVariadicBox(this.el, this.model.sizing_mode, changed)
    this.layout.set_sizing(this.box_sizing())
  }

  render(): void {
    super.render()
    set_size(this.el, this.model)
  }
}




declare function jQuery(...args: any[]): any

function ID() {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
}

export class jsTreePlotView extends PanelHTMLBoxView {
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

    render(): void {
        super.render()
        
        this._id = ID()
        console.log(this._id)
    
        // this._container = div({id: this._id})
        this._container = div({id: this._id, })
        // applyStyle(this._container, JSTREE_DIV_STYLES)
     
    
        // this._jstree = jQuery('#'+this._id).jstree({ "core": { "data": this.model.data, "check_callback": true}, plugins: this.model.plugins});
        // applyStyle(this.el, JSTREE_DIV_STYLES)
        applyStyle(this._container, JSTREE_DIV_STYLES)
        set_size(this._container, this.model)
        // set_size(this.el, this.model)
        //if (!(this._container === this.el.childNodes[0]))
        this.el.appendChild(this._container);
        
        let kw = {}
        if (!this.model.multiple) {
            kw = {"checkbox": {
                        "three_state": false,
                        "cascade": "undetermined"}}
        }

        this._jstree = jQuery('#'+this._id).jstree(
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

    static init_jsTreePlot(): void {
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
"""

class jsTreePlot(HTMLBox):
    """
    A Bokeh model that wraps around a jsTree editor and renders it inside
    a Bokeh plot.
    """

    __implementation__ = TypeScript(TS_CODE)
    # __implementation__ = str(pathlib.Path(__file__).resolve().parent / "jstree.ts")

    # __javascript_raw__ = [
    #     # JS_URLS['jQuery'],  # not sure why this isn't working with the panel jquery url
    #     'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
    #     'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js'
    # ]

    __css__ = [
        'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css'
    ]
    #
    # @classproperty
    # def __javascript__(cls):
    #     return bundled_files(cls)
    #
    # @classproperty
    # def __css__(cls):
    #     return bundled_files(cls, 'css')
    #
    # # @classproperty
    # # def __js_skip__(cls):
    # #     return {'jsTree': cls.__javascript__[:]}
    #
    # __js_require__ = {
    #     'paths': {
    #         'jstree': 'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min',
    #     },
    #     'exports': {'jstree': 'jsTree'}
    # }

    __javascript__ = ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js']



    plugins = List(Any)
    multiple = Bool(default=True)
    show_icons = Bool(default=True)
    show_dots = Bool(default=True)
    url = String()
    _last_opened = Any()
    _new_nodes = Any()
    _flat_tree = List(Any)

    # Callback properties
    value = List(Any)
    data = List(Any)

