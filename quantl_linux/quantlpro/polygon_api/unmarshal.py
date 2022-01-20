from typing import Type

import polygon_api.library
import polygon_api.definitions

library = polygon_api.library
definitions = polygon_api.definitions

def unmarshal_json(response_type, resp_json) -> Type[library.AnyDefinition]:
    obj = library.name_to_class[response_type]()
    obj.unmarshal_json(resp_json)
    return obj