"""Files: what stage 7 (write) wrote for one board, and what stage 8 (verify) found."""
from dataclasses import dataclass, field


@dataclass
class Files:
    model: object                                   # the Model they were written from
    out_dir: object                                 # the output folder (Path)
    written: list = field(default_factory=list)     # Paths, in the order written
    glb_path: object = None
    verify_ok: object = None                        # None when the Verifier did not run
    verify_lines: list = field(default_factory=list)
