"""
parameters/Run_KESE/Parallel.py - how many processor cores work at once, and how much the work holds in
memory at once.

Every value here is recorded in parameters.txt next to each output.  None of them changes the
model: the files come out the same, byte for byte, however the work is shared out.
"""

# How many threads or processes work at once.  Threads where the 2D geometry library does the work
# (it runs outside Python's lock): the copper layers and the solder mask's minimum web width, group
# by group, in stage 3; both sides of the solder mask and the silkscreen, and the finish's copper
# layers and groups of bores, in stage 4; the faces of the visual-mode skin and the test for its
# hidden triangles, in stage 6; the Verifier's overlap check in stage 8.  Processes of their own
# where much of the work is Python's: in stage 3 the copper layers of a board of 1,000 nets or more,
# in stage 6 the parts built at once in "simulation" mode and the parts sliced for the "visual"
# skin, in stage 7 the parts of a STEP file (PROCESS_WORKERS and PROCESS_MIN_COORDINATES below).
# 0 = one per processor thread this process may use (all of the machine's, unless a job scheduler,
# taskset or a container limits it); 1 = everything in turn, in one process.
WORKERS = 0

# At most this many worker processes at once, in stages 3, 6 and 7; 0 = as many as WORKERS.  Each holds
# its own Python, numpy and shapely (about 36 MB) and the part it builds: NE_Delta in simulation mode
# peaks at 2.80 GB in all with 4 workers and 4.37 GB with 32, and at 3.65 GB with 4 when it writes the
# STEP file too.  A thread costs little memory, so a machine with many threads and little memory can
# keep WORKERS and lower this.  If one is stopped or runs out of memory, the parts left go to half as
# many processes, and to the main process once that would be one; if the processes cannot start,
# the main process builds them; each time with a note in report.txt.  Windows holds at most 61
# processes at once.
PROCESS_WORKERS = 0

# Stage 6 starts worker processes only when the parts hold this many coordinates or more in all
# their prisms, the STEP writer only when their faces do, and stage 3 only when the copper items do
# (on a board of 1,000 nets or more: kese/s3_resolve/copper.py); smaller boards are built part after
# part in the main process, which is faster than starting the processes (about 0.3 s for 4): one of
# the test boards takes 0.10 s that way, and 0.35 s in processes.  0 = processes for every board of
# more than one part (in stage 3, of 1,000 nets or more).
PROCESS_MIN_COORDINATES = 20_000

# Hand the memory that threads freed back to the system after each step done in threads, and in each
# worker process after each part (glibc's malloc_trim, on Linux; elsewhere nothing is done).  glibc
# keeps a pool for each thread and holds on to what is freed in it: NE_Delta in visual mode peaks at
# 2.65 GB with 4 workers and 3.57 GB with 32 with this, and 3.45 GB and 4.76 GB without.  Tens of
# milliseconds per run.
GIVE_BACK_MEMORY = True

# Work done in batches, so that a big board does not hold all of it in memory at once: bigger batches
# are a little faster and take more memory.
SKIN_PROBES_AT_A_TIME = 2_000_000       # visual skin, the test for hidden triangles: triangles probed at once
                                        # (their probe points and normals take about a quarter of a gigabyte)
VERIFY_TRIANGLES_AT_A_TIME = 200_000    # the Verifier's vertical rays: triangles tested at once
STEP_ROWS_AT_A_TIME = 100_000           # the STEP writer: points, edges or faces turned into text at once

# Nets, counted layer by layer: from this many, stage 3 joins the copper layers in processes of their own (if
# PROCESS_MIN_COORDINATES agrees).  Much of a net's work is then Python's (the loop over the nets, the copies
# of the shapes), which threads take in turn: CIAA ACC (6,200) takes 24.3 s in four threads and 13.2 s
# in four processes, ULX4M (5,526) 17.9 s and 8.7 s, a 4-layer board of 1,720 3.7 s and 2.1 s.  With
# fewer nets most of the work is GEOS's, which threads run as fast without sending the shapes to the
# processes and back: NE_Delta (804 nets on 2 layers, 1.6 million coordinates) 8.0 s and 9.3 s.
PROCESS_MIN_NETS = 1000

SKIN_PROBES_PER_SHARE = 100_000         # visual skin, the test for hidden triangles: a slice's probes are shared among
                                        # the threads in shares of at least this many, each share on a copy of the slice
                                        # of its own (a copy and its index take about as long as 30,000 probes)
VERIFY_POLYGONS_PER_THREAD = 2000       # the Verifier's overlap check: fewer polygons are tested in one thread,
VERIFY_GROUPS_PER_WORKER = 4            # more in up to this many groups per worker (a slow group made up for by the others)
WORKER_STOP_WAIT_S = 10                 # seconds a run waits at most for worker processes it stopped to be gone
