import bpy
from bpy.types import Operator
import bmesh

class OBJECT_OT_vertex_snap(Operator):
    bl_idname = "object.vertex_snap_and_shrinkwrap"
    bl_label = "Add Vertex Group and Shrinkwrap"
    bl_options = {'REGISTER', 'UNDO'}
    
    vertex_group_name: bpy.props.StringProperty(
        name="Vertex Group Name",
        default="root"
    )
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects or len(selected_objects) < 2:
            self.report({'WARNING'}, "Select at least two mesh objects")
            return {'CANCELLED'}
        
        # Ensure the last selected object is used as the target
        target_obj = context.active_object
        
        for obj in selected_objects:
            if obj != target_obj and obj.type == 'MESH':
                vg = self.add_vertex_group_with_weights(obj, self.vertex_group_name)
                self.add_shrinkwrap_modifier(obj, vg.name, target_obj)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def add_vertex_group_with_weights(self, obj, vg_name):
        # Enter Edit Mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Create vertex group
        vg = obj.vertex_groups.new(name=vg_name)
        
        # Use bmesh to get selected vertices
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v.index for v in bm.verts if v.select]
        
        # Return to Object Mode to assign the vertices to the vertex group
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign 100% weight to the selected vertices in the vertex group
        if selected_verts:
            vg.add(selected_verts, 1.0, 'ADD')
        
        return vg
    
    def add_shrinkwrap_modifier(self, obj, vg_name, target_obj):
        mod = obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
        mod.vertex_group = vg_name
        mod.target = target_obj
        mod.wrap_mode = 'INSIDE'  # Set the snap mode to "inside"
        mod.offset = 0.2  # Set the offset to 0.2 meters

# Add to Vertex Group Specials menu
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_vertex_snap.bl_idname)

# Register classes and menu
def register():
    bpy.utils.register_class(OBJECT_OT_vertex_snap)
    bpy.types.MESH_MT_vertex_group_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_vertex_snap)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
