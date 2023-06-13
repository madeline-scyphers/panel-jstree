import * as jsTree from "./jstree"
export {jsTree}

import {register_models} from "@bokehjs/base"
register_models(jsTree as any)
