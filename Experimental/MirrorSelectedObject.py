import bpy
from mathutils import Vector

def mirror_opposite_object():
    obj = bpy.context.active_object
    if not obj:
        print("No object selected.")
        return

    name = obj.name
    mirror_name = None

    if "_l" in name.lower():
        mirror_name = name[: -2] + ("_R" if name[-2:].islower() else "_R")
    elif ".l" in name.lower():
        mirror_name = name[: -2] + (".R" if name[-2:].islower() else ".R")
    elif "_r" in name.lower():
        mirror_name = name[: -2] + ("_L" if name[-2:].islower() else "_L")
    elif ".r" in name.lower():
        mirror_name = name[: -2] + (".L" if name[-2:].islower() else ".L")
    else:
        print("Selected object name does not contain _L/.L/_R/.R")
        return

    mirror_obj = bpy.data.objects.get(mirror_name)
    if not mirror_obj:
        print(f"No object found with name '{mirror_name}'")
        return

    # Mirror the location of the selected object across the X axis
    mirrored_location = Vector(obj.location)
    mirrored_location.x *= -1
    mirror_obj.location = mirrored_location

    print(f"Moved '{mirror_name}' to mirrored position of '{name}'")

mirror_opposite_object()
