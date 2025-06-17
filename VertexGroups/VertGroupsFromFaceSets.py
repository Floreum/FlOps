import bpy
import bmesh
import random
from bpy.types import Operator



class SCULPT_OT_FaceSetToVertGroups(Operator):
    bl_idname = "sculpt.face_set_from_vert_groups"
    bl_label = "Create a Vertex Groups from Face Sets"
    bl_description = "Creates vertex groups based on face sets (Useful for GoB)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        
        obj.vertex_groups.clear()

        # Ensure we're in Sculpt Mode and go to Edit Mode to work with vertices
        if bpy.context.mode != 'SCULPT':
            bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        face_set_layer = bm.faces.layers.int.get(".sculpt_face_set")
        if not face_set_layer:
            print("No face sets found.")
            return

        face_set_ids = set(face[face_set_layer] for face in bm.faces)

        # Iterate over each face set ID
        for face_set_id in face_set_ids:
            group_name = f"{random.randint(100000, 999999)}"
            
            bpy.ops.mesh.select_all(action='DESELECT')
            for face in bm.faces:
                if face[face_set_layer] == face_set_id:
                    face.select = True

            # Create a vertex group with the random name and assign selected vertices
            vertex_group = obj.vertex_groups.new(name=group_name)
            bpy.ops.object.vertex_group_assign()

        bpy.ops.mesh.select_all(action='DESELECT')
        bmesh.update_edit_mesh(obj.data)

        bpy.ops.object.mode_set(mode='SCULPT')
        print("Vertex groups created from face sets.")
        
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(SCULPT_OT_FaceSetToVertGroups)


def unregister():
    bpy.utils.unregister_class(SCULPT_OT_FaceSetToVertGroups)

