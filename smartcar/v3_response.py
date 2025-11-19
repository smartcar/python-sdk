from typing import TypedDict, Any, Dict


class Response(TypedDict):
    body: Any
    headers: Dict[str, Any]
