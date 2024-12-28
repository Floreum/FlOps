import bpy

class SCULPT_OT_selected_vert_mask_tool(bpy.types.Operator):
    """Mask from Edit Mode Selection"""
    bl_idname = "sculpt.selected_mask_tool"
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

# Function to customize the Mask menu
def custom_draw_mask_menu(self, context):
    # Draw the original Mask menu
    self.layout.operator("paint.mask_flood_fill", text="Invert Mask").mode = 'INVERT'
    self.layout.operator("paint.mask_flood_fill", text="Clear Mask").mode = 'VALUE'
    self.layout.operator("sculpt.mask_from_face_sets", text="Mask from Face Sets Boundary")
    
    # Add your custom operator under "Mask from Face Sets Boundary"
    self.layout.separator()
    self.layout.operator(SCULPT_OT_selected_vert_mask_tool.bl_idname)

# Register and Unregister
def register():
    bpy.utils.register_class(SCULPT_OT_selected_vert_mask_tool)
    # Replace the default VIEW3D_MT_mask menu with our custom version
    bpy.types.VIEW3D_MT_mask.draw = custom_draw_mask_menu

def unregister():
    bpy.utils.unregister_class(SCULPT_OT_selected_vert_mask_tool)
    # Restore the default VIEW3D_MT_mask menu
    del bpy.types.VIEW3D_MT_mask.draw

if __name__ == "__main__":
    register()
