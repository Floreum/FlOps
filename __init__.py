bl_info = {
    "name" : "Fastops",
    "author" : "Floreum",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.types import Operator, Panel, Menu
import blf

from .sanitize_mesh_names import OBJECT_OT_SanitizeName, OBJECT_OT_RemoveAllMaterials



extend = False

bpy.types.Scene.mirrorOP = bpy.props.BoolProperty(
    name="Enable Mirror",
    description="Turns on mirroring for every operation",
    default=True
)

bpy.types.Scene.enableUV = bpy.props.BoolProperty(
    name="Preserve UVs",
    description="Preverses UV's when collapsing",
    default=False
)

bpy.types.Scene.cycle_mode_active = bpy.props.BoolProperty(
    name="Cycle Mode Active",
    description="Indicates whether the cycle mode is active",
    default=False
)

bpy.types.Scene.cycle_mode_op = bpy.props.IntProperty(
    name="Cycle Mode Active",
    description="Cycles through selected after operation is complete",
    default=0
)

bpy.types.Scene.run_check = bpy.props.BoolProperty(
    name="Run Check",
    description="Running",
    default=False
)

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
                
class OBJECT_OT_mirror_merge(Operator):
    """Mirror Merge Operator"""
    bl_idname = "mesh.mirror_merge"
    bl_label = "Collapse"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom merge functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.merge(type='COLLAPSE', uvs=True)
        return {'FINISHED'}

class OBJECT_OT_mirror_DissolveLimited(Operator):
    """Mirror Dissolve Limited Operator"""
    bl_idname = "mesh.mirror_dissolve_limited"
    bl_label = "Dissolve Limited"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_limited()
        return {'FINISHED'}
    
class OBJECT_OT_mirror_DissolveEdges(Operator): # broken? check later
    """Mirror Dissolve Edge Operator"""
    bl_idname = "mesh.mirror_dissolve_edge"
    bl_label = "Dissolve Edges"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_edges()
        return {'FINISHED'}

class OBJECT_OT_mirror_DissolveVerts(Operator):
    """Mirror Dissolve Vert Operator"""
    bl_idname = "mesh.mirror_dissolve_vert"
    bl_label = "Dissolve Verts"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.dissolve_verts()
        return {'FINISHED'}
    
class OBJECT_OT_mirror_DeleteVerts(Operator):
    """Mirror Delete Vert Operator"""
    bl_idname = "mesh.mirror_delete_vert"
    bl_label = "Delete Verts"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
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
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}
    
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
            mo_use_mesh_mirror(context)
            
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
        

# Custom Panel delete this
class VIEW3D_PT_CycleItemsPanel(Panel):
    """Panel for Cycle Items"""
    bl_idname = "VIEW3D_PT_CycleItemsPanel"
    bl_label = "Cycle Items Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        if context.scene.cycle_mode_active:
            layout.label(text="Cycle Mode Active")
            # Additional UI elements related to the operator can be added here
    
class OBJECT_OT_mirror_UVSeams(Operator):
    """Mirror Delete UV Seam Operator"""
    bl_idname = "mesh.mirror_uv_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
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
            mo_use_mesh_mirror(context)
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
            mo_use_mesh_mirror(context)
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
    """Mirror Delete UV Extract Operator"""
    bl_idname = "mesh.mirror_uv_extract"
    bl_label = "Mark Extract"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Custom dissolve functionality
        if context.scene.mirrorOP == True:
            mo_use_mesh_mirror(context)
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.select_all(action='DESELECT')
        
        # Need to create a custom property that it will read in the selections, then reads the suffix, then gives it a new suffix "_extract"
        # got a working example elsewhere and need to look at it, need to make it switch back to edit mode after
        


        return {'FINISHED'}
    
