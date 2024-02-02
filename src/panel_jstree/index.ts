import * as PaneljsTree from "./bokeh_extensions/"
export {PaneljsTree}

import {register_models} from "@bokehjs/base"
register_models(PaneljsTree as any)
