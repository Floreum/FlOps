import bpy
from mathutils import Vector

def mirror_opposite_object():
    obj = bpy.context.active_object
    if not obj:
        print("No object selected.")
        return

    # Determine mirrored name
    name = obj.name
    if "_L" in name:
        mirror_name = name.replace("_L", "_R")
    elif ".L" in name:
        mirror_name = name.replace(".L", ".R")
    else:
        print("Selected object does not have _L or .L in the name.")
        return

    # Find the mirrored object
    mirror_obj = bpy.data.objects.get(mirror_name)
    if not mirror_obj:
        print(f"No object found with name '{mirror_name}'")
        return

    # Mirror the location across the X axis (world space)
    mirrored_location = Vector(obj.location)
    mirrored_location.x *= -1
    mirror_obj.location = mirrored_location

    print(f"Moved '{mirror_name}' to mirrored position of '{name}'")

mirror_opposite_object()
