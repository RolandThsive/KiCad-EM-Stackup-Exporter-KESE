"""
parameters/verifier.py - the Verifier (stage 8): whether it runs, and what it lets pass.

Every value here is recorded in parameters.txt next to each output.  How many triangles its rays
test at once is Parallel.VERIFY_TRIANGLES_AT_A_TIME.
"""

# Run the Verifier after generation (also: kese --verify).  It adds about 1-3 s per board on the
# example boards, more on dense boards.  Results go in report.txt.
VERIFY = False
VERIFY_RAYS = 3000                     # rays the Verifier casts through a visual model, along the board's normal
                                       # (vertical when upright), to test its surfaces
VERIFY_VOLUME_TOLERANCE = 1e-7         # a part's volumes from its faces, slices and mesh may differ by this share
                                       # of its volume (the numerical noise of areas and meshes) and still pass
VERIFY_OPENED_VOLUME_MM3 = 1e-3        # mm3 the opened pinch points may take from a part's prisms and still pass
