"""
parameters/Fileformats/Mesh.py - the mesh files GLB, STL and OBJ: normals and shading.

Every value here is recorded in parameters.txt next to each output.  The files' units are
Run.UNITS; each format is written only when Run.FILE_FORMAT holds "glb", "stl" or "obj".  How
finely a curve is cut into flat faces is in Run_KESE/Geometry.py, and every colour is in its
element's file in PCB_elements/.

Which layers of the board go into the files is set in PCB_elements/Stackup.py; the solder mask and
the silkscreen are left out by default.
"""

# Write a normal for every vertex (GLB, OBJ), so viewers shade the faces as below
EXPORT_INCLUDE_NORMALS = True

# GLB: mark each buffer view as vertex data or indices (keeps the Khronos glTF validator report free of hints)
EXPORT_SET_BUFFERVIEW_TARGETS = True

# Edges sharper than this stay crisp; cylinders shade smooth
SMOOTH_SHADE_ANGLE_DEG = 25.0
