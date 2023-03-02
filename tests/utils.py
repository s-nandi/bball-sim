from typing import Callable, Any, TypeVar

T = TypeVar("T")


def require_exception(callback: Callable[[], T], exception_type: Any):
    success = False
    try:
        callback()
    except exception_type:
        success = True
    assert success
