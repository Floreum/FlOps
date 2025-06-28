import bpy, mathutils

#initialize gn_mask node group
def gn_mask_node_group():
    gn_mask = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "GN Mask")

    gn_mask.color_tag = 'NONE'
    gn_mask.description = ""
    gn_mask.default_group_node_width = 140
    

    gn_mask.is_modifier = True

    #gn_mask interface
    #Socket Geometry
    geometry_socket = gn_mask.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = gn_mask.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Vertex Groups
    vertex_groups_socket = gn_mask.interface.new_socket(name = "Vertex Groups", in_out='INPUT', socket_type = 'NodeSocketString')
    vertex_groups_socket.default_value = ""
    vertex_groups_socket.subtype = 'NONE'
    vertex_groups_socket.attribute_domain = 'POINT'

    #Socket Hide
    hide_socket = gn_mask.interface.new_socket(name = "Hide", in_out='INPUT', socket_type = 'NodeSocketBool')
    hide_socket.default_value = False
    hide_socket.attribute_domain = 'POINT'

    #Socket Retain Normals
    retain_normals_socket = gn_mask.interface.new_socket(name = "Retain Normals", in_out='INPUT', socket_type = 'NodeSocketBool')
    retain_normals_socket.default_value = False
    retain_normals_socket.attribute_domain = 'POINT'


    #initialize gn_mask nodes
    #node Group Input
    group_input = gn_mask.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True

    #node Group Output
    group_output = gn_mask.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"

    #node Delete Geometry
    delete_geometry = gn_mask.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"

    #node Named Attribute
    named_attribute = gn_mask.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"

    #node Sample Index
    sample_index = gn_mask.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.data_type = 'FLOAT_VECTOR'

    #node Sample Nearest
    sample_nearest = gn_mask.nodes.new("GeometryNodeSampleNearest")
    sample_nearest.name = "Sample Nearest"
    #Sample Position
    sample_nearest.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Normal
    normal = gn_mask.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"

    #node Switch
    switch = gn_mask.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"

    #node Set Mesh Normal
    set_mesh_normal = gn_mask.nodes.new("GeometryNodeSetMeshNormal")
    set_mesh_normal.name = "Set Mesh Normal"
    set_mesh_normal.mode = 'FREE'

    #node Group Input.001
    group_input_001 = gn_mask.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True

    #node Switch.001
    switch_001 = gn_mask.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"

    #node Reroute
    reroute = gn_mask.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    #node Reroute.001
    reroute_001 = gn_mask.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    #node Group Input.002
    group_input_002 = gn_mask.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[4].hide = True





    #Set locations
    group_input.location = (152.4623260498047, -86.7455062866211)
    group_output.location = (1721.2177734375, 204.67822265625)
    delete_geometry.location = (844.5514526367188, 72.7951431274414)
    named_attribute.location = (632.3502197265625, -43.68994140625)
    sample_index.location = (630.9369506835938, -178.49488830566406)
    sample_nearest.location = (398.1531677246094, -419.5123291015625)
    normal.location = (398.5230407714844, -326.889404296875)
    switch.location = (1532.7318115234375, 214.2721710205078)
    set_mesh_normal.location = (1040.7972412109375, -77.05755615234375)
    group_input_001.location = (1232.7689208984375, 183.95248413085938)
    switch_001.location = (1345.8580322265625, 66.86405181884766)
    reroute.location = (634.3084106445312, 15.936161994934082)
    reroute_001.location = (789.5669555664062, 106.52722930908203)
    group_input_002.location = (1037.34521484375, 61.32982635498047)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    sample_nearest.width, sample_nearest.height = 140.0, 100.0
    normal.width, normal.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    set_mesh_normal.width, set_mesh_normal.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    switch_001.width, switch_001.height = 140.0, 100.0
    reroute.width, reroute.height = 11.5, 100.0
    reroute_001.width, reroute_001.height = 11.5, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0

    #initialize gn_mask links
    #switch.Output -> group_output.Geometry
    gn_mask.links.new(switch.outputs[0], group_output.inputs[0])
    #reroute.Output -> delete_geometry.Geometry
    gn_mask.links.new(reroute.outputs[0], delete_geometry.inputs[0])
    #named_attribute.Attribute -> delete_geometry.Selection
    gn_mask.links.new(named_attribute.outputs[0], delete_geometry.inputs[1])
    #group_input.Vertex Groups -> named_attribute.Name
    gn_mask.links.new(group_input.outputs[1], named_attribute.inputs[0])
    #group_input.Geometry -> sample_index.Geometry
    gn_mask.links.new(group_input.outputs[0], sample_index.inputs[0])
    #group_input.Geometry -> sample_nearest.Geometry
    gn_mask.links.new(group_input.outputs[0], sample_nearest.inputs[0])
    #switch_001.Output -> switch.True
    gn_mask.links.new(switch_001.outputs[0], switch.inputs[2])
    #reroute_001.Output -> switch.False
    gn_mask.links.new(reroute_001.outputs[0], switch.inputs[1])
    #delete_geometry.Geometry -> set_mesh_normal.Mesh
    gn_mask.links.new(delete_geometry.outputs[0], set_mesh_normal.inputs[0])
    #group_input_001.Hide -> switch.Switch
    gn_mask.links.new(group_input_001.outputs[2], switch.inputs[0])
    #delete_geometry.Geometry -> switch_001.False
    gn_mask.links.new(delete_geometry.outputs[0], switch_001.inputs[1])
    #set_mesh_normal.Mesh -> switch_001.True
    gn_mask.links.new(set_mesh_normal.outputs[0], switch_001.inputs[2])
    #reroute.Output -> reroute_001.Input
    gn_mask.links.new(reroute.outputs[0], reroute_001.inputs[0])
    #group_input_002.Retain Normals -> switch_001.Switch
    gn_mask.links.new(group_input_002.outputs[3], switch_001.inputs[0])
    #normal.Normal -> sample_index.Value
    gn_mask.links.new(normal.outputs[0], sample_index.inputs[1])
    #sample_nearest.Index -> sample_index.Index
    gn_mask.links.new(sample_nearest.outputs[0], sample_index.inputs[2])
    #sample_index.Value -> set_mesh_normal.Custom Normal
    gn_mask.links.new(sample_index.outputs[0], set_mesh_normal.inputs[1])
    #group_input.Geometry -> reroute.Input
    gn_mask.links.new(group_input.outputs[0], reroute.inputs[0])
    return gn_mask

gn_mask = gn_mask_node_group()

