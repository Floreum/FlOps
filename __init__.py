bl_info = {
    "name": "FlOps",
    "author": "Floreum",
    "description": "Floreum's operators that I use frequently to speed up my personal workflow and address some of the shortcomings of Blenders symmetry.",
    "blender": (4, 4, 0),
    "version": (0, 2, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}

import bpy
from bpy.types import Operator, Panel, Menu
import blf

# Organized list of imports

# General Operators
from .MirrorOps.delete_ops import OBJECT_OT_mirror_DeleteFaces, OBJECT_OT_mirror_DeleteVerts
from .MirrorOps.dissolve_ops import (
    OBJECT_OT_mirror_merge,
    OBJECT_OT_mirror_DissolveEdges,
    OBJECT_OT_mirror_DissolveLimited,
    OBJECT_OT_mirror_DissolveVerts,
)
from .MirrorOps.MergeCenter import OBJECT_OT_mirror_MergeByCenter
from .MirrorOps.mirror_op import OBJECT_OT_MirrorOperator, MirrorAxisProperty

# Utility Operators
from .Misc.sanitize_mesh_names import (
    OBJECT_OT_SanitizeName,
    OBJECT_OT_RemoveAllMaterials,
    OBJECT_OT_SanitizeAllNames,
)
from .UI_Additions.sync_visibility import (
    register as register_sync_visibility,
    unregister as unregister_sync_visibility,
)
from .UI_Additions.temp_layout import register as register_temp_layout, unregister as unregister_temp_layout
from .VertexGroups.vertex_snap import OBJECT_OT_vertex_snap
from .VertexGroups.BlendNormalsBoundaries import register as register_blend_normals, unregister as unregister_blend_normals

# Weight Painting Operators
from .VertexGroups.DeleteVertWeight import OBJECT_OT_DeleteVertexGroupWeights, OBJECT_OT_CopyVertexWeights
from .VertexGroups.transfer_mode_weightpaint import register as register_transfer_mode_wp, unregister as unregister_transfer_mode_wp

# Experimental Operators
from .VertexGroups.VertexColSelection import OBJECT_OT_VertexColorSelection
from .UI_Additions.SetAttributes import register as register_setattr, unregister as unregister_setattr
from .Misc.SetOrigin import register as register_setorigin, unregister as unregister_setorigin

# Sculpting Operators
from .VertexGroups.VertGroupsFromFaceSets import SCULPT_OT_FaceSetToVertGroups
from .Sculpting.MaskSelectedVerts import SCULPT_OT_selected_vert_mask_tool
from .VertexGroups.Weights2FaceSets import SCULPT_OT_Weights2FaceSets

# Menus
from .UI.ui_main import register as register_ui, unregister as unregister_ui
from .UI.FlopsMenus import register as flops_menus_register, unregister as flops_menus_unregister

# Properties
bpy.types.Scene.mirrorOP = bpy.props.BoolProperty(
    name="Enable Mirror",
    description="Turns on mirroring for every operation",
    default=True,
)

bpy.types.Scene.enableUV = bpy.props.BoolProperty(
    name="Preserve UVs",
    description="Preserves UVs when collapsing",
    default=False,
)

bpy.types.Scene.cycle_mode_active = bpy.props.BoolProperty(
    name="Cycle Mode Active",
    description="Indicates whether the cycle mode is active",
    default=False,
)

bpy.types.Scene.cycle_mode_op = bpy.props.IntProperty(
    name="Cycle Mode Active",
    description="Cycles through selected after operation is complete",
    default=0,
)

bpy.types.Scene.run_check = bpy.props.BoolProperty(
    name="Run Check",
    description="Running",
    default=False,
)


def draw_func(self, context):
    self.layout.menu("VIEW3D_MT_MirrorDelete")


def register():
    register = bpy.utils.register_class

    # Menus
    register_ui()

    # Properties
    register(MirrorAxisProperty)
    bpy.types.Scene.mirror_axis = bpy.props.CollectionProperty(type=MirrorAxisProperty)

    # General Operators
    register(OBJECT_OT_MirrorOperator)
    register(OBJECT_OT_mirror_merge)
    register(OBJECT_OT_mirror_DissolveLimited)
    register(OBJECT_OT_mirror_DissolveEdges)
    register(OBJECT_OT_mirror_DissolveVerts)
    register(OBJECT_OT_mirror_DeleteVerts)
    register(OBJECT_OT_mirror_DeleteFaces)
    register_temp_layout()
    register(OBJECT_OT_mirror_MergeByCenter)
    register_blend_normals()

    # Utility Operators
    register(OBJECT_OT_SanitizeName)
    register(OBJECT_OT_RemoveAllMaterials)
    register(OBJECT_OT_vertex_snap)
    register(OBJECT_OT_SanitizeAllNames)

    # Weight Painting Operators
    register(OBJECT_OT_DeleteVertexGroupWeights)
    register(OBJECT_OT_CopyVertexWeights)
    register_transfer_mode_wp()

    # Experimental Operators
    register(OBJECT_OT_VertexColorSelection)
    register_setattr()
    register_setorigin()

    # Sculpting Operators
    bpy.utils.register_class(SCULPT_OT_Weights2FaceSets)
    bpy.utils.register_class(SCULPT_OT_selected_vert_mask_tool)
    bpy.utils.register_class(SCULPT_OT_FaceSetToVertGroups)


    # Outliner Menus
    register_sync_visibility()

    # Keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new("wm.call_menu", type="X", value="PRESS", ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_MirrorDelete"

    kmi = km.keymap_items.new("wm.call_menu", type="C", value="PRESS", ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_CycleItemsPanel"

    flops_menus_register()  # <-- Add this at the end of register()


def unregister():
    unregister = bpy.utils.unregister_class

    # Menus
    unregister_ui()
    
    # Properties
    unregister(MirrorAxisProperty)
    del bpy.types.Scene.mirror_axis

    # General Operators
    unregister(OBJECT_OT_MirrorOperator)
    unregister(OBJECT_OT_mirror_merge)
    unregister(OBJECT_OT_mirror_DissolveLimited)
    unregister(OBJECT_OT_mirror_DissolveEdges)
    unregister(OBJECT_OT_mirror_DissolveVerts)
    unregister(OBJECT_OT_mirror_DeleteVerts)
    unregister(OBJECT_OT_mirror_DeleteFaces)
    unregister_temp_layout()
    unregister(OBJECT_OT_mirror_MergeByCenter)
    unregister_blend_normals()

    # Utility Operators
    unregister(OBJECT_OT_SanitizeName)
    unregister(OBJECT_OT_RemoveAllMaterials)
    unregister(OBJECT_OT_vertex_snap)
    unregister(OBJECT_OT_SanitizeAllNames)

    # Weight Painting Operators
    unregister(OBJECT_OT_DeleteVertexGroupWeights)
    unregister(OBJECT_OT_CopyVertexWeights)
    unregister_transfer_mode_wp()

    # Experimental Operators
    unregister(OBJECT_OT_VertexColorSelection)
    unregister_setattr()
    unregister_setorigin()


    # Sculpting Operators
    bpy.utils.unregister_class(SCULPT_OT_Weights2FaceSets)
    bpy.utils.unregister_class(SCULPT_OT_selected_vert_mask_tool)
    bpy.utils.unregister_class(SCULPT_OT_FaceSetToVertGroups)


    # Outliner Menus
    unregister_sync_visibility()

    # Keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get("3D View")
    if km:
        to_remove = []
        for kmi in km.keymap_items:
            if kmi.idname == "wm.call_menu" and getattr(kmi.properties, "name", "") in {
                "VIEW3D_MT_MirrorDelete", "VIEW3D_MT_CycleItemsPanel"
            }:
                to_remove.append(kmi)
        for kmi in to_remove:
            km.keymap_items.remove(kmi)

    flops_menus_unregister()  # <-- Add this at the end of unregister()


if __name__ == "__main__":
    register()
