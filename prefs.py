import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty
# from .Preferences.PrefToggles import 

def update_cycle_items_panel(self, context):
    from .UI import ui_main
    import bpy
    # Unregister menu
    try:
        bpy.utils.unregister_class(ui_main.VIEW3D_MT_CycleItemsPanel)
    except Exception:
        pass
    # Remove keymap if exists
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get("3D View")
    if km:
        for kmi in list(km.keymap_items):
            if kmi.idname == "wm.call_menu" and getattr(kmi.properties, "name", "") == "VIEW3D_MT_CycleItemsPanel":
                km.keymap_items.remove(kmi)
    # Register menu and keymap if enabled
    if self.enable_cycle_items_panel:
        try:
            bpy.utils.register_class(ui_main.VIEW3D_MT_CycleItemsPanel)
        except Exception:
            pass
        # Add keymap
        if km:
            kmi = km.keymap_items.new("wm.call_menu", type="C", value="PRESS", ctrl=True, shift=True)
            kmi.properties.name = "VIEW3D_MT_CycleItemsPanel"

class FlOpsPreferences(AddonPreferences):
    bl_idname = __package__

    enable_cycle_items_panel: BoolProperty(
        name="Enable Cycle Items Panel",
        description="Show the Alt Ops menu (Cycle Items Panel) in the UI",
        default=True,
        update=update_cycle_items_panel
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="FlOps Preferences")
        layout.label(text="You can customize the addon to enable or disable certain features.")
        layout.separator()

        row = layout.row()
        col_left = row.column()
        col_right = row.column()

        # Left box
        box_left = col_left.box()
        box_left.prop(self, "enable_cycle_items_panel")

        # Right box
        box_right = col_right.box()
        box_right.label(text="Right column")

        # Bottom Section
        layout.separator()
        layout.box().label(text="Bottom Text 😂")
        
        # Future section
        layout.separator()

def register():
    bpy.utils.register_class(FlOpsPreferences)

def unregister():
    bpy.utils.unregister_class(FlOpsPreferences)