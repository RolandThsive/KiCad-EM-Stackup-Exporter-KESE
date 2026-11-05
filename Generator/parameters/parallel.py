"""
parameters/parallel.py - how many processor cores work at once, and how much the work holds in
memory at once.

Every value here is recorded in parameters.txt next to each output.  None of them changes the
model: the files come out the same, byte for byte, however the work is shared out.
"""

# How many threads or processes work at once.  Threads where the 2D geometry library does the work
# (it runs outside Python's lock): the copper layers in stage 3; both sides of the solder mask and
# the silkscreen, and the finish's copper layers and hole spans, in stage 4; the faces of the
# visual-mode skin and the test for its hidden triangles, in stage 6; the Verifier's overlap check in
# stage 8.  Processes of their own where much of the work is Python's: in stage 3 the copper layers
# of a board of 1,000 nets or more, in stage 6 the parts built at once in "simulation" mode and the
# parts sliced for the "visual" skin, in stage 7 the parts of a STEP file (PROCESS_WORKERS and
# PROCESS_MIN_COORDINATES below).
# 0 = one per processor thread this process may use (all of the machine's, unless a job scheduler,
# taskset or a container limits it); 1 = everything in turn, in one process.
WORKERS = 0

# At most this many worker processes at once, in stages 3, 6 and 7; 0 = as many as WORKERS.  Each holds
# its own Python, numpy and shapely (about 36 MB) and the part it builds: NE_Delta in simulation mode
# peaks at 2.8 GB in all with 4 workers and 4.5 GB with 32.  A thread costs little memory, so a
# machine with many threads and little memory can keep WORKERS and lower this.  If the processes
# cannot start, or one is stopped or runs out of memory, the main process builds the parts left,
# with a note in report.txt.  Windows holds at most 61 processes at once.
PROCESS_WORKERS = 0

# Stage 6 starts worker processes only when the parts hold this many coordinates or more in all
# their prisms, the STEP writer only when their faces do, and stage 3 only when the copper items do
# (on a board of 1,000 nets or more: kese/s3_resolve/copper.py); smaller boards are built part after
# part in the main process, which is faster than starting the processes (about 0.3 s for 4): one of
# the test boards takes 0.10 s that way, and 0.35 s in processes.  0 = processes for every board of
# more than one part.
PROCESS_MIN_COORDINATES = 20_000

# Hand the memory that threads freed back to the system after each step done in threads, and in each
# worker process after each part (glibc's malloc_trim, on Linux; elsewhere nothing is done).  glibc
# keeps a pool for each thread and holds on to what is freed in it: NE_Delta in visual mode peaks at
# 3.46 GB with 32 workers with this, and 4.86 GB without.  Tens of milliseconds per run.
GIVE_BACK_MEMORY = True

# Work done in batches, so that a big board does not hold all of it in memory at once: bigger batches
# are a little faster and take more memory.
SKIN_PROBES_AT_A_TIME = 2_000_000       # visual skin, the test for hidden triangles: triangles probed at once
                                        # (their probe points and normals take about a quarter of a gigabyte)
VERIFY_TRIANGLES_AT_A_TIME = 200_000    # the Verifier's vertical rays: triangles tested at once
STEP_ROWS_AT_A_TIME = 100_000           # the STEP writer: points, edges or faces turned into text at once
