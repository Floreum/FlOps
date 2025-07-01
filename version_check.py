import bpy

# Stores all version check functions for the preferences

def bl_v4_4():
    try:
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        return bpy.app.version >= (4, 4, 0) and addon_prefs #.enable_cycle_items_panel
    except (KeyError, AttributeError):
        return False

def legacy_normals(): # Check if legacy normals are enabled in preferences for 4.5+
    try:
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        return bpy.app.version >= (4, 5, 0) and addon_prefs.enable_legacy_normal_blend_modifier
    except (KeyError, AttributeError):
        return False
    
    




__all__ = [name for name in globals() if name.startswith("blender_v")]
