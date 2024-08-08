import bpy
from bpy.types import Operator

class OBJECT_OT_SanitizeName(Operator):
    """Sanitize all meshes names to prepare for other software that doesn't like certain characters"""
    bl_idname = "obj.sanitize_name"
    bl_label = "Sanitize Names"
    bl_options = {'REGISTER', 'UNDO'}
    
    @staticmethod
    def sanitize_mesh_name(name):
        # Replace periods with underscores and replaces the Geo suffix
        name = name.replace(' ', '')
        return name.replace('.', '_').rstrip("_Geo") + "_Mesh"
    
    def sanitize_name(name):
        # Replace periods with underscores
        
        return name.replace('.', '_')

    @staticmethod
    def rename_mesh_data(objects):
        bpy.ops.object.mode_set(mode='OBJECT')
        
        sanitize_name = OBJECT_OT_SanitizeName.sanitize_name
        sanitize_meshname = OBJECT_OT_SanitizeName.sanitize_mesh_name
        
        # Need to figure out why this isn't working on the object level first
        # probably should take it out of the objects for loops
        for obj in objects:
            if obj.type == 'OBJECT':
                obj.data.name = sanitize_name(obj.data.name)
            
            if obj.type == 'MESH':
                obj.data.name = sanitize_meshname(obj.name)
                
                if obj.data:
                    obj.data.name = sanitize_meshname(obj.name)
                    
                # rename shape keys
                if obj.data.shape_keys:
                    for key in obj.data.shape_keys.key_blocks:
                        key.name = sanitize_name(key.name)
                        
                # rename vertex groups 
                # maybe I should make sure this is bones first so that these get automatically changed that way instead?
                for group in obj.vertex_groups:
                    group.name = sanitize_name(group.name)
                    
                # rename materials
                for mat in obj.data.materials:
                    if mat:
                        mat.name = sanitize_name(mat.name)
            
                

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        # Execute the function to rename mesh data, shape keys, materials, and empties
        self.rename_mesh_data(selected_objects)
        
        return {'FINISHED'}
    
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


