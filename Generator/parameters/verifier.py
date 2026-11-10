"""
parameters/verifier.py - the Verifier (stage 8): whether it runs, and what it lets pass.

Every value here is recorded in parameters.txt next to each output.  How many triangles its rays
test at once is Parallel.VERIFY_TRIANGLES_AT_A_TIME.
"""

# Run the Verifier after generation (also: kese --verify).  It adds at most about 1.5 s per board on
# the example boards (the checks stage 6 makes of each part included), more on dense boards.  Results
# go in report.txt.
VERIFY = False
VERIFY_RAYS = 3000                     # rays the Verifier casts through a visual model, along the board's normal
                                       # (vertical when upright), to test its surfaces
VERIFY_VOLUME_TOLERANCE = 1e-7         # a part's volumes from its faces, slices and mesh may differ by this share
                                       # of its volume (the numerical noise of areas and meshes) and still pass
VERIFY_VOLUME_NOISE_MM3 = 1e-9         # and by this many mm3 more, whatever its volume
VERIFY_OPENED_VOLUME_MM3 = 1e-3        # mm3 opening pinch points and sharing vertices may take from a part's prisms
                                       # (or add) and still pass: in all, or else in every piece, none gone
VERIFY_GONE_AREA_MM2 = 1e-4           # mm2: a piece this small may be gone, prisms with no slice left on them (a speck
                                       # of finish a pinch point's cut takes whole); a bigger piece gone fails the part
VERIFY_MERGE_EXTRA_DIGITS = 2          # the closed-mesh check merges vertices this many decimal digits finer than
                                       # the snapping grid (1e-6 mm)
