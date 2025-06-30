import bpy, mathutils
from bpy.types import Context, Event, Operator
from bpy.props import EnumProperty





#initialize gn_mask node group
def gn_mask_node_group(vertex_group_name = "__Mask"):
    
    # -- Create the node group for the mask modifier --
    
    
    
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
    vertex_groups_socket.default_value = vertex_group_name
    vertex_groups_socket.subtype = 'NONE'
    vertex_groups_socket.attribute_domain = 'POINT'
    

    #Socket Hide
    hide_socket = gn_mask.interface.new_socket(name = "Hide", in_out='INPUT', socket_type = 'NodeSocketBool')
    hide_socket.default_value = True
    hide_socket.attribute_domain = 'POINT'

    #Socket Retain Normals
    retain_normals_socket = gn_mask.interface.new_socket(name = "Retain Normals", in_out='INPUT', socket_type = 'NodeSocketBool')
    retain_normals_socket.default_value = True
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
    set_mesh_normal.mode = 'TANGENT_SPACE'

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

    #node Is Edge Smooth
    is_edge_smooth = gn_mask.nodes.new("GeometryNodeInputEdgeSmooth")
    is_edge_smooth.name = "Is Edge Smooth"

    #node Reroute.002
    reroute_002 = gn_mask.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    #node Reroute.003
    reroute_003 = gn_mask.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    #node Reroute.004
    reroute_004 = gn_mask.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    #node Reroute.005
    reroute_005 = gn_mask.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    #node Reroute.006
    reroute_006 = gn_mask.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    #node Store Named Attribute
    store_named_attribute = gn_mask.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.label = "Store Mark Sharp"
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT_VECTOR'
    #Name
    store_named_attribute.inputs[2].default_value = "Sharp"

    #node Named Attribute.002
    named_attribute_002 = gn_mask.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_002.inputs[0].default_value = "Sharp"

    #node Reroute.007
    reroute_007 = gn_mask.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    #node Reroute.008
    reroute_008 = gn_mask.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"




    #Set locations
    group_input.location = (120.55929565429688, -86.7455062866211)
    group_output.location = (2041.7183837890625, 231.01028442382812)
    delete_geometry.location = (739.5439453125, 72.7951431274414)
    named_attribute.location = (527.3427124023438, -43.68994140625)
    sample_index.location = (594.417236328125, -178.49488830566406)
    sample_nearest.location = (361.6336364746094, -419.5123291015625)
    normal.location = (365.91278076171875, -295.574462890625)
    switch.location = (1855.4951171875, 230.96240234375)
    set_mesh_normal.location = (1465.7322998046875, -117.82703399658203)
    group_input_001.location = (1668.229248046875, 203.6925506591797)
    switch_001.location = (1668.621337890625, 83.55426788330078)
    reroute.location = (524.1443481445312, -8.847688674926758)
    reroute_001.location = (789.5669555664062, 106.52722930908203)
    group_input_002.location = (1498.2479248046875, 78.51254272460938)
    is_edge_smooth.location = (927.391357421875, -29.283342361450195)
    reroute_002.location = (394.9714660644531, -123.1223373413086)
    reroute_003.location = (317.7731628417969, -121.9115219116211)
    reroute_004.location = (313.7630920410156, -500.8111877441406)
    reroute_005.location = (1370.6295166015625, -15.869229316711426)
    reroute_006.location = (1370.6295166015625, -175.86923217773438)
    store_named_attribute.location = (1162.9052734375, 66.39854431152344)
    named_attribute_002.location = (1163.1700439453125, -164.86936950683594)
    reroute_007.location = (1108.1732177734375, -215.0505828857422)
    reroute_008.location = (1110.0377197265625, -83.24942016601562)

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
    is_edge_smooth.width, is_edge_smooth.height = 140.0, 100.0
    reroute_002.width, reroute_002.height = 11.5, 100.0
    reroute_003.width, reroute_003.height = 11.5, 100.0
    reroute_004.width, reroute_004.height = 11.5, 100.0
    reroute_005.width, reroute_005.height = 11.5, 100.0
    reroute_006.width, reroute_006.height = 11.5, 100.0
    store_named_attribute.width, store_named_attribute.height = 140.0, 100.0
    named_attribute_002.width, named_attribute_002.height = 140.0, 100.0
    reroute_007.width, reroute_007.height = 11.5, 100.0
    reroute_008.width, reroute_008.height = 11.5, 100.0

    #initialize gn_mask links
    #switch.Output -> group_output.Geometry
    gn_mask.links.new(switch.outputs[0], group_output.inputs[0])
    #reroute.Output -> delete_geometry.Geometry
    gn_mask.links.new(reroute.outputs[0], delete_geometry.inputs[0])
    #named_attribute.Attribute -> delete_geometry.Selection
    gn_mask.links.new(named_attribute.outputs[0], delete_geometry.inputs[1])
    #group_input.Vertex Groups -> named_attribute.Name
    gn_mask.links.new(group_input.outputs[1], named_attribute.inputs[0])
    #reroute_002.Output -> sample_index.Geometry
    gn_mask.links.new(reroute_002.outputs[0], sample_index.inputs[0])
    #reroute_004.Output -> sample_nearest.Geometry
    gn_mask.links.new(reroute_004.outputs[0], sample_nearest.inputs[0])
    #switch_001.Output -> switch.True
    gn_mask.links.new(switch_001.outputs[0], switch.inputs[2])
    #reroute_001.Output -> switch.False
    gn_mask.links.new(reroute_001.outputs[0], switch.inputs[1])
    #reroute_006.Output -> set_mesh_normal.Mesh
    gn_mask.links.new(reroute_006.outputs[0], set_mesh_normal.inputs[0])
    #group_input_001.Hide -> switch.Switch
    gn_mask.links.new(group_input_001.outputs[2], switch.inputs[0])
    #reroute_005.Output -> switch_001.False
    gn_mask.links.new(reroute_005.outputs[0], switch_001.inputs[1])
    #reroute.Output -> reroute_001.Input
    gn_mask.links.new(reroute.outputs[0], reroute_001.inputs[0])
    #group_input_002.Retain Normals -> switch_001.Switch
    gn_mask.links.new(group_input_002.outputs[3], switch_001.inputs[0])
    #normal.Normal -> sample_index.Value
    gn_mask.links.new(normal.outputs[0], sample_index.inputs[1])
    #sample_nearest.Index -> sample_index.Index
    gn_mask.links.new(sample_nearest.outputs[0], sample_index.inputs[2])
    #reroute_002.Output -> reroute.Input
    gn_mask.links.new(reroute_002.outputs[0], reroute.inputs[0])
    #reroute_003.Output -> reroute_002.Input
    gn_mask.links.new(reroute_003.outputs[0], reroute_002.inputs[0])
    #group_input.Geometry -> reroute_003.Input
    gn_mask.links.new(group_input.outputs[0], reroute_003.inputs[0])
    #reroute_003.Output -> reroute_004.Input
    gn_mask.links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    #store_named_attribute.Geometry -> reroute_005.Input
    gn_mask.links.new(store_named_attribute.outputs[0], reroute_005.inputs[0])
    #reroute_005.Output -> reroute_006.Input
    gn_mask.links.new(reroute_005.outputs[0], reroute_006.inputs[0])
    #delete_geometry.Geometry -> store_named_attribute.Geometry
    gn_mask.links.new(delete_geometry.outputs[0], store_named_attribute.inputs[0])
    #reroute_008.Output -> store_named_attribute.Value
    gn_mask.links.new(reroute_008.outputs[0], store_named_attribute.inputs[3])
    #set_mesh_normal.Mesh -> switch_001.True
    gn_mask.links.new(set_mesh_normal.outputs[0], switch_001.inputs[2])
    #named_attribute_002.Attribute -> set_mesh_normal.Custom Normal
    gn_mask.links.new(named_attribute_002.outputs[0], set_mesh_normal.inputs[1])
    #is_edge_smooth.Smooth -> store_named_attribute.Selection
    gn_mask.links.new(is_edge_smooth.outputs[0], store_named_attribute.inputs[1])
    #sample_index.Value -> reroute_007.Input
    gn_mask.links.new(sample_index.outputs[0], reroute_007.inputs[0])
    #reroute_007.Output -> reroute_008.Input
    gn_mask.links.new(reroute_007.outputs[0], reroute_008.inputs[0])
    return gn_mask

