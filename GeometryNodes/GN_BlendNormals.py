import bpy
from bpy.types import Operator
import mathutils
from mathutils import kdtree
from .. import ADDON_NAME


def normal_blend_node_group():
    normal_blend = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Normal Blend")

    normal_blend.color_tag = 'NONE'
    normal_blend.description = ""
    normal_blend.default_group_node_width = 140
    

    normal_blend.is_modifier = True

    #normal_blend interface
    #Socket Geometry
    geometry_socket = normal_blend.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = normal_blend.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Object
    object_socket = normal_blend.interface.new_socket(name = "Source", in_out='INPUT', socket_type = 'NodeSocketObject')
    object_socket.attribute_domain = 'POINT'

    #Socket Vertex Group
    vertex_group_socket = normal_blend.interface.new_socket(name = "Vertex Group", in_out='INPUT', socket_type = 'NodeSocketString')
    vertex_group_socket.default_value = "__boundary"
    vertex_group_socket.subtype = 'NONE'
    vertex_group_socket.attribute_domain = 'POINT'


    #initialize normal_blend nodes
    #node Group Input
    group_input = normal_blend.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Group Output
    group_output = normal_blend.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"

    #node Named Attribute
    named_attribute = normal_blend.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"

    #node Object Info.001
    object_info_001 = normal_blend.nodes.new("GeometryNodeObjectInfo")
    object_info_001.name = "Object Info.001"
    #As Instance
    object_info_001.inputs[1].default_value = False

    #node Sample Nearest
    sample_nearest = normal_blend.nodes.new("GeometryNodeSampleNearest")
    sample_nearest.name = "Sample Nearest"
    #Sample Position
    sample_nearest.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Sample Index
    sample_index = normal_blend.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.data_type = 'FLOAT_VECTOR'
    

    #node Set Mesh Normal
    set_mesh_normal = normal_blend.nodes.new("GeometryNodeSetMeshNormal")
    set_mesh_normal.name = "Set Mesh Normal"
    set_mesh_normal.mode = 'TANGENT_SPACE'

    #node Normal
    normal = normal_blend.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"

    #node Switch
    switch = normal_blend.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'VECTOR'

    #node Reroute
    reroute = normal_blend.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    #node Reroute.001
    reroute_001 = normal_blend.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    #node Reroute.002
    reroute_002 = normal_blend.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    #node Reroute.003
    reroute_003 = normal_blend.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"




    #Set locations
    group_input.location = (-1356.3408203125, -144.27955627441406)
    group_output.location = (89.2410659790039, -147.4367218017578)
    named_attribute.location = (-602.1201782226562, -542.9856567382812)
    object_info_001.location = (-1132.44091796875, -255.4764862060547)
    sample_nearest.location = (-808.6032104492188, -198.55416870117188)
    sample_index.location = (-584.9135131835938, -207.0968780517578)
    set_mesh_normal.location = (-115.66053009033203, -97.08987426757812)
    normal.location = (-818.74365234375, -408.56689453125)
    switch.location = (-311.4276123046875, -331.9448547363281)
    reroute.location = (-918.2396850585938, -224.11387634277344)
    reroute_001.location = (-873.2657470703125, -379.6064453125)
    reroute_002.location = (-647.1483154296875, -379.4969482421875)
    reroute_003.location = (-915.63720703125, -648.2503051757812)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    object_info_001.width, object_info_001.height = 140.0, 100.0
    sample_nearest.width, sample_nearest.height = 140.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    set_mesh_normal.width, set_mesh_normal.height = 140.0, 100.0
    normal.width, normal.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    reroute.width, reroute.height = 11.5, 100.0
    reroute_001.width, reroute_001.height = 11.5, 100.0
    reroute_002.width, reroute_002.height = 11.5, 100.0
    reroute_003.width, reroute_003.height = 11.5, 100.0

    #initialize normal_blend links
    #reroute_001.Output -> sample_nearest.Geometry
    normal_blend.links.new(reroute_001.outputs[0], sample_nearest.inputs[0])
    #reroute_002.Output -> sample_index.Geometry
    normal_blend.links.new(reroute_002.outputs[0], sample_index.inputs[0])
    #group_input.Geometry -> set_mesh_normal.Mesh
    normal_blend.links.new(group_input.outputs[0], set_mesh_normal.inputs[0])
    #set_mesh_normal.Mesh -> group_output.Geometry
    normal_blend.links.new(set_mesh_normal.outputs[0], group_output.inputs[0])
    #normal.Normal -> sample_index.Value
    normal_blend.links.new(normal.outputs[0], sample_index.inputs[1])
    #sample_nearest.Index -> sample_index.Index
    normal_blend.links.new(sample_nearest.outputs[0], sample_index.inputs[2])
    #switch.Output -> set_mesh_normal.Custom Normal
    normal_blend.links.new(switch.outputs[0], set_mesh_normal.inputs[1])
    #named_attribute.Attribute -> switch.Switch
    normal_blend.links.new(named_attribute.outputs[0], switch.inputs[0])
    #sample_index.Value -> switch.True
    normal_blend.links.new(sample_index.outputs[0], switch.inputs[2])
    #normal.Normal -> switch.False
    normal_blend.links.new(normal.outputs[0], switch.inputs[1])
    #group_input.Object -> object_info_001.Object
    normal_blend.links.new(group_input.outputs[1], object_info_001.inputs[0])
    #reroute_003.Output -> named_attribute.Name
    normal_blend.links.new(reroute_003.outputs[0], named_attribute.inputs[0])
    #group_input.Vertex Group -> reroute.Input
    normal_blend.links.new(group_input.outputs[2], reroute.inputs[0])
    #object_info_001.Geometry -> reroute_001.Input
    normal_blend.links.new(object_info_001.outputs[4], reroute_001.inputs[0])
    #reroute_001.Output -> reroute_002.Input
    normal_blend.links.new(reroute_001.outputs[0], reroute_002.inputs[0])
    #reroute.Output -> reroute_003.Input
    normal_blend.links.new(reroute.outputs[0], reroute_003.inputs[0])

