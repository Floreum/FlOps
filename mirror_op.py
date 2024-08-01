import bpy
from bpy.types import Operator

class OBJECT_OT_MirrorOperator(Operator):
    bl_idname = "object.mirror_op"
    bl_label = "Mirror Operator"

    def execute(self, context):
        "Apply mirror based on symmetry mode"
        active_obj = context.active_object
        
        # Check if the active object is valid and has mesh data
        if active_obj and active_obj.type == 'MESH':
            # Determine which mirror axes are enabled
            mirror_axis = set()
            bpy.types.Scene.mirrorOP = True
            if active_obj.use_mesh_mirror_x:
                mirror_axis.add('X')
            if active_obj.use_mesh_mirror_y:
                mirror_axis.add('Y')
            if active_obj.use_mesh_mirror_z:
                mirror_axis.add('Z')
            
            # Check if any axis is enabled
            if mirror_axis:
                if context.scene.mirrorOP:
                    bpy.ops.mesh.select_mirror(axis=mirror_axis, extend=True)
                    
            return {'FINISHED'}
        
class MirrorAxisProperty(bpy.types.PropertyGroup):
    axis: bpy.props.StringProperty(name="Mirror Axis")
