import inspect
from functools import partial
from .image import Image
from . import prettyprinter, filemanager

for methods in [prettyprinter, filemanager]:
    for name, f in methods.__dict__.items():
        if not callable(f):
            continue
        arg = next(iter(inspect.signature(f).parameters.keys()), None)
        if arg in ("self", "image"):
            setattr(Image, name, f)
        else:
            setattr(Image, name, staticmethod(f))
