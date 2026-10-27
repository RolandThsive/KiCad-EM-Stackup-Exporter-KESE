"""Stage 8 - verify (opt-in: Run.VERIFY or --verify): the Model has to prove itself with the
checks in meshes.py and volumes.py; the verdict goes on screen and into report.txt."""
from kese.s8_verify.meshes import verify
from kese.s8_verify.volumes import volumes_agree


def run(files, job):
    if job.verify:
        with job.stage("verify", "verify"):
            files.verify_ok, files.verify_lines = every_check(files.model, files.glb_path)
        job.say("  " + files.verify_lines[0])
    return files


def every_check(model, glb_path=None):
    """Every check on the Model: (ok, report lines), the verdict first."""
    ok, lines = verify(model, glb_path)
    agree, more = volumes_agree(model)
    return ok and agree, [f"Verifier: {'PASS' if ok and agree else 'FAIL'}"] + lines + more
