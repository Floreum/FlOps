import bpy
import blf
from bpy.types import Operator, Panel, Menu
from .mirror_op import OBJECT_OT_MirrorOperator, MirrorAxisProperty



# Custom Operator for Cycling Items
class OBJECT_OT_cycle_items(Operator):
    """Cycle Through Items Operator"""
    bl_idname = "mesh.cycle_items"
    bl_label = "Cycle Items"
    bl_options = {'REGISTER', 'UNDO'}

    # Define properties for the dialog

    

    def __init__(self):
        self._item_index = 0  # Initialize the item index
        self._txt_activate = None
        self._txt_instr = None

    def invoke(self, context, event):
        # Show properties dialog
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        context.scene.run_check = True
        
        context.scene.cycle_mode_active = True
        if self._txt_activate is None:
            self._txt_activate = bpy.types.SpaceView3D.draw_handler_add(self.draw_text_activate, (context,), 'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()

        if self._txt_instr is None:
            self._txt_instr = bpy.types.SpaceView3D.draw_handler_add(self.draw_text_activate_instruct, (context,), 'WINDOW', 'POST_PIXEL')
            context.area.tag_redraw()
        
        
        # Add modal handler
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        run_check = context.scene.run_check
        
        if event.type == 'WHEELUPMOUSE':
            bpy.ops.mesh.select_next_item()
            self._item_index += 1
        elif event.type == 'WHEELDOWNMOUSE':
            bpy.ops.mesh.select_prev_item()
            self._item_index -= 1
        elif event.type in {'LEFTMOUSE', 'RET'} and event.value == 'PRESS':
            # Show properties dialog after confirming
            self.report({'INFO'}, "Item selected: {}".format(self._item_index))
            context.scene.cycle_mode_active = False
            
            bpy.ops.mesh.loop_multi_select(ring=True)
            bpy.ops.object.mirror_op()
            
            # Remove draw handler
            if self._txt_activate:
                bpy.types.SpaceView3D.draw_handler_remove(self._txt_activate, 'WINDOW')
                bpy.types.SpaceView3D.draw_handler_remove(self._txt_instr, 'WINDOW')
                self._txt_activate = None
                context.area.tag_redraw()
                
                
                
            return {'FINISHED'}
        elif event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            self.report({'INFO'}, "Operation cancelled")
            context.scene.cycle_mode_active = False
            # Remove draw handler
            if self._txt_activate:
                bpy.types.SpaceView3D.draw_handler_remove(self._txt_activate, 'WINDOW')
                bpy.types.SpaceView3D.draw_handler_remove(self._txt_instr, 'WINDOW')
                # context.area.tag_redraw()
                self._txt_activate = None
                context.area.tag_redraw()
                
                
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}

    def draw_text_activate(self, context):
        # Get the 3D view space
        space = context.space_data
        # Create a new font object
        font_id = 0
        # Define text properties
        blf.position(font_id, 0.5 * context.region.width, 0.03 * context.region.height, 0)
        blf.size(font_id, 20)
        blf.color(font_id, 0.0, 1.0, 0.0, 0.5)
        blf.draw(font_id, "Cycle Mode")
        
    def draw_text_activate_instruct(self, context):
        # Get the 3D view space
        space = context.space_data
        # Create a new font object
        font_id = 1
        # Define text properties
        blf.position(font_id, 0.05 * context.region.width, 0.3 * context.region.height, 0)
        blf.size(font_id, 12)
        blf.color(font_id, 1.0, 1.0, 1.0, 0.8)
        blf.draw(font_id, "MMB + scroll wheel to cycle edges")
        
class OBJECT_OT_mirror_UVSeams(Operator):
    """Mirror Delete UV Seam Operator"""
    bl_idname = "mesh.mirror_uv_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            bpy.ops.object.mirror_op()
        bpy.ops.mesh.mark_seam(clear=False)
        #elif clear == True:
            #bpy.ops.mesh.mark_seam(clear=True)

        return {'FINISHED'}
    
class OBJECT_OT_mirror_Crease(Operator):
    """Mirror Delete UV Crease Operator"""
    bl_idname = "mesh.mirror_uv_crease"
    bl_label = "Mark Crease"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
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
        # Custom dissolve functionality
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
        # Check if mirroring is enabled
        if context.scene.mirrorOP:
            bpy.ops.object.mirror_op()
        
        # Store active mirror axis
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
          