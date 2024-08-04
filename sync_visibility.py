import bpy
from bpy.types import Operator, Menu

class OUTLINER_SyncRenderWithView(Operator):
    "Sync all visibility of render views with the current state of viewport"
    bl_idname = "view3d.draw_sync_render_view"
    bl_label = "Sync Render with View"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in bpy.context.scene.objects: 
            obj.hide_render = obj.hide_viewport
        return {'FINISHED'}

class OUTLINER_SyncViewWithRender(Operator):
    "Sync all visibility of viewport with the current state of render view"
    bl_idname = "view3d.draw_sync_view_render"
    bl_label = "Sync View with Render"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in bpy.context.scene.objects: 
            obj.hide_viewport = obj.hide_render
        return {'FINISHED'}

class VIEW3D_MT_SyncVisibilityMenu(Menu):
    bl_label = "Sync Visibility"
    bl_idname = "VIEW3D_MT_sync_visibility_menu"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.draw_sync_view_render", text="Viewport <- Render", icon="RESTRICT_VIEW_OFF")
        layout.operator("view3d.draw_sync_render_view", text="Viewport -> Render", icon="RESTRICT_RENDER_OFF")

def draw_sync_visibility_menu(self, context):
    self.layout.menu("VIEW3D_MT_sync_visibility_menu")
