import bpy


# Pasted from Blender script editor so I need to properly format it to work within the addon

if bpy.context.object.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')


bpy.ops.mesh.select_mode(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')
obj = bpy.context.object

group_name = "VGroup.L"
vertex_group = obj.vertex_groups.get(group_name)

if vertex_group is None:
    vertex_group = obj.vertex_groups.new(name=group_name)

# Clear any existing weights
for v in obj.data.vertices:
    vertex_group.remove([v.index])

vertex_group.add([v.index for v in obj.data.vertices if v.select], 1.0, 'REPLACE')
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.symmetrize_vertex_weights(groups='ACTIVE')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')

group_index = obj.vertex_groups[group_name].index

# Deselect all vertices first
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.merge(type='CENTER')
bpy.ops.mesh.select_all(action='DESELECT')

if "VGroup.R" in obj.vertex_groups:
    # Set the active vertex group
    obj.vertex_groups.active = obj.vertex_groups["VGroup.R"]
    
    # Select the vertices in the vertex group
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.merge(type='CENTER')
    
else:
    print("Vertex group 'VGroup.R' not found.")
    
obj = bpy.context.active_object

vertex_groups_to_delete = ["VGroup.L", "VGroup.R"]

for vg_name in vertex_groups_to_delete:
    vg = obj.vertex_groups.get(vg_name)
    if vg is not None:
        obj.vertex_groups.remove(vg)
    else:
        print(f"Vertex group '{vg_name}' not found.")