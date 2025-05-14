import bpy


class SCULPT_OT_selected_vert_mask_tool(bpy.types.Operator):
    """Mask from Edit Mode Selection"""
    bl_idname = "sculpt.selected_vert_mask_tool"
    bl_label = "Mask from Edit Mode Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if obj.mode == 'SCULPT':

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.hide(unselected=False)
            bpy.ops.object.mode_set(mode='SCULPT')
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
            bpy.ops.sculpt.face_set_change_visibility(mode='TOGGLE')
            bpy.ops.paint.mask_flood_fill(mode='INVERT')

        return {'FINISHED'}



def register():
    bpy.utils.register_class(SCULPT_OT_selected_vert_mask_tool)


def unregister():
    bpy.utils.unregister_class(SCULPT_OT_selected_vert_mask_tool)

