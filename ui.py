import bpy
from bpy.types import Menu




class VIEW3D_MT_MirrorDelete(Menu):
    bl_idname = "VIEW3D_MT_MirrorDelete"
    bl_label = "Mirror Delete"
    
    @staticmethod
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
        self.layout.operator(self.OBJECT_OT_mirror_DeleteVerts.bl_idname)
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