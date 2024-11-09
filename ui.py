import bpy
import bmesh
from bpy.types import Menu
# from .ui
from .sanitize_mesh_names import OBJECT_OT_SanitizeName, OBJECT_OT_RemoveAllMaterials
from .dissolve_ops import OBJECT_OT_mirror_merge, OBJECT_OT_mirror_DissolveEdges, OBJECT_OT_mirror_DissolveLimited, OBJECT_OT_mirror_DissolveVerts
from .delete_ops import OBJECT_OT_mirror_DeleteFaces, OBJECT_OT_mirror_DeleteVerts
from .temp_layout import OBJECT_OT_cycle_items, OBJECT_OT_mirror_Crease, OBJECT_OT_mirror_Extract, OBJECT_OT_mirror_UVSeams, OBJECT_OT_ripedgemove
from .mirror_op import OBJECT_OT_MirrorOperator
from .vertex_snap import OBJECT_OT_vertex_snap
from .MergeCenter import OBJECT_OT_mirror_MergeByCenter
from .DeleteVertWeight import OBJECT_OT_DeleteVertexGroupWeights, OBJECT_OT_CopyVertexWeights
from .VertexColSelection import OBJECT_OT_VertexColorSelection



# Draw the Delete UI
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
        
        
        # come back to this)
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
        
        separator()
        operator(OBJECT_OT_cycle_items.bl_idname)
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
        
        layout.label(text="Alt Ops Menu")
        separator()
        operator(OBJECT_OT_mirror_UVSeams.bl_idname)
        operator(OBJECT_OT_mirror_Crease.bl_idname)
        
        column.label(text="Test")
        separator()
        operator(OBJECT_OT_mirror_Extract.bl_idname)
        operator(OBJECT_OT_ripedgemove.bl_idname)
        layout.separator()
        operator(OBJECT_OT_SanitizeName.bl_idname)
        operator(OBJECT_OT_RemoveAllMaterials.bl_idname)
        # Additional UI elements related to the operator can be added here
        layout.separator()
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("object.delete_vertex_group_weights", text="Delete Selected Vertex Weights")
        layout.operator("object.copy_vertex_weights", text="Copy Active to Selected Vertex Weights")
        
        layout.separator()
        operator("object.vertex_color_selection")
        
        
        
