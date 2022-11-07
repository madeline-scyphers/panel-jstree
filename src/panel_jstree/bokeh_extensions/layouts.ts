import {classes, content_size, extents, sized} from "@bokehjs/core/dom"
import {color2css} from "@bokehjs/core/util/color"
import {VariadicBox} from "@bokehjs/core/layout/html"
import {Size, SizeHint, Sizeable} from "@bokehjs/core/layout/types"
import {MarkupView} from "@bokehjs/models/widgets/markup"
import {HTMLBox, HTMLBoxView} from "@bokehjs/models/layouts/html_box"

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
