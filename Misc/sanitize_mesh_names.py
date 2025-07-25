import bpy
from bpy.types import Context, Event, Operator

class OBJECT_OT_SanitizeName(Operator):
    """Sanitize all meshes names to prepare for other software that doesn't like certain characters"""
    bl_idname = "obj.sanitize_name"
    bl_label = "Sanitize Names"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    
    @staticmethod
    def sanitize_mesh_name(name):
        # Replace periods with underscores and replaces the Geo suffix
        name = name.replace(' ', '').replace('.', '_').replace(':', '_').replace('-', '_')
        return name.rstrip("_Geo") + "_Mesh"
    
    @staticmethod
    def sanitize_name(name):
        # Replace periods with underscores
        return name.replace('.', '_').replace(':', '_').replace('-', '_')

    @staticmethod
    def rename_mesh_data(objects):
        bpy.ops.object.mode_set(mode='OBJECT')
        
        sanitize_name = OBJECT_OT_SanitizeName.sanitize_name
        sanitize_meshname = OBJECT_OT_SanitizeName.sanitize_mesh_name
        
        for obj in objects:
            if obj.type == 'MESH':
                obj.data.name = sanitize_meshname(obj.name)
                
                obj.name = sanitize_name(obj.name)
                
                if obj.data:
                    obj.data.name = sanitize_meshname(obj.name)
                    
                # Rename shape keys
                if obj.data.shape_keys:
                    for key in obj.data.shape_keys.key_blocks:
                        key.name = sanitize_name(key.name)
                        
                # Rename vertex groups
                for group in obj.vertex_groups:
                    group.name = sanitize_name(group.name)
                    
                # Rename materials
                for mat in obj.data.materials:
                    if mat:
                        mat.name = sanitize_name(mat.name)

    def execute(self, context):
        selected_objects = context.selected_objects
        if selected_objects:
            self.rename_mesh_data(selected_objects)
        else:
            self.rename_mesh_data(bpy.data.objects)
        self.report({'INFO'}, "Renaming done.")
        return {'FINISHED'}

    def invoke(self, context, event=None):
        return context.window_manager.invoke_confirm(self, event)


        
    
    def draw(self, context):
        pass



class OBJECT_OT_SanitizeAllNames(Operator):
    """Confirmation dialog for renaming all objects in the scene"""
    bl_idname = "object.sanitize_all_names"
    bl_label = "Confirm Rename All"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        OBJECT_OT_SanitizeName.rename_mesh_data(bpy.data.objects)
        return {'FINISHED'}
    
    def cancel(self, context):
        return {'CANCELLED'}
    

        
    
class OBJECT_OT_RemoveAllMaterials(Operator):
    bl_idname = "obj.remove_mats"
    bl_label = "Remove All Mats"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def remove_materials_from_objects(objects):
        # Ensure we're in Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Iterate over all selected objects
        for obj in objects:
            if obj.type == 'MESH':
                # Clear all materials
                obj.data.materials.clear()

    def execute(self, context):
        # Get all selected objects
        selected_objects = bpy.context.selected_objects
    
        # Execute the function to remove materials
        self.remove_materials_from_objects(selected_objects)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_SanitizeName)
    bpy.utils.register_class(OBJECT_OT_SanitizeAllNames)
    bpy.utils.register_class(OBJECT_OT_RemoveAllMaterials)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SanitizeName)
    bpy.utils.unregister_class(OBJECT_OT_SanitizeAllNames)
    bpy.utils.unregister_class(OBJECT_OT_RemoveAllMaterials)

if __name__ == "__main__":
    register()