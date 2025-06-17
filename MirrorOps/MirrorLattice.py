import bpy
from bpy.props import EnumProperty, BoolProperty


class View3D_LatticeMirrorOperator(bpy.types.Operator):
    bl_idname = "object.simple_lattice_mirror"
    bl_label = "Mirror Lattice Along Axis"
    bl_description = "Mirrors a lattice's vertices along the selected axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: EnumProperty(
        name="Mirror Axis",
        description="Axis to mirror along",
        items=[
            ('X', "X Axis", "Mirror along the X axis"),
            ('Y', "Y Axis", "Mirror along the Y axis"),
            ('Z', "Z Axis", "Mirror along the Z axis"),
        ],
        default='X',
    )

    from_opposite: BoolProperty(
        name="Mirror From Opposite",
        description="Mirror points from the opposite side instead of mirroring current points (ignored if vertices are selected)",
        default=False,
    )

    def execute(self, context):
        obj = context.active_object

        if obj and obj.type == 'LATTICE' and bpy.context.mode == 'EDIT_LATTICE':
            lattice = obj.data

            u, v, w = lattice.points_u, lattice.points_v, lattice.points_w
            selected_indices = [
                idx for idx, point in enumerate(lattice.points) if point.select
            ]

            # If vertices are selected, always operate on those, ignoring "from_opposite"
            is_using_selected = bool(selected_indices)
            target_indices = selected_indices if is_using_selected else range(len(lattice.points))

            new_positions = {}

            for idx in target_indices:
                i = idx % u
                j = (idx // u) % v
                k = idx // (u * v)
                point = lattice.points[idx]

                # Determine the coordinate to mirror based on the selected axis
                coord = {'X': point.co_deform.x, 'Y': point.co_deform.y, 'Z': point.co_deform.z}[self.axis]

                # Ignore "from_opposite" if vertices are selected
                if (is_using_selected or (coord > 0 and not self.from_opposite) or (coord < 0 and self.from_opposite)):
                    mirrored_position = point.co_deform.copy()

                    # Mirror the coordinate along the selected axis
                    if self.axis == 'X':
                        mirrored_position.x *= -1
                        new_positions[(u - 1 - i, j, k)] = mirrored_position
                    elif self.axis == 'Y':
                        mirrored_position.y *= -1
                        new_positions[(i, v - 1 - j, k)] = mirrored_position
                    elif self.axis == 'Z':
                        mirrored_position.z *= -1
                        new_positions[(i, j, w - 1 - k)] = mirrored_position

            # Apply the new mirrored positions
            for (i, j, k), mirrored_position in new_positions.items():
                idx = i + j * u + k * u * v
                lattice.points[idx].co_deform = mirrored_position

            if is_using_selected:
                self.report({'INFO'}, f"Selected lattice vertices mirrored along the {self.axis}-axis.")
            else:
                self.report({'INFO'}, f"All lattice vertices mirrored along the {self.axis}-axis (from opposite: {self.from_opposite}).")
        else:
            self.report({'WARNING'}, "Please select a lattice object.")
        
        return {'FINISHED'}

class LatticeMirrorPanel(bpy.types.Panel):
    bl_label = "Simple Lattice Mirror"
    bl_idname = "OBJECT_PT_simple_lattice_mirror"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'LATTICE' and context.mode == 'EDIT_LATTICE'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        op = col.operator("object.simple_lattice_mirror", text="Mirror Lattice Along X")
        op.axis = 'X'
        op = col.operator("object.simple_lattice_mirror", text="Mirror Lattice Along Y")
        op.axis = 'Y'
        op = col.operator("object.simple_lattice_mirror", text="Mirror Lattice Along Z")
        op.axis = 'Z'
        col.prop(context.window_manager, "mirror_from_opposite", text="Mirror From Opposite")


def mirror_lattice(self, context):
    self.layout.separator()
    self.layout.label(text="FlOps")
    self.layout.operator(View3D_LatticeMirrorOperator.bl_idname, text="Mirror Lattice")


def register():
    bpy.utils.register_class(View3D_LatticeMirrorOperator)
    bpy.utils.register_class(LatticeMirrorPanel)
    bpy.types.VIEW3D_MT_edit_lattice.append(mirror_lattice)


def unregister():
    bpy.utils.unregister_class(View3D_LatticeMirrorOperator)
    bpy.utils.unregister_class(LatticeMirrorPanel)
    bpy.types.VIEW3D_MT_edit_lattice.remove(mirror_lattice)

if __name__ == "__main__":
    try:
        unregister()
    except RuntimeError:
        pass
    register()
