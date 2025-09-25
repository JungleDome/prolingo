from typing import Callable

from drf_spectacular.utils import extend_schema, extend_schema_view


def extend_schema_with_tags(tag: str) -> Callable:
    """Apply the given swagger tag to every HTTP method defined on the view."""

    def decorator(view_cls):
        method_names = ["get", "post", "put", "patch", "delete"]
        schema_kwargs = {
            method: extend_schema(tags=[tag])
            for method in method_names
            if hasattr(view_cls, method)
        }
        if not schema_kwargs:
            return view_cls
        return extend_schema_view(**schema_kwargs)(view_cls)

    return decorator
