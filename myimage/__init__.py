import inspect
from importlib import import_module
from pathlib import Path

Image = import_module("." + __package__, __package__).Image
__all__ = ["load", "save"]

IGNORED_SUBMODULES = {"__init__", __package__}
for f in Path(__file__).resolve().parent.iterdir():
    if f.suffix != ".py" or not f.is_file() or f.stem in IGNORED_SUBMODULES:
        continue
    for name, f in import_module("." + f.stem, __package__).__dict__.items():
        if not callable(f):
            continue
        parameters = inspect.signature(f).parameters.keys()
        if next(iter(parameters), None) not in ("self", "image"):
            f = staticmethod(f)
        setattr(Image, name, f)
