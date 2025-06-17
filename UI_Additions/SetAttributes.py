import bpy


class AttributeSetProps(bpy.types.PropertyGroup):
    attrvalue_float: bpy.props.FloatProperty(name="Float Value", default=0.0)
    attrvalue_int: bpy.props.IntProperty(name="Int Value", default=0)
    attrvalue_bool: bpy.props.BoolProperty(name="Bool Value", default=False)
    attrvalue_color: bpy.props.FloatVectorProperty(
        name="Color Value",
        subtype='COLOR',
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )


class MESH_OT_attribute_set(bpy.types.Operator):
    bl_idname = "mesh.attribute_set_operator"
    bl_label = "Set Attribute"
    bl_description = "Set the attribute using the value from the box"

    def execute(self, context):
        obj = context.object
        if not obj or not obj.data or not obj.data.attributes.active:
            self.report({'ERROR'}, "No active attribute selected")
            return {'CANCELLED'}

        attr = obj.data.attributes.active
        props = context.scene.set_attributes

        # Detect attribute type and get value
        # Need more types added
        if attr.data_type == 'FLOAT':
            value = context.scene.set_attributes.attrvalue_float
            bpy.ops.mesh.attribute_set(value_float=value)
        elif attr.data_type == 'INT':
            value = context.scene.set_attributes.attrvalue_int
            bpy.ops.mesh.attribute_set(value_int=value)
        elif attr.data_type == 'BOOLEAN':
            value = context.scene.set_attributes.attrvalue_bool
            bpy.ops.mesh.attribute_set(value_bool=value)
        elif attr.data_type == 'FLOAT_COLOR':
            value = context.scene.set_attributes.attrvalue_color
            bpy.ops.mesh.attribute_set(value_color=value)
        else:
            self.report({'ERROR'}, "Unsupported attribute type")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Set {attr.name} ({attr.data_type}) to {value}")
        return {'FINISHED'}


class DATA_PT_set_attributes(bpy.types.Panel):
    bl_label = "My Attributes"
    bl_idname = "DATA_PT_set_attributes"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "mesh"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if not obj or not obj.data or not obj.data.attributes.active:
            layout.label(text="Select an attribute")
            return
        
        layout.label(text="Set Attributes")
        
        attr = obj.data.attributes.active
        props = context.scene.set_attributes
        
        row = layout.row(align=True)
        if attr.data_type == 'FLOAT':
            row.prop(props, "attrvalue_float", text="")
        elif attr.data_type == 'INT':
            row.prop(props, "attrvalue_int", text="")
        elif attr.data_type == 'BOOLEAN':
            row.prop(props, "attrvalue_bool", text="")
        elif attr.data_type == 'FLOAT_COLOR':
            row.prop(props, "attrvalue_color", text="")    
        row.operator("mesh.attribute_set_operator", text="Set")


classes = [AttributeSetProps, MESH_OT_attribute_set, DATA_PT_set_attributes]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.set_attributes = bpy.props.PointerProperty(type=AttributeSetProps)

    # Append to the existing Mesh Attributes panel
    bpy.types.DATA_PT_mesh_attributes.append(DATA_PT_set_attributes.draw)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.set_attributes

    # Remove from Mesh Attributes panel
    bpy.types.DATA_PT_mesh_attributes.remove(DATA_PT_set_attributes.draw)


if __name__ == "__main__":
    register()
