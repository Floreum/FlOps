import bpy
import blf
import bgl
from bpy.types import Operator, Panel, Menu
from ..MirrorOps.mirror_op import OBJECT_OT_MirrorOperator, MirrorAxisProperty
import bmesh

## I need to make a check for menu items to show up when in edit/object mode

class MESH_OT_cycle_items(Operator):
    """Cycle through mesh elements with the mouse wheel"""
    bl_idname = "mesh.cycle_items"
    bl_label = "Cycle Items"
    bl_options = {'REGISTER', 'UNDO'}

    _handle1 = None
    _handle2 = None
    _handle3 = None


    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH'

    def draw_text_activate(self, context):
        space = context.space_data
        font_id = 0
        blf.position(font_id, 0.5 * context.region.width, 0.03 * context.region.height, 0)
        blf.size(font_id, 20)
        blf.color(font_id, 0.0, 1.0, 0.0, 0.5)
        blf.draw(font_id, "Cycle Mode")

    def draw_text_activate_instruct(self, context):
        space = context.space_data
        font_id = 1
        dpi = context.preferences.system.dpi
        dpi_scale = dpi / 65.0

        # First line
        blf.position(font_id, 0.05 * context.region.width, 0.3 * context.region.height, 0)
        blf.size(font_id, int(12 * dpi_scale))
        blf.color(font_id, 1.0, 1.0, 0.8, 1.0)
        blf.draw(font_id, "Scroll wheel up/down to cycle edges")
        # Second line
        blf.position(font_id, 0.05 * context.region.width, 0.27 * context.region.height, 0)
        blf.draw(font_id, "ESC/Right Click to cancel, Left Click to confirm")

    def draw_text_edge_ring(self, context):
        space = context.space_data
        font_id = 1
        dpi = context.preferences.system.dpi
        dpi_scale = dpi / 65.0
        
        status = "(ON)" if self.edge_ring_mode else "(OFF)"
        blf.position(font_id, 0.05 * context.region.width, 0.24 * context.region.height, 0)
        blf.size(font_id, (12 * dpi_scale))
        blf.color(font_id, 1.0, 1.0, 0.8, 1.0)
        blf.draw(font_id, f"(e) Edge Ring {status}")

    def modal(self, context, event):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            for elem in bm.edges:
                elem.select_set(elem.index in self.initial_selection)
            bmesh.update_edit_mesh(obj.data)
            self.report({'INFO'}, "Cycle Items Cancelled (Selection Restored)")
            self.remove_draw_handlers()
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE':
            # Perform edge ring selection if enabled
            if self.edge_ring_mode:
                bpy.ops.mesh.loop_multi_select(ring=True)
            # Only mirror on confirm
            if context.scene.mirrorOP:
                bpy.ops.object.mirror_op()
            self.report({'INFO'}, f"Cycle Items Finished (Edge Ring {'ON' if self.edge_ring_mode else 'OFF'})")
            self.remove_draw_handlers()
            return {'FINISHED'}

        if event.type == 'E' and event.value == 'PRESS':
            self.edge_ring_mode = not self.edge_ring_mode
            if context.area:
                context.area.tag_redraw()
            return {'RUNNING_MODAL'}

        if event.type == 'WHEELDOWNMOUSE':
            bpy.ops.mesh.select_prev_item()
            return {'RUNNING_MODAL'}
        elif event.type == 'WHEELUPMOUSE':
            bpy.ops.mesh.select_next_item()
            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        self.initial_selection = {e.index for e in bm.edges if e.select}
        self.edge_ring_mode = False
        self._handle1 = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_text_activate, (context,), 'WINDOW', 'POST_PIXEL'
        )
        self._handle2 = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_text_activate_instruct, (context,), 'WINDOW', 'POST_PIXEL'
        )
        self._handle3 = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_text_edge_ring, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        if context.area:
            context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def remove_draw_handlers(self):
        if self._handle1 is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle1, 'WINDOW')
            self._handle1 = None
        if self._handle2 is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle2, 'WINDOW')
            self._handle2 = None
        if self._handle3 is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle3, 'WINDOW')
            self._handle3 = None

