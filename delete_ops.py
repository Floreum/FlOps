import bpy
from bpy.types import Operator
from .mirror_op import MirrorOperator

class OBJECT_OT_mirror_DeleteVerts(Operator):
    """Mirror Delete Vert Operator"""
    bl_idname = "mesh.mirror_delete_vert"
    bl_label = "Delete Verts"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            MirrorOperator(context)
        bpy.ops.mesh.delete(type='VERT')
        return {'FINISHED'}
    
class OBJECT_OT_mirror_DeleteFaces(Operator):
    """Mirror Delete Face Operator"""
    bl_idname = "mesh.mirror_delete_face"
    bl_label = "Delete Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            MirrorOperator(context)
        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}
    