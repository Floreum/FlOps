import bpy
import bmesh
from mathutils import Vector

class Flops_OT_Set_Origin_to_Vertices(bpy.types.Operator):
    """
    Reset origin to world center, then set the active object's origin to the center of its selected vertices.
    """
    bl_idname = "object.origin_to_selected_vertices"
    bl_label = "Origin to Selected Vertices"
    bl_description = "Set the object's origin to the selected vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh")
            return {'CANCELLED'}

        # Store current mode
        prev_mode = obj.mode

        bpy.ops.object.mode_set(mode='OBJECT')

        # Reset origin to world center via 3D cursor
        context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Switch to Edit Mode to gather selected verts
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v.co.copy() for v in bm.verts if v.select]
        bpy.ops.object.mode_set(mode='OBJECT')

        if not selected_verts:
            self.report({'WARNING'}, "No vertices selected")
            # Restore previous mode
            bpy.ops.object.mode_set(mode=prev_mode)
            return {'CANCELLED'}

        # Compute local-space centroid of selection
        center_local = sum(selected_verts, Vector()) / len(selected_verts)
        center_world = obj.matrix_world @ center_local
        offset = center_world - obj.location

        # Move mesh vertices to keep geometry stationary
        inv_world = obj.matrix_world.inverted()
        for v in obj.data.vertices:
            v.co -= inv_world @ offset

        # Finally move object origin
        obj.location = center_world

        # Restore previous mode
        bpy.ops.object.mode_set(mode=prev_mode)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.label(text="FlOps")
    self.layout.operator(
        Flops_OT_Set_Origin_to_Vertices.bl_idname,
        text=Flops_OT_Set_Origin_to_Vertices.bl_label,
        icon='OBJECT_ORIGIN'
    )

def snap_pie_menu_func(self, context):
    pie = self.layout.menu_pie()
    # Example: Assign your operator to the BOTTOM slice
    pie.operator(
        Flops_OT_Set_Origin_to_Vertices.bl_idname,
        text="Origin to Selected Vertices",
        icon='OBJECT_ORIGIN'
    )
    # The rest of the pie slices are filled by the original menu

def register():
    bpy.utils.register_class(Flops_OT_Set_Origin_to_Vertices)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_snap_pie.append(snap_pie_menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_snap_pie.remove(snap_pie_menu_func)
    bpy.utils.unregister_class(Flops_OT_Set_Origin_to_Vertices)


if __name__ == "__main__":
    register()
    bpy.ops.object.origin_to_selected_vertices()
