import bpy
import bmesh
import random

def face_sets_to_vertex_groups():
    obj = bpy.context.object

    # Delete all existing vertex groups
    obj.vertex_groups.clear()

    # Ensure we're in Sculpt Mode and go to Edit Mode to work with vertices
    if bpy.context.mode != 'SCULPT':
        bpy.ops.object.mode_set(mode='SCULPT')
    bpy.ops.object.mode_set(mode='EDIT')

    # Create a BMesh to access face data
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    # Get unique face set IDs
    face_set_layer = bm.faces.layers.int.get(".sculpt_face_set")
    if not face_set_layer:
        print("No face sets found.")
        return

    face_set_ids = set(face[face_set_layer] for face in bm.faces)

    # Iterate over each face set ID
    for face_set_id in face_set_ids:
        # Generate a random 6-digit number for the vertex group name
        group_name = f"{random.randint(100000, 999999)}"
        
        # Deselect all faces, then select only faces in the current face set
        bpy.ops.mesh.select_all(action='DESELECT')
        for face in bm.faces:
            if face[face_set_layer] == face_set_id:
                face.select = True

        # Create a vertex group with the random name and assign selected vertices
        vertex_group = obj.vertex_groups.new(name=group_name)
        bpy.ops.object.vertex_group_assign()

    # Deselect everything and update the mesh
    bpy.ops.mesh.select_all(action='DESELECT')
    bmesh.update_edit_mesh(obj.data)

    # Return to Sculpt Mode
    bpy.ops.object.mode_set(mode='SCULPT')
    print("Vertex groups created from face sets.")

# Run the function
face_sets_to_vertex_groups()
