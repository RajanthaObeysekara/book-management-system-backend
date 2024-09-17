from typing import Dict

def get_not_found_response() -> Dict[str, Dict[str, str]]:
    return {404: {"description": "Not found"}}
