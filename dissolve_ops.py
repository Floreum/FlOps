import bpy
from bpy.types import Operator, Panel, Menu

def mo_use_mesh_mirror(context):
    "Apply mirror based on symmetry mode"
    active_obj = context.active_object
    
    # Check if the active object is valid and has mesh data
    if active_obj and active_obj.type == 'MESH':
        # Determine which mirror axes are enabled
        mirror_axes = set()
        bpy.types.Scene.mirrorOP = True
        if active_obj.use_mesh_mirror_x:
            mirror_axes.add('X')
        if active_obj.use_mesh_mirror_y:
            mirror_axes.add('Y')
        if active_obj.use_mesh_mirror_z:
            mirror_axes.add('Z')
        # else:
        #     bpy.types.Scene.mirrorOP = False
        
        # Check if any axis is enabled
        if mirror_axes:
            if context.scene.mirrorOP:
                bpy.ops.mesh.select_mirror(axis=mirror_axes, extend=True)
                
class OBJECT_OT_mirror_merge(Operator):
    """Mirror Merge Operator"""
    bl_idname = "mesh.mirror_merge"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom merge functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.merge(type='COLLAPSE', uvs=True)
        return {'FINISHED'}

class OBJECT_OT_mirror_DissolveLimited(Operator):
    """Mirror Dissolve Limited Operator"""
    bl_idname = "mesh.mirror_dissolve_limited"
    bl_label = "Dissolve Limited"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_limited()
        return {'FINISHED'}
    
class OBJECT_OT_mirror_DissolveEdges(Operator): # broken? check later
    """Mirror Dissolve Edge Operator"""
    bl_idname = "mesh.mirror_dissolve_edge"
    bl_label = "Dissolve Edges"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_edges()
        return {'FINISHED'}

class OBJECT_OT_mirror_DissolveVerts(Operator):
    """Mirror Dissolve Vert Operator"""
    bl_idname = "mesh.mirror_dissolve_vert"
    bl_label = "Dissolve Verts"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_verts()
        return {'FINISHED'}
 