from typing import Literal
from enum import Enum


class ENV(Enum):
    LOCAL = "local"
    PRODUCTION = "production"

IMAGETYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
]

PDFTYPES = [
    "application/pdf",
]