class OBJECT_OT_mirror_UVSeams(Operator):
    """Mirror Delete UV Seam Operator"""
    bl_idname = "mesh.mirror_uv_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.scene.mirrorOP == True:
            bpy.ops.object.mirror_op()
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}
    
class OBJECT_OT_mirror_Crease(Operator):
    """Mirror Delete UV Crease Operator"""
    bl_idname = "mesh.mirror_uv_crease"
    bl_label = "Mark Crease"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.scene.mirrorOP == True:
            bpy.ops.object.mirror_op()
        bpy.ops.transform.edge_crease()


        return {'FINISHED'}
    
class OBJECT_OT_ripedgemove(Operator):
    """Mirror Delete UV Rip Edge Move Operator"""
    bl_idname = "mesh.mirror_ripedgemove"
    bl_label = "Rip Edge Move"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.scene.mirrorOP == True:
            bpy.ops.object.mirror_op()
        bpy.ops.mesh.rip_edge_move(MESH_OT_rip_edge={"mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, 
                                                     "use_proportional_connected":False, "use_proportional_projected":False, "release_confirm":False, "use_accurate":False}, 
                                   TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                                                           "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, 
                                                           "proportional_edit_falloff":'SMOOTH', "proportional_size":0.000209987, "use_proportional_connected":False, "use_proportional_projected":False, 
                                                           "snap":False, "snap_elements":{'VERTEX'}, "use_snap_project":False, "snap_target":'CENTER', "use_snap_self":False, "use_snap_edit":True, 
                                                           "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), 
                                                           "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, 
                                                           "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        return {'FINISHED'}
    
class OBJECT_OT_mirror_Extract(Operator):
    """Mirror UV Extract Operator"""
    bl_idname = "mesh.mirror_uv_extract"
    bl_label = "Mark Extract"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.scene.mirrorOP:
            bpy.ops.object.mirror_op()
        
        active_obj = context.active_object
        mirror_axis = []
        
        if active_obj:
            if active_obj.use_mesh_mirror_x:
                mirror_axis.append('X')
            if active_obj.use_mesh_mirror_y:
                mirror_axis.append('Y')
            if active_obj.use_mesh_mirror_z:
                mirror_axis.append('Z')
                
            context.scene.mirror_axis.clear()
            
            for axis in mirror_axis:
                item = context.scene.mirror_axis.add()
                item.axis = axis
        
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type='SELECTED')
        
        new_object = bpy.context.selected_objects[-1]
        
        if new_object:
            base_name = new_object.name.split('.')[0]
            new_object.name = base_name + "_extract"
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        
        if new_object:
            new_object.select_set(True)
            context.view_layer.objects.active = new_object
            
        if new_object:
            for axis in context.scene.mirror_axis:
                if axis == 'X':
                    new_object.use_mesh_mirror_x = True
                elif axis == 'Y':
                    new_object.use_mesh_mirror_y = True
                elif axis == 'Z':
                    new_object.use_mesh_mirror_z = True
                    
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(MESH_OT_cycle_items)
    bpy.utils.register_class(OBJECT_OT_mirror_UVSeams)
    bpy.utils.register_class(OBJECT_OT_mirror_Crease)
    bpy.utils.register_class(OBJECT_OT_ripedgemove)
    bpy.utils.register_class(OBJECT_OT_mirror_Extract)

def unregister():
    bpy.utils.unregister_class(MESH_OT_cycle_items)
    bpy.utils.unregister_class(OBJECT_OT_mirror_UVSeams)
    bpy.utils.unregister_class(OBJECT_OT_mirror_Crease)
    bpy.utils.unregister_class(OBJECT_OT_ripedgemove)
    bpy.utils.unregister_class(OBJECT_OT_mirror_Extract)

if __name__ == "__main__":
    register()
