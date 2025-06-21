import bpy

class OBJECT_OT_VertexColorSelection(bpy.types.Operator):
    """Assign colors based on vertex selection order"""
    bl_idname = "object.vertex_color_selection"
    bl_label = "Vertex Color Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.assign_vertex_colors()  # Call with self
        return {'FINISHED'}

    def assign_vertex_colors(self):
        obj = bpy.context.object
        mesh = obj.data
        
        # Ensure we are in Object Mode
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create or use existing vertex color layer
        if not mesh.vertex_colors:
            color_layer = mesh.vertex_colors.new(name="z9-MergeAtFirst")
        else:
            color_layer = mesh.vertex_colors.active

        # Clear previous colors
        for loop in color_layer.data:
            loop.color = (0, 0, 0, 1)  # Set default to black

        # Get selected vertices
        selected_verts = [v for v in mesh.vertices if v.select]
        if len(selected_verts) < 2:
            self.report({'WARNING'}, "Select at least two vertices")
            return

        # Color mapping based on vertex order
        color_map = {}
        num_verts = len(selected_verts)
        for i, vert in enumerate(selected_verts):
            color = (0, 1, 0, 1)  # Default green
            if i == 0:
                color = (0, 0, 1, 1)  # Blue for first vertex
            elif i == num_verts - 1:
                color = (1, 0, 0, 1)  # Red for last vertex
            color_map[vert.index] = color

        # Assign colors to loops
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                loop = mesh.loops[loop_index]
                vert_index = loop.vertex_index
                if vert_index in color_map:
                    color_layer.data[loop_index].color = color_map[vert_index]

        # Update mesh
        mesh.update()

def register():
    bpy.utils.register_class(OBJECT_OT_VertexColorSelection)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_VertexColorSelection)

if __name__ == "__main__":
    register()