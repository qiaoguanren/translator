from __future__ import annotations

from .xdl import XDL
from .xdl_controller import XDLController

try:  # Python 3.7
    import importlib_metadata as metadata
except ImportError:
    from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = "unknown"
