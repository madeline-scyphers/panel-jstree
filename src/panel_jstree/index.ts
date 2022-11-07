// export {jsTreePlot} from "./models/jstree"

// import {register_models} from "@bokehjs/base"
// register_models(jsTreePlot as any)

import * as PaneljsTree from "./bokeh_extensions/"
export {PaneljsTree}

import {register_models} from "@bokehjs/base"
register_models(PaneljsTree as any)