from bpy.props import EnumProperty

def get_vertex_group_items(self, context):
    obj = context.active_object
    if obj and obj.type == 'MESH' and obj.vertex_groups:
        items = [(vg.name, vg.name, "") for vg in obj.vertex_groups]
        if "__Mask" not in [name for name, _, _ in items]:
            items.insert(0, ("__Mask", "__Mask", "Default mask group"))
        return items
    return [("__Mask", "__Mask", "Default mask group")]

class OBJECT_FLOPS_GN_MASK(Operator):
    """Create Geometry Nodes Mask Modifier"""
    bl_idname = "object.flops_gn_mask"
    bl_label = "Geometry Nodes Mask Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    vertex_groups: EnumProperty(
        name="Vertex Group",
        description="Name of the vertex group to use for masking",
        items=get_vertex_group_items,
    )
    
    hide_geometry: bpy.props.BoolProperty(
        name="Hide",
        description="Hide masked geometry",
        default=True
    )

    retain_normals: bpy.props.BoolProperty(
        name="Retain Normals",
        description="Preserve normals from masked geometry",
        default=True
    )


    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh")
            return {'CANCELLED'}

        if not obj.vertex_groups:
            self.report({'ERROR'}, "No vertex groups found on the active mesh")
            return {'CANCELLED'}

        node_group = gn_mask_node_group(self.vertex_groups)

        mod = obj.modifiers.get("GN Mask")
        if mod is None:
            mod = obj.modifiers.new(name="GN Mask", type='NODES')

        mod.node_group = node_group
        
        mod["Socket_3"] = self.hide_geometry
        mod["Socket_4"] = self.retain_normals


        self.report({'INFO'}, f"Geometry Nodes Mask Modifier created using '{self.vertex_groups}' vertex group")
        return {'FINISHED'}


        
        
def register():
    bpy.utils.register_class(OBJECT_FLOPS_GN_MASK)

def unregister():
    bpy.utils.unregister_class(OBJECT_FLOPS_GN_MASK)
    
if __name__ == "__main__":
    register()
    # bpy.ops.object.flops_gn_mask()
    

# gn_mask = gn_mask_node_group()

