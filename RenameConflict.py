import bpy
from bpy.props import StringProperty
from bpy.types import Operator

class VIEW3D_OT_RenameWithConflictResolution(Operator):
    """Rename the selected object with conflict resolution for similar names"""
    bl_idname = "object.rename_with_conflict_resolution"
    bl_label = "Rename with Conflict Resolution"
    bl_options = {'REGISTER', 'UNDO'}
    
    new_name: StringProperty(
        name="New Name",
        description="Enter the new name for the selected object",
        default="RandoG_Body_GEO"
    )
    
    def execute(self, context):
        selected_obj = context.object

        if selected_obj is None:
            self.report({'WARNING'}, "No object is selected.")
            return {'CANCELLED'}
        
        # Check if any objects already use the target name
        if self.new_name in bpy.data.objects:
            # Rename all similarly named objects with a temporary prefix
            counter = 1
            for obj in bpy.data.objects:
                if obj.name.startswith(self.new_name) and obj != selected_obj:
                    # Rename to a temporary name to avoid conflicts
                    obj.name = f"{self.new_name}_temp_{counter:03}"
                    counter += 1

        # Rename the selected object to the target name
        selected_obj.name = self.new_name

        # Rename previously renamed objects to avoid name conflicts
        counter = 1
        for obj in bpy.data.objects:
            if obj.name.startswith(f"{self.new_name}_temp_"):
                obj.name = f"{self.new_name}.{counter:03}"
                counter += 1

        self.report({'INFO'}, f"Renamed selected object to '{self.new_name}' and adjusted other names.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Display a pop-up to allow user input
        return context.window_manager.invoke_props_dialog(self)

# Register the operator and add it to the 3D Viewport Object Context Menu
def menu_func(self, context):
    self.layout.operator(VIEW3D_OT_RenameWithConflictResolution.bl_idname, text="Rename with Conflict Resolution")

# Register and add to the 3D Viewport Object Context Menu
def register():
    bpy.utils.register_class(VIEW3D_OT_RenameWithConflictResolution)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)  # Adding to the 3D Viewport Object Context Menu

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_RenameWithConflictResolution)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
