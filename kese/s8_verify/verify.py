"""Stage 8 - verify (opt-in: Run.VERIFY or --verify): the Model has to prove itself with the
checks in meshes.py; the verdict goes on screen and into report.txt."""
from kese.s8_verify.meshes import verify


def run(files, job):
    if job.verify:
        with job.stage("verify", "verify"):
            files.verify_ok, files.verify_lines = verify(files.model, files.glb_path)
        job.say("  " + files.verify_lines[0])
    return files
