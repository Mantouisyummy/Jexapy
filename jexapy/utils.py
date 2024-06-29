import requests

from dataclasses import make_dataclass

from typing import Any, Dict

def request(method: str, endpoint: str,  headers: dict, payload: dict = None):
    response = requests.request(method, endpoint, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(response.json()['errors'][0]['detail'])
    return response


def create_environment_dataclass(fields: Dict[str, Any]):
    """
    Create a dynamic dataclass with the given fields.

    Args:
        class_name (str): The name of the dataclass.
        fields (Dict[str, Any]): A dictionary where the keys are field names and values are field types.

    Returns:
        Type: The dynamically created dataclass.
    """
    return make_dataclass("Environment", [(name, typ) for name, typ in fields.items()])