class OBJECT_FLOPS_normal_blend(Operator):
    """Create Normal Blend Geometry Node Modifier and assign vertex group"""
    bl_idname = "object.flops_gn_normal_blend"
    bl_label = "Normal Blend Setup"
    bl_options = {'REGISTER', 'UNDO'}
    
    addon_prefs = bpy.context.preferences.addons[ADDON_NAME].preferences
    
    
    auto_disable_outline: bpy.props.BoolProperty(
        name="Auto Disable Object Outline",
        description="Automatically disable object outline for better visualization",
        default=True
    )

    def execute(self, context):
        obj = context.active_object
        node_group = normal_blend_node_group()
        
        
        try:
            addon_prefs = bpy.context.preferences.addons[ADDON_NAME].preferences
        except (KeyError, AttributeError):
            addon_prefs = None 
        
        # Set outline visibility based on user preference
        if addon_prefs.disable_outline:
            for area in context.window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D' and hasattr(space.shading, "show_object_outline"):
                            if self.auto_disable_outline and addon_prefs.disable_outline:
                                if space.shading.show_object_outline:
                                    space.shading.show_object_outline = False
                                    self.report({'WARNING'}, "Object Outline has been automatically disabled for better visualization.")
                            else:
                                if not space.shading.show_object_outline:
                                    space.shading.show_object_outline = True
                                    self.report({'INFO'}, "Object Outline has been re-enabled.")
                    break
        
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}

        selected_meshes = [o for o in context.selected_objects if o.type == 'MESH' and o != obj]
        if not selected_meshes:
            self.report({'ERROR'}, "Select at least two mesh objects (active + source)")
            return {'CANCELLED'}

        source = selected_meshes[0]

        # Create or get vertex group "__boundary"
        group_name = "__boundary"
        vertex_group = obj.vertex_groups.get(group_name)
        if vertex_group is None:
            vertex_group = obj.vertex_groups.new(name=group_name)

        # Build KDTree for source vertices in world space
        source_verts = [source.matrix_world @ v.co for v in source.data.vertices]
        kd = kdtree.KDTree(len(source_verts))
        for i, v_co in enumerate(source_verts):
            kd.insert(v_co, i)
        kd.balance()

        # Find verts in obj touching source verts (within epsilon)
        epsilon = 1e-5
        matching_verts = []
        for v in obj.data.vertices:
            v_world = obj.matrix_world @ v.co
            co, index, dist = kd.find(v_world)
            if dist < epsilon:
                matching_verts.append(v.index)

        # Assign verts to vertex group
        if matching_verts:
            vertex_group.add(matching_verts, 1.0, 'REPLACE')
        else:
            self.report({'WARNING'}, "No matching vertices found for vertex group assignment")

        # Create the Geometry Nodes modifier or get existing
        mod = obj.modifiers.get("Normal Blend Modifier")
        if mod is None:
            mod = obj.modifiers.new(name="Normal Blend Modifier", type='NODES')

        # Create or reuse the geometry node group
        normal_blend = bpy.data.node_groups.get("Normal Blend")
        if normal_blend is None:
            normal_blend = normal_blend_node_group()

        mod.node_group = normal_blend

        # Assign inputs by index: 0=Geometry, 1=Object, 2=Vertex Group
        # Set Object input to source object
        mod["Socket_2"] = source
        # Set Vertex Group input
        mod["Input_2"] = group_name

        self.report({'INFO'}, "Normal Blend setup complete")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_FLOPS_normal_blend)

def unregister():
    bpy.utils.unregister_class(OBJECT_FLOPS_normal_blend)

if __name__ == "__main__":
    register()
    # To run: select two meshes, with target active, then:
    bpy.ops.object.flops_gn_normal_blend()
