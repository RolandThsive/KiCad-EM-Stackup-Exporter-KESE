"""
parameters/geometry.py - numerical quality of the geometry.

These control how finely curves are faceted and how neighbouring layers are made to share
exact edges.  They do not change dimensions.
"""

# Snapping grid in mm.  All 2D shapes are snapped to it so touching layers share identical
# vertices (no hairline gaps, no T-junctions).  0.0001 mm = 0.1 um.
SNAP_GRID_MM = 0.0001

# Simplification tolerance for copper outlines after union, mm (0 = none)
SIMPLIFY_TOLERANCE_MM = 0.0005

# Circles and arcs
ARC_STEP_DEG = 3.0                      # max angle per segment when flattening arcs
CIRCLE_CHORD_TOLERANCE_MM = 0.002       # max deviation of a flattened circle from the true one
CIRCLE_MIN_QUAD_SEGS = 8                # at least this many segments per quarter circle
CIRCLE_MAX_QUAD_SEGS = 128
TRACK_END_MIN_QUAD_SEGS = 4             # roundness of track ends
BEZIER_SEGMENTS = 32                    # straight pieces per Bezier curve

# Polygons whose rings touch at a single point are opened by this much so they can be meshed
PINCH_POINT_OPENING_MM = 1e-4

# The tops and bottoms of prisms are cut into triangles by earcut, as in KiCad's 3D viewer
TRIANGULATE_CELL_POINTS = 5000          # a polygon with more points than this is cut strip by strip
TRIANGULATE_CELL_MM = 10.0              # width of those strips (KiCad cuts big polygons into 1 cm cells)

# Visual mode (visible skin)
SKIN_BURIED_TEST_OFFSET_MM = 0.0005     # a face is dropped if a point this far outside it lies inside another solid
SKIN_TILE_POINTS = 250_000              # outline points joined at once; a big board is joined in tiles of about this size
