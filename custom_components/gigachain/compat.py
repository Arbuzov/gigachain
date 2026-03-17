"""Compatibility patches for gigachat SDK with Python 3.14 and pydantic v1."""
import sys
import types


def apply_gigachat_compat_patch() -> None:
    """Patch gigachat.models.with_x_headers for Python 3.14 + pydantic v1 compatibility.

    Python 3.14 changed annotation evaluation semantics, which breaks pydantic v1's
    metaclass when it encounters nested generic types like Optional[Dict[str, Optional[str]]].
    This patch replaces the problematic class definition with a compatible one before
    the gigachat package is imported.
    """
    if "gigachat.models.with_x_headers" in sys.modules:
        return

    from typing import Any, Dict, Optional

    try:
        from pydantic.v1 import BaseModel, Field
    except ImportError:
        try:
            from pydantic import BaseModel, Field  # type: ignore[no-redef]
        except ImportError:
            return

    class WithXHeaders(BaseModel):
        x_headers: Optional[Dict[str, Any]] = Field(default=None)
        """Служебная информация о запросе (x-request-id, x-session-id, x-client-id)"""

    mod = types.ModuleType("gigachat.models.with_x_headers")
    mod.WithXHeaders = WithXHeaders  # type: ignore[attr-defined]
    sys.modules["gigachat.models.with_x_headers"] = mod
