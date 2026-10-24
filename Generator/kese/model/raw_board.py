"""RawBoard: a .kicad_pcb file as read, before anything is interpreted."""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RawBoard:
    path: Path
    name: str
    tree: list
    version: int
    generator: str
    copper_layers: list            # outermost first
    all_layers: list
    file_thickness: float | None
    title: str
    warnings: list = field(default_factory=list)
