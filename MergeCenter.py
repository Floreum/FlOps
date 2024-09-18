import bpy
from bpy.types import Operator

class OBJECT_OT_mirror_MergeByCenter(Operator):
    """Mirror Merge by Center"""
    bl_idname = "mesh.mirror_merge_center"
    bl_label = "Merge by Center"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active object
        obj = bpy.context.object

        # Create a new vertex group
        group_name_L = "zzzz9VGroup.L"
        vertex_group_L = obj.vertex_groups.get(group_name_L)

        if vertex_group_L is None:
            vertex_group_L = obj.vertex_groups.new(name=group_name_L)
        bpy.ops.object.vertex_group_assign()
        
        #Assign a new Vertex Group    
        group_name_R = "zzzz9VGroup.R"
        vertex_group_R = obj.vertex_groups.get(group_name_R)

        if vertex_group_R is None:
            vertex_group_R = obj.vertex_groups.new(name=group_name_R)
        bpy.ops.object.vertex_group_assign()
        
        # Then mirror it
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.vertex_group_mirror(use_topology=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Move the selected Vert Group back up then select the vertices, merge, then delete the group.
        bpy.ops.object.vertex_group_move(direction='UP')
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Do the same thing again
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.object.vertex_group_remove(all=False, all_unlocked=False)
        bpy.ops.mesh.select_mirror(extend=True)
        
        return {'FINISHED'}