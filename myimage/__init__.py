from pathlib import Path
from .myimage import Image
from importlib import import_module
import inspect
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
