import bpy
import bmesh
from bpy.types import Menu
from .. import ADDON_NAME
from .. import version_check

from ..MirrorOps.delete_ops import OBJECT_OT_mirror_DeleteFaces, OBJECT_OT_mirror_DeleteVerts
from ..VertexGroups.DeleteVertWeight import OBJECT_OT_DeleteVertexGroupWeights, OBJECT_OT_CopyVertexWeights
from ..MirrorOps.dissolve_ops import OBJECT_OT_mirror_merge, OBJECT_OT_mirror_DissolveEdges, OBJECT_OT_mirror_DissolveLimited, OBJECT_OT_mirror_DissolveVerts

from ..MirrorOps.MergeCenter import OBJECT_OT_mirror_MergeByCenter
from ..MirrorOps.mirror_op import OBJECT_OT_MirrorOperator, MirrorAxisProperty
from ..MirrorOps.SymSelectedObjectLoc import OBJECT_OT_Symmetrize_Selected_Object_Location

from ..Misc.sanitize_mesh_names import OBJECT_OT_SanitizeName, OBJECT_OT_RemoveAllMaterials, OBJECT_OT_SanitizeAllNames
from ..UI_Additions.temp_layout import MESH_OT_cycle_items, OBJECT_OT_mirror_Crease, OBJECT_OT_mirror_Extract, OBJECT_OT_mirror_UVSeams, OBJECT_OT_ripedgemove # this needs to get renamed and put into its own UI menus

from ..VertexGroups.vertex_snap import OBJECT_OT_vertex_snap
from ..VertexGroups.VertexColSelection import OBJECT_OT_VertexColorSelection
from ..GeometryNodes.GN_Mask import OBJECT_FLOPS_GN_MASK

# versions
legacy_normals = version_check.legacy_normals




# Draw the Delete UI.
class VIEW3D_MT_MirrorDelete(Menu):
    bl_idname = "VIEW3D_MT_MirrorDelete"
    bl_label = "Mirror Delete"
    
    @staticmethod
    def draw(self, context):
        layout = self.layout
        separator = self.layout.separator
        row = layout.row()
        column = layout.column()
        operator = self.layout.operator
        
        
        # Come back to this
        if context.scene.mirrorOP == False:
            column.label(text="Mirror Disabled")
        if context.scene.mirrorOP == True:
            column.label(text="Mirror Enabled")
        
            
        separator()
        operator(OBJECT_OT_mirror_DeleteVerts.bl_idname)
        operator(OBJECT_OT_mirror_DeleteFaces.bl_idname)
        separator()
        
        separator()
        operator(OBJECT_OT_mirror_DissolveLimited.bl_idname)
        operator(OBJECT_OT_mirror_DissolveEdges.bl_idname)
        operator(OBJECT_OT_mirror_DissolveVerts.bl_idname)
        operator(OBJECT_OT_Symmetrize_Selected_Object_Location.bl_idname)
        
        separator()
        layout.operator_context = 'INVOKE_DEFAULT'
        operator(MESH_OT_cycle_items.bl_idname)
        layout.operator_context = 'EXEC_DEFAULT'
        operator(OBJECT_OT_mirror_merge.bl_idname)
        operator(OBJECT_OT_vertex_snap.bl_idname)
        
        separator()
        layout.label(text="Merge by")
        operator(OBJECT_OT_mirror_MergeByCenter.bl_idname)
        
        

        
        
# Panel for the new stuff unrelated to delete I need to come up a name for
class VIEW3D_MT_CycleItemsPanel(Menu):
    "Panel for Cycle Items"
    bl_idname = "VIEW3D_MT_CycleItemsPanel"
    bl_label = "Alt Ops"


    def draw(self, context):
        layout = self.layout
        separator = self.layout.separator
        row = layout.row()
        column = layout.column()
        operator = self.layout.operator
        
        

        
        

        separator()
        operator(OBJECT_OT_mirror_UVSeams.bl_idname)
        operator(OBJECT_OT_mirror_Crease.bl_idname)

        separator()
        operator(OBJECT_OT_mirror_Extract.bl_idname)
        operator(OBJECT_OT_ripedgemove.bl_idname)
        layout.separator()
        operator(OBJECT_OT_SanitizeName.bl_idname)
        operator(OBJECT_OT_RemoveAllMaterials.bl_idname)

        
        # Additional UI elements
        layout.separator()
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("object.delete_vertex_group_weights", text="Delete Selected Vertex Weights")
        layout.operator("object.copy_vertex_weights", text="Copy Active to Selected Vertex Weights")

        layout.separator()
        operator("object.vertex_color_selection")
        
        if bpy.app.version >= (4, 5, 0):
            operator("object.flops_gn_mask")
            operator("object.flops_gn_normal_blend", text="Blend Boundary Normals")
        
        if legacy_normals():
            operator("object.flops_normal_blend_legacy", text="Blend Boundary Normals (Legacy)")
        else:
            operator("object.flops_normal_blend_legacy", text="Blend Boundary Normals")


def register():
    bpy.utils.register_class(VIEW3D_MT_CycleItemsPanel)
    bpy.utils.register_class(VIEW3D_MT_MirrorDelete)
    

def unregister():

    bpy.utils.unregister_class(VIEW3D_MT_CycleItemsPanel)
    bpy.utils.unregister_class(VIEW3D_MT_MirrorDelete)

if __name__ == "__main__":
    register()