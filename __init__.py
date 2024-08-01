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
from .ui import VIEW3D_MT_MirrorDelete, VIEW3D_MT_CycleItemsPanel
from .dissolve_ops import OBJECT_OT_mirror_merge, OBJECT_OT_mirror_DissolveEdges, OBJECT_OT_mirror_DissolveLimited, OBJECT_OT_mirror_DissolveVerts
from .delete_ops import OBJECT_OT_mirror_DeleteFaces, OBJECT_OT_mirror_DeleteVerts
from .temp_layout import OBJECT_OT_cycle_items, OBJECT_OT_mirror_Crease, OBJECT_OT_mirror_Extract, OBJECT_OT_mirror_UVSeams, OBJECT_OT_ripedgemove # this needs to get renamed and put into their own UI menus
from .mirror_op import OBJECT_OT_MirrorOperator, MirrorAxisProperty



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



    

        
def draw_func(self, context):
    self.layout.menu("VIEW3D_MT_MirrorDelete")

def register():
    register = bpy.utils.register_class
    
    # Menus
    register(VIEW3D_MT_MirrorDelete)
    register(VIEW3D_MT_CycleItemsPanel)

    
    # Properties
    register(MirrorAxisProperty)
    bpy.types.Scene.mirror_axis = bpy.props.CollectionProperty(type=MirrorAxisProperty)
    
    # Operators
    register(OBJECT_OT_MirrorOperator)
    register(OBJECT_OT_mirror_merge)
    register(OBJECT_OT_mirror_DissolveLimited)
    register(OBJECT_OT_mirror_DissolveEdges)
    register(OBJECT_OT_mirror_DissolveVerts)
    register(OBJECT_OT_mirror_DeleteVerts)
    register(OBJECT_OT_mirror_DeleteFaces)
    register(OBJECT_OT_mirror_UVSeams)
    register(OBJECT_OT_cycle_items)
    register(OBJECT_OT_mirror_Crease)
    register(OBJECT_OT_mirror_Extract)
    register(OBJECT_OT_ripedgemove)
    register(OBJECT_OT_SanitizeName)
    register(OBJECT_OT_RemoveAllMaterials)
    


    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu", type='X', value='PRESS', ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_MirrorDelete"
    
    kmi = km.keymap_items.new("wm.call_menu", type='C', value='PRESS', ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_CycleItemsPanel"
    

def unregister():
    unregister = bpy.utils.unregister_class
    
    # Menus
    unregister(VIEW3D_MT_MirrorDelete)
    unregister(VIEW3D_MT_CycleItemsPanel)
    
    # Properties
    unregister(MirrorAxisProperty)
    del bpy.types.Scene.mirror_axis
    
    # Operators
    unregister(OBJECT_OT_MirrorOperator)
    unregister(OBJECT_OT_mirror_merge)
    unregister(OBJECT_OT_mirror_DissolveLimited)
    unregister(OBJECT_OT_mirror_DissolveEdges)
    unregister(OBJECT_OT_mirror_DissolveVerts)
    unregister(OBJECT_OT_mirror_DeleteVerts)
    unregister(OBJECT_OT_mirror_DeleteFaces)
    unregister(OBJECT_OT_mirror_UVSeams)
    unregister(OBJECT_OT_cycle_items)
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
            if kmi.idname == 'wm.call_menu' and kmi.properties.name == 'VIEW3D_MT_CycleItemsPanel':
                km.keymap_items.remove(kmi)
                break

if __name__ == "__main__":
    register()
