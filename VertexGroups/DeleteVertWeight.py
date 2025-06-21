import bpy
import bmesh 
from bpy.types import Operator

class OBJECT_OT_DeleteVertexGroupWeights(Operator):
    """Delete vertex group weights by prefix input"""
    bl_idname = "object.delete_vertex_group_weights"
    bl_label = "Delete Vertex Group Weights"
    bl_options = {'REGISTER', 'UNDO'}

    # String input for the prefix
    group_prefix: bpy.props.StringProperty(
        name="Vertex Group Prefix",
        description="Prefix of the vertex groups to search for",
        default=""
    )

    def execute(self, context):
        obj = context.object

        # Ensure we are in edit mode
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}

        # Switch temporarily to object mode to access vertex group weights
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the selected vertices
        mesh = obj.data
        selected_vertices = [v for v in mesh.vertices if v.select]

        if not selected_vertices:
            self.report({'WARNING'}, "No vertices selected")
            bpy.ops.object.mode_set(mode='EDIT')  # Return to Edit Mode
            return {'CANCELLED'}

        # Get the vertex groups that start with the inputted prefix
        matching_groups = [vg for vg in obj.vertex_groups if vg.name.startswith(self.group_prefix)]

        if not matching_groups:
            self.report({'INFO'}, f"No vertex groups found starting with '{self.group_prefix}'")
            bpy.ops.object.mode_set(mode='EDIT')  # Return to Edit Mode
            return {'CANCELLED'}

        # Remove the vertex weights for selected vertices in the matching vertex groups
        for vg in matching_groups:
            group_index = vg.index
            for v in selected_vertices:
                # Check if the vertex is in the group
                for group in v.groups:
                    if group.group == group_index:
                        vg.remove([v.index])
                        break  # Stop checking once we remove it from the group

        # Switch back to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Deleted weights from {len(matching_groups)} vertex groups")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Display the popup with the input field
        return context.window_manager.invoke_props_dialog(self)
    

class OBJECT_OT_CopyVertexWeights(bpy.types.Operator):
    """Copy vertex weights from the active vertex to the selected vertices"""
    bl_idname = "object.copy_vertex_weights"
    bl_label = "Copy Vertex Weights"
    bl_options = {'REGISTER', 'UNDO'}

    group_prefix: bpy.props.StringProperty(
        name="Vertex Group Prefix",
        description="Prefix of the vertex groups to copy weights from",
        default=""
    )

    def execute(self, context):
        obj = context.object

        # Ensure we are in Edit Mode
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}

        # Switch to Object Mode temporarily to access vertex group information
        bpy.ops.object.mode_set(mode='OBJECT')

        mesh = obj.data
        selected_vertices = [v for v in mesh.vertices if v.select]

        if not selected_vertices:
            self.report({'WARNING'}, "No vertices selected")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        # Get the active vertex (the last selected one)
        active_vertex = selected_vertices[-1]

        # Find the vertex groups that match the prefix
        matching_groups = [vg for vg in obj.vertex_groups if vg.name.startswith(self.group_prefix)]

        if not matching_groups:
            self.report({'WARNING'}, f"No vertex groups found starting with '{self.group_prefix}'")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        # Copy weights from the active vertex to the other selected vertices
        for v in selected_vertices:
            if v != active_vertex:  # Skip copying to itself
                for group in matching_groups:
                    # Get the weight of the active vertex in this group
                    try:
                        active_weight = group.weight(active_vertex.index)
                    except RuntimeError:
                        active_weight = 0.0  # Active vertex isn't in this group

                    # Assign the same weight to the other selected vertex
                    if active_weight > 0:  # Only add if there's a weight
                        group.add([v.index], active_weight, 'REPLACE')

        # Switch back to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        self.report({'INFO'}, f"Copied weights from active vertex to selected vertices for groups starting with '{self.group_prefix}'")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(OBJECT_OT_DeleteVertexGroupWeights)
    bpy.utils.register_class(OBJECT_OT_CopyVertexWeights)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_DeleteVertexGroupWeights)
    bpy.utils.unregister_class(OBJECT_OT_CopyVertexWeights)

