import bpy

# Add a custom float property to the Scene
bpy.types.Scene.my_float_value = bpy.props.FloatProperty(
    name="Value",
    default=0.0,
    description="Float value to set attribute"
)

# Create an operator that calls the mesh.attribute_set operator with the value from the scene
class MESH_OT_attribute_set(bpy.types.Operator):
    bl_idname = "mesh.attribute_set_operator"
    bl_label = "Set Attribute"
    bl_description = "Set the attribute using the value from the box"

    def execute(self, context):
        value = context.scene.my_float_value
        # Call the attribute_set operator with the float value.
        # (Make sure that bpy.ops.mesh.attribute_set exists in your Blender version.)
        bpy.ops.mesh.attribute_set(value_float=value)
        self.report({'INFO'}, f"Attribute set with value: {value}")
        return {'FINISHED'}

# Create a panel in the Data properties (Attributes) context
class DATA_PT_my_attributes(bpy.types.Panel):
    bl_label = "My Attributes"
    bl_idname = "DATA_PT_my_attributes"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "mesh"  # This places the panel in the Data (object/data) context

    def draw(self, context):
        layout = self.layout

        # Place the float box and the button on the same row.
        layout.label(text="Set Attributes")
        row = layout.row(align=True)
        row.prop(context.scene, "my_float_value", text="")
        row.operator("mesh.attribute_set_operator", text="Set")

# Registration
classes = [MESH_OT_attribute_set, DATA_PT_my_attributes]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.DATA_PT_mesh_attributes.append(DATA_PT_my_attributes.draw)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_float_value
    bpy.types.DATA_PT_mesh_attributes.remove(DATA_PT_my_attributes.draw)

if __name__ == "__main__":
    register()
