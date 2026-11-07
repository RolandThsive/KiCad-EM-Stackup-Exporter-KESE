"""RawBoard: a .kicad_pcb file as read, before anything is interpreted."""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RawBoard:
    path: Path
    name: str
    tree: list
    dialect: object                # s1_read/parse_kicad_version.py KicadDialect: everything that differs by version
    generator: str
    copper_layers: list            # outermost first
    file_thickness: float | None
    title: str
    warnings: list = field(default_factory=list)
