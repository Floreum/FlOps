import bpy

keymaps = []

def setup_keymaps(addon_name):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("wm.call_menu", type="X", value="PRESS", ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_MT_MirrorDelete"
    keymaps.append((km, kmi))

    addon_prefs = bpy.context.preferences.addons[addon_name].preferences
    if addon_prefs.enable_cycle_items_panel:
        kmi = km.keymap_items.new("wm.call_menu", type="C", value="PRESS", ctrl=True, shift=True)
        kmi.properties.name = "VIEW3D_MT_CycleItemsPanel"
        keymaps.append((km, kmi))

def remove_keymaps():
    for km, kmi in keymaps:
        try:
            km.keymap_items.remove(kmi)
        except (ReferenceError, RuntimeError):
            pass
    keymaps.clear()


