import bpy
import bmesh
from mathutils import Color

# Define the target color (for example, green)
target_color = Color((0.0, 1.0, 0.0))  # RGB values for green
tolerance = 0.1  # How close the color needs to be to the target

# Get the active object (must be a mesh and in Edit Mode)
obj = bpy.context.object

# Ensure the object is in Edit Mode
if obj.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')

# Get the active mesh and bmesh data
mesh = obj.data
bm = bmesh.from_edit_mesh(mesh)

# Get the active vertex color layer
if not mesh.vertex_colors.active:
    print("No active vertex color layer found")
else:
    color_layer = bm.loops.layers.color.active

    # Deselect all vertices first
    for v in bm.verts:
        v.select = False

    # Helper function to compare colors with tolerance
    def color_match(col1, col2, tol):
        return all(abs(c1 - c2) <= tol for c1, c2 in zip(col1, col2))

    # Iterate through all faces and loops to check vertex color
    for face in bm.faces:
        for loop in face.loops:
            # Get the color for this loop (vertex)
            color = loop[color_layer]
            # Compare vertex color to the target color within tolerance
            if color_match(color, target_color, tolerance):
                loop.vert.select = True

    # Update the mesh with the changes
    bmesh.update_edit_mesh(mesh)
