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
from .ui import VIEW3D_MT_MirrorDelete
from .dissolve_ops import OBJECT_OT_mirror_merge, OBJECT_OT_mirror_DissolveEdges, OBJECT_OT_mirror_DissolveLimited, OBJECT_OT_mirror_DissolveVerts
from .delete_ops import OBJECT_OT_mirror_DeleteFaces, OBJECT_OT_mirror_DeleteVerts
from .temp_layout import OBJECT_OT_cycle_items, OBJECT_OT_mirror_Crease, OBJECT_OT_mirror_Extract, OBJECT_OT_mirror_UVSeams, OBJECT_OT_ripedgemove # this needs to get renamed and put into their own UI menus
from .mirror_op import MirrorOperator



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
