import bpy

# Ensure we are in Edit Mode
if bpy.context.object.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')

# Switch to Vertex Select Mode
bpy.ops.mesh.select_mode(type='VERT')

# Switch to Object Mode to manipulate vertex groups
bpy.ops.object.mode_set(mode='OBJECT')

# Get the active object
obj = bpy.context.object

# Create a new vertex group or get the existing one
group_name = "VGroup.L"
vertex_group = obj.vertex_groups.get(group_name)

if vertex_group is None:
    vertex_group = obj.vertex_groups.new(name=group_name)

# Clear any existing weights
for v in obj.data.vertices:
    vertex_group.remove([v.index])

# Assign the selected vertices to the new group
vertex_group.add([v.index for v in obj.data.vertices if v.select], 1.0, 'REPLACE')

# Switch to Weight Paint Mode
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

# Symmetrize vertex weights
bpy.ops.object.symmetrize_vertex_weights(groups='ACTIVE')

# Switch back to Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

# Ensure we're in Vertex Select Mode
bpy.ops.mesh.select_mode(type='VERT')

# Select vertices from VGroup.L
# Switch to Object Mode to perform selection
bpy.ops.object.mode_set(mode='OBJECT')

# Get the vertex group index
group_index = obj.vertex_groups[group_name].index

# Deselect all vertices first
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.merge(type='CENTER')
bpy.ops.mesh.select_all(action='DESELECT')

# Ensure the object has the vertex group
if "VGroup.R" in obj.vertex_groups:
    # Set the active vertex group to VGroup.R
    obj.vertex_groups.active = obj.vertex_groups["VGroup.R"]
    
    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select the vertices in the vertex group
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.merge(type='CENTER')
    
else:
    print("Vertex group 'VGroup.R' not found.")
    
# Get the active object
obj = bpy.context.active_object

# List of vertex groups to delete
vertex_groups_to_delete = ["VGroup.L", "VGroup.R"]

# Loop through the list and delete each vertex group if it exists
for vg_name in vertex_groups_to_delete:
    vg = obj.vertex_groups.get(vg_name)
    if vg is not None:
        obj.vertex_groups.remove(vg)
    else:
        print(f"Vertex group '{vg_name}' not found.")