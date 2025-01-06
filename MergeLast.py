import bpy
import bmesh

# this is going to be all useless, as I think I want to reuse Merge Centers code that creates vertex groups. The only thing I want from this is to store and flip the active selection


# Ensure you're in Edit Mode
if bpy.context.object.mode == 'EDIT':
    obj = bpy.context.object
    me = obj.data

    # Get the bmesh data
    bm = bmesh.from_edit_mesh(me)

    # Store the active vertex
    active_vert = None
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert) and elem.select:
            active_vert = elem
            break

    # Get selected vertices
    selected_verts = [v for v in bm.verts if v.select]

    if not selected_verts:
        print("No vertices selected.")
    else:
        # Deselect all vertices
        for v in bm.verts:
            v.select = False

        # Dictionary to store mirrored vertex pairs
        mirrored_verts = {}

        # Loop through selected vertices
        for v in selected_verts:
            # Mirror X-axis position
            mirrored_co = v.co.copy()
            mirrored_co.x = -mirrored_co.x

            # Find the vertex closest to the mirrored position
            closest_vert = None
            min_dist = float('inf')
            for vert in bm.verts:
                dist = (vert.co - mirrored_co).length
                if dist < min_dist:
                    min_dist = dist
                    closest_vert = vert

            # Select the closest mirrored vertex
            if closest_vert:
                closest_vert.select = True
                mirrored_verts[v] = closest_vert

        # Handle the active vertex separately - I need this part of the code
        if active_vert:
            mirrored_active_co = active_vert.co.copy()
            mirrored_active_co.x = -mirrored_active_co.x

            # Find the closest mirrored vertex to the active vertex's mirrored position
            closest_active_vert = None
            min_dist = float('inf')
            for vert in bm.verts:
                dist = (vert.co - mirrored_active_co).length
                if dist < min_dist:
                    min_dist = dist
                    closest_active_vert = vert

            if closest_active_vert:
                # Set the mirrored active vertex as active
                bm.select_history.clear()
                bm.select_history.add(closest_active_vert)

        # Update the mesh to reflect the selection change
        bmesh.update_edit_mesh(me, loop_triangles=False, destructive=False)

        # Force an update of the viewport
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
else:
    print("Please switch to Edit Mode to use this script.")
