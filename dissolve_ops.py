import bpy 
from bpy.types import Operator
from .mirror_op import OBJECT_OT_MirrorOperator
               
class OBJECT_OT_mirror_merge(Operator):
    """Mirror Merge Operator"""
    bl_idname = "mesh.mirror_merge"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom merge functionality
        if context.scene.mirrorOP == True:
            bpy.ops.object.mirror_op()
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
            bpy.ops.object.mirror_op()
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
            bpy.ops.object.mirror_op()
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
            bpy.ops.object.mirror_op()
        bpy.ops.mesh.dissolve_verts()
        return {'FINISHED'}
    