# Draw UI Menu
class VIEW3D_MT_MirrorDelete(Menu):
    bl_idname = "VIEW3D_MT_MirrorDelete"
    bl_label = "Mirror Delete"
    
    
    def draw(self, context):
        layout = self.layout
        separate = layout.separator()
        row = layout.row()
        column = layout.column()
        
        
        # come back to this)
        if context.scene.mirrorOP == False:
            column.label(text="Mirror Disabled")
        if context.scene.mirrorOP == True:
            column.label(text="Mirror Enabled")
        
            
        self.layout.separator()
        self.layout.operator(OBJECT_OT_mirror_DeleteVerts.bl_idname)
        self.layout.operator(OBJECT_OT_mirror_DeleteFaces.bl_idname)
        self.layout.separator()
        
        self.layout.operator(OBJECT_OT_mirror_DissolveLimited.bl_idname)
        self.layout.operator(OBJECT_OT_mirror_DissolveEdges.bl_idname)
        self.layout.operator(OBJECT_OT_mirror_DissolveVerts.bl_idname)
        
        self.layout.separator()
        self.layout.operator(OBJECT_OT_cycle_items.bl_idname)
        if OBJECT_OT_cycle_items == True: #delete this I don't think it does anything
            bpy.types.SpaceView3D.draw_handler_remove(self._txt_activate, 'WINDOW')
        self.layout.operator(OBJECT_OT_mirror_merge.bl_idname)
        self.layout.separator()
        self.layout.operator(OBJECT_OT_mirror_UVSeams.bl_idname)
        self.layout.operator(OBJECT_OT_mirror_Crease.bl_idname)
        
        column.label(text="Test")
        self.layout.separator()
        self.layout.operator(OBJECT_OT_mirror_Extract.bl_idname)
        self.layout.operator(OBJECT_OT_ripedgemove.bl_idname)
        layout.separator()
        self.layout.operator(OBJECT_OT_SanitizeName.bl_idname)
        self.layout.operator(OBJECT_OT_RemoveAllMaterials.bl_idname)
        
        
    
    
        
        
def draw_func(self, context):
    self.layout.menu("VIEW3D_MT_MirrorDelete")

def register():
    register = bpy.utils.register_class
    
    register(OBJECT_OT_mirror_merge)
    register(OBJECT_OT_mirror_DissolveLimited)
    register(OBJECT_OT_mirror_DissolveEdges)
    register(VIEW3D_MT_MirrorDelete)
    register(OBJECT_OT_mirror_DissolveVerts)
    register(OBJECT_OT_mirror_DeleteVerts)
    register(OBJECT_OT_mirror_DeleteFaces)
    register(OBJECT_OT_mirror_UVSeams)
    register(OBJECT_OT_cycle_items)
    register(VIEW3D_PT_CycleItemsPanel)
    register(OBJECT_OT_mirror_Crease)
    register(OBJECT_OT_mirror_Extract)
    register(OBJECT_OT_ripedgemove)
    register(OBJECT_OT_SanitizeName)
    register(OBJECT_OT_RemoveAllMaterials)
    


    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu", type='X', value='PRESS', ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_MirrorDelete"

def unregister():
    unregister = bpy.utils.unregister_class
    
    unregister(OBJECT_OT_mirror_merge)
    unregister(OBJECT_OT_mirror_DissolveLimited)
    unregister(OBJECT_OT_mirror_DissolveEdges)
    unregister(VIEW3D_MT_MirrorDelete)
    unregister(OBJECT_OT_mirror_DissolveVerts)
    unregister(OBJECT_OT_mirror_DeleteVerts)
    unregister(OBJECT_OT_mirror_DeleteFaces)
    unregister(OBJECT_OT_mirror_UVSeams)
    unregister(OBJECT_OT_cycle_items)
    unregister(VIEW3D_PT_CycleItemsPanel)
    unregister(OBJECT_OT_mirror_Crease)
    unregister(OBJECT_OT_mirror_Extract)
    unregister(OBJECT_OT_ripedgemove)
    unregister(OBJECT_OT_SanitizeName)
    unregister(OBJECT_OT_RemoveAllMaterials)
        
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    if km:
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu' and kmi.properties.name == 'VIEW3D_MT_MirrorDelete':
                km.keymap_items.remove(kmi)
                break

if __name__ == "__main__":
    register()
