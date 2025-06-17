import bpy
from bpy.types import Operator, Menu
import bpy.utils.previews
import os

preview_collections = {}

def get_eye_icon():
    pcoll = preview_collections.get("main")
    if not pcoll:
        pcoll = bpy.utils.previews.new()
        icons_dir = os.path.join(os.path.dirname(__file__), "icons")
        sync_icon_path = os.path.join(icons_dir, "sync_view.svg")
        pcoll.load("sync_view", sync_icon_path, 'IMAGE')
        preview_collections["main"] = pcoll
    return pcoll["sync_view"].icon_id

def clear_icons():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

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

class OUTLINER_MT_SyncVisibilityMenu(bpy.types.Menu):
    bl_label = "Sync Visibility"
    bl_idname = "OUTLINER_MT_sync_visibility_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.draw_sync_view_render", text="Viewport <- Render", icon="RESTRICT_VIEW_OFF")
        layout.operator("view3d.draw_sync_render_view", text="Viewport -> Render", icon="RESTRICT_RENDER_OFF")

def draw_sync_visibility_button(self, context):
    layout = self.layout
    icon_id = get_eye_icon()
    layout.menu(OUTLINER_MT_SyncVisibilityMenu.bl_idname, text="", icon_value=icon_id,)
    

def register():
    bpy.utils.register_class(OUTLINER_SyncRenderWithView)
    bpy.utils.register_class(OUTLINER_SyncViewWithRender)
    bpy.utils.register_class(OUTLINER_MT_SyncVisibilityMenu)
    bpy.types.OUTLINER_HT_header.append(draw_sync_visibility_button)

def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw_sync_visibility_button)
    bpy.utils.unregister_class(OUTLINER_MT_SyncVisibilityMenu)
    bpy.utils.unregister_class(OUTLINER_SyncRenderWithView)
    bpy.utils.unregister_class(OUTLINER_SyncViewWithRender)

