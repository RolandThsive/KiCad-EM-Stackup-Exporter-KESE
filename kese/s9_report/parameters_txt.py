"""parameters.txt: every setting the run used, the command-line overrides first."""
from parameters import P


def write_parameters(path, overrides):
    text = P.snapshot()
    if overrides:
        text = "# command-line overrides applied: " + ", ".join(f"{k}={v!r}" for k, v in overrides) + "\n\n" + text
    path.write_text(text, encoding="utf-8")
    return path
