bl_info = {
    "name": "FlOps",
    "author": "Floreum",
    "description": "Floreum's operators that I use frequently to speed up my personal workflow and address some of the shortcomings of Blenders symmetry.",
    "blender": (4, 4, 0),
    "version": (0, 4, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

import bpy
from bpy.types import Operator, Panel, Menu
import blf

ADDON_NAME = __name__

# this whole registering system is a mess, but it works for now...

# Organized list of imports
from .prefs import register as prefs_register, unregister as prefs_unregister
from .Preferences import Keymaps


# Menus
from .UI.ui_main import register as register_ui, unregister as unregister_ui
from .UI.FlopsMenus import register as flops_menus_register, unregister as flops_menus_unregister


# General Operators
from .MirrorOps.delete_ops import register as register_delete_ops, unregister as unregister_delete_ops
from .MirrorOps.dissolve_ops import register as register_disolve_ops, unregister as unregister_disolve_ops
from .MirrorOps.MergeCenter import register as register_mirror_merge, unregister as unregister_mirror_merge
from .MirrorOps.mirror_op import register as register_mirroroperator, unregister as unregister_mirroroperator
from .MirrorOps.SymSelectedObjectLoc import register as register_sym_obj_loc, unregister as unregister_sym_obj_loc

# Utility Operators
from .Misc.sanitize_mesh_names import register as register_sanitize_names, unregister as unregister_sanitize_names
from .UI_Additions.sync_visibility import register as register_sync_visibility, unregister as unregister_sync_visibility
from .UI_Additions.temp_layout import register as register_temp_layout, unregister as unregister_temp_layout
from .VertexGroups.vertex_snap import register as register_vertex_snap, unregister as unregister_vertex_snap
from .VertexGroups.BlendNormalsBoundaries import register as register_blend_normals, unregister as unregister_blend_normals
from .GeometryNodes.GN_BlendNormals import register as register_gn_blend_normals, unregister as unregister_gn_blend_normals

# Weight Painting Operators
from .VertexGroups.DeleteVertWeight import register as register_delete_vertex_weights, unregister as unregister_delete_vertex_weights
from .VertexGroups.transfer_mode_weightpaint import register as register_transfer_mode_wp, unregister as unregister_transfer_mode_wp

# Experimental Operators
from .VertexGroups.VertexColSelection import register as register_vertex_color_selection, unregister as unregister_vertex_color_selection
from .UI_Additions.SetAttributes import register as register_setattr, unregister as unregister_setattr
from .Misc.SetOrigin import register as register_setorigin, unregister as unregister_setorigin
from .GeometryNodes.GN_Mask import register as register_gn_mask, unregister as unregister_gn_mask

# Sculpting Operators
from .VertexGroups.VertGroups2FaceSets import register as register_face_set_to_vert_groups, unregister as unregister_face_set_to_vert_groups
from .Sculpting.MaskSelectedVerts import register as register_sculpt_mask_selected_verts, unregister as unregister_sculpt_mask_selected_verts
from .VertexGroups.Weights2FaceSets import register as register_weights_to_face_sets, unregister as unregister_weights_to_face_sets


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
    self.layout.menu("VIEW3D_MT_MirrorDelete")  # Need to move this



cycle_items_kmi = None




def register():
    global cycle_items_kmi
    register = bpy.utils.register_class

    # Preferences
    prefs_register()

    # Menus
    register_ui()
    flops_menus_register()

    # General Operators
    register_mirroroperator()
    register_disolve_ops()
    register_delete_ops()
    register_temp_layout()
    register_mirror_merge()
    register_blend_normals()
    register_gn_blend_normals()
    register_sym_obj_loc()

    # Utility Operators
    register_sanitize_names()
    register_vertex_snap()
    

    # Weight Painting Operators
    register_transfer_mode_wp()
    register_delete_vertex_weights()

    # Experimental Operators
    register_vertex_color_selection()
    register_setattr()
    register_setorigin()
    register_gn_mask()

    # Sculpting Operators
    register_weights_to_face_sets()
    register_sculpt_mask_selected_verts()
    register_face_set_to_vert_groups()


    # Outliner Menus
    register_sync_visibility()
    
    Keymaps.setup_keymaps(__name__)

    


def unregister():
    global cycle_items_kmi
    unregister = bpy.utils.unregister_class
    
    # Preferences
    prefs_unregister()

    # Menus
    unregister_ui()
    flops_menus_unregister()

    # General Operators
    unregister_mirroroperator()
    unregister_disolve_ops()
    unregister_delete_ops()
    unregister_temp_layout()
    unregister_mirror_merge()
    unregister_blend_normals()
    unregister_gn_blend_normals()
    unregister_sym_obj_loc()

    # Utility Operators
    unregister_sanitize_names()
    unregister_vertex_snap()
    

    # Weight Painting Operators
    unregister_transfer_mode_wp()
    unregister_delete_vertex_weights()

    # Experimental Operators
    unregister_vertex_color_selection()
    unregister_setattr()
    unregister_setorigin()
    unregister_gn_mask()


    # Sculpting Operators
    unregister_weights_to_face_sets()
    unregister_sculpt_mask_selected_verts()
    unregister_face_set_to_vert_groups()


    # Outliner Menus
    unregister_sync_visibility()
    
    Keymaps.remove_keymaps()
    
    
    
    


if __name__ == "__main__":
    register()
