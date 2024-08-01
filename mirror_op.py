import bpy
from bpy.types import Operator

class MirrorOperator(Operator):
    bl_idname = "VIEW3D_MT_MirrorOp"
    bl_label = "Mirror Operator"

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