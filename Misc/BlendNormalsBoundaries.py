import bpy
from bpy.types import Operator


class OBJECT_FLOPS_normal_blend(Operator):
    """Select Boundary Blend Normal"""
    bl_idname = "mesh.select_boundary_blend"
    bl_label = "Select Boundary and Blend normals to another object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.select_boundary_blend(context)
        return {'FINISHED'}

    def select_boundary_blend(self, context):
        # Check and disable object outline if enabled
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and hasattr(space.shading, "show_object_outline"):
                        if space.shading.show_object_outline:
                            space.shading.show_object_outline = False
                            self.report({'WARNING'}, "Object Outline was enabled and has been disabled for this operation.")
                break

        obj = bpy.context.object  # Active object (target)
        selected = [o for o in context.selected_objects if o.type == 'MESH']
        # Find the source object (the other selected mesh)
        source = next((o for o in selected if o != obj), None)
        if source is None:
            self.report({'ERROR'}, "Select two mesh objects: target (active) and source")
            return

        # Store the initial mode
        initial_mode = obj.mode

        # Ensure we are in edit mode for selection
        if initial_mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        # Set selection mode to EDGE before selecting non-manifold
        bpy.ops.mesh.select_mode(type="EDGE")

        # Deselect everything
        bpy.ops.mesh.select_all(action='DESELECT')
        # Select boundary edges
        bpy.ops.mesh.select_non_manifold(use_boundary=True)
        # Switch to edge select mode
        bpy.ops.mesh.select_mode(type="EDGE")

        # Get indices of selected boundary edges
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = obj.data
        boundary_verts = set()
        for edge in mesh.edges:
            if edge.select:
                boundary_verts.update(edge.vertices)
        # Assign only boundary vertices to the group
        if boundary_verts:
            group_name = "__boundary"
            vertex_group = obj.vertex_groups.get(group_name)
            if vertex_group is None:
                vertex_group = obj.vertex_groups.new(name=group_name)
            vertex_group.add(list(boundary_verts), 1.0, 'REPLACE')

        # Add or update Data Transfer modifier
        mod = obj.modifiers.get("Normal Blend")
        if mod is None:
            mod = obj.modifiers.new(name="Normal Blend", type='DATA_TRANSFER')
        mod.show_in_editmode = True
        mod.show_on_cage = True
        mod.vertex_group = group_name
        mod.use_loop_data = True
        mod.data_types_loops = {'CUSTOM_NORMAL'}
        mod.object = source  # Set the source object

        # Restore the initial mode
        if initial_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
        
        
def register():
    bpy.utils.register_class(OBJECT_FLOPS_normal_blend)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_FLOPS_normal_blend)









