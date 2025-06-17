import bpy
from bpy.types import Operator
import mathutils
from mathutils import kdtree


class OBJECT_FLOPS_normal_blend(Operator):
    """Select Boundary Blend Normal"""
    bl_idname = "mesh.select_boundary_blend"
    bl_label = "Blend normals"
    bl_options = {'REGISTER', 'UNDO'}

    message: bpy.props.StringProperty(
        name="Result",
        description="Operation result",
        default=""
    )
    apply_modifier: bpy.props.BoolProperty(
        name="Apply Modifier",
        description="Apply the Normal Blend modifier after creation",
        default=False
    )
    loop_mapping: bpy.props.EnumProperty(
        name="Loop Mapping",
        description="How loops are mapped for custom normals transfer",
        items=[
            ('TOPOLOGY', "Topology", "Match by topology"),
            ('NEAREST_NORMAL', "Nearest Corner and Best Matching Normal", "Match by nearest normal"),
            ('NEAREST_POLYNOR', "Nearest Nearest Corner and Best Matching Face Normal", "Match by nearest polygon normal"),
            ('NEAREST_POLY', "Nearest Comer of Nearest Face", "Match by nearest polygon"),
            ('POLYINTERP_NEAREST', "Nearest Eace Interpolated", "Interpolated polygon mapping (nearest)"),
            ('POLYINTERP_LNORPROJ', "Projected Face Interpolated", "Interpolated polygon mapping (lnorproj)"),
        ],
        default='NEAREST_NORMAL'
    )
    auto_disable_outline: bpy.props.BoolProperty(
        name="Auto Disable Object Outline",
        description="Automatically disable object outline for better visualization",
        default=True
    )

    def execute(self, context):
        result = self.select_boundary_blend(context)
        if result is not None:
            self.message = result

        # Apply the modifier if the user requested it
        if self.apply_modifier:
            obj = context.object
            mod = obj.modifiers.get("Normal Blend")
        return {'FINISHED'}

    def select_boundary_blend(self, context):
        # Set outline visibility based on user preference
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and hasattr(space.shading, "show_object_outline"):
                        if self.auto_disable_outline:
                            if space.shading.show_object_outline:
                                space.shading.show_object_outline = False
                                self.report({'WARNING'}, "Object Outline has been automatically disabled for better visualization.")
                        else:
                            if not space.shading.show_object_outline:
                                space.shading.show_object_outline = True
                                self.report({'INFO'}, "Object Outline has been re-enabled.")
                break

        obj = bpy.context.object  # Active object (target)
        selected = [o for o in context.selected_objects if o.type == 'MESH']
        # Find the source object
        source = next((o for o in selected if o != obj), None)
        if source is None:
            self.report({'ERROR'}, "Select two mesh objects: target (active) and source")
            return "Error: Select two mesh objects: target (active) and source"

        initial_mode = obj.mode
        if initial_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Build KDTree from source vertices
        source_verts = [source.matrix_world @ v.co for v in source.data.vertices]
        size = len(source_verts)
        kd = kdtree.KDTree(size)
        for i, v in enumerate(source_verts):
            kd.insert(v, i)
        kd.balance()

        # Find matching vertices in target object
        epsilon = 1e-5 # Tolerance for matching vertices
        matching_verts = []
        for v in obj.data.vertices:
            v_world = obj.matrix_world @ v.co
            co, index, dist = kd.find(v_world)
            if dist < epsilon:
                matching_verts.append(v.index)

        # Assign only matching vertices to the group
        if matching_verts:
            group_name = "__boundary"
            vertex_group = obj.vertex_groups.get(group_name)
            if vertex_group is None:
                vertex_group = obj.vertex_groups.new(name=group_name)
            vertex_group.add(matching_verts, 1.0, 'REPLACE')

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
        
    # Draw the operator panel in the UI    
    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message)
        layout.prop(self, "apply_modifier")
        # Grey out loop_mapping when apply_modifier is True
        row = layout.row()
        row.enabled = not self.apply_modifier
        row.prop(self, "loop_mapping")
        layout.prop(self, "auto_disable_outline")  # <-- Add this line

def register():
    bpy.utils.register_class(OBJECT_FLOPS_normal_blend)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_FLOPS_normal_blend)









