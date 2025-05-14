import bpy
import blf
import bgl
import time
import gpu
from gpu_extras.batch import batch_for_shader


class SCULPT_OT_Weights2FaceSets(bpy.types.Operator):
    """Assign face sets based on vertex groups"""
    bl_idname = "sculpt.weights_to_face_sets"
    bl_label = "Weights to Face Sets"
    bl_options = {'REGISTER', 'UNDO'}

    _draw_handler = None
    _font_id = 0  # Default font ID
    _start_time = None

    def execute(self, context):
        # Add the draw handler to display the text
        self.add_draw_handler(context)

        # Record the start time
        self._start_time = time.time()

        # Switch to modal mode
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # Wait for 1 second before running the operation
        if time.time() - self._start_time > 1.0:
            # Perform the operation
            self.vertex_group_to_face_sets(context.active_object)

            # Remove the draw handler after the operation
            self.remove_draw_handler(context)

            # Send an alert to the user
            self.report({'INFO'}, "Weights to Face Set Complete!")

            return {'FINISHED'}

        # Keep the modal operator running
        return {'RUNNING_MODAL'}

    def vertex_group_to_face_sets(self, obj):
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object selected.")
            return

        mesh = obj.data

        # Ensure we are in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create the face set attribute if it doesn't exist
        attr_name = ".sculpt_face_set"
        if attr_name not in mesh.attributes:
            mesh.attributes.new(name=attr_name, type='INT', domain='FACE')

        face_set_data = mesh.attributes[attr_name].data

        # Clear existing face set values
        for item in face_set_data:
            item.value = 0

        # Build a map of vertex group index -> set of vertex indices
        vg_verts = {}
        for vgroup in obj.vertex_groups:
            verts_in_group = set()
            for v in mesh.vertices:
                for g in v.groups:
                    if g.group == vgroup.index:
                        verts_in_group.add(v.index)
            vg_verts[vgroup.index] = verts_in_group

        # Assign unique face set IDs to faces based on vertex groups
        face_set_index = 1
        for vgroup in obj.vertex_groups:
            verts_in_group = vg_verts[vgroup.index]
            for face in mesh.polygons:
                if all(v in verts_in_group for v in face.vertices):
                    face_set_data[face.index].value = face_set_index
            face_set_index += 1

        mesh.update()
        bpy.ops.object.mode_set(mode='SCULPT')
        print("Face sets created from vertex groups.")

    def draw_text_callback(self, context):
        """Draw text in the 3D Viewport with a background box."""
        region = context.region
        width = region.width
        height = region.height

        # Text properties
        text = "Face set to vertex group transfer in progress, please wait."
        text_width =530  # Approximate width of the text
        text_height = 30  # Approximate height of the text
        box_padding = 10  # Padding around the text

        # Calculate box dimensions
        box_x = width / 2 - text_width / 2 - box_padding
        box_y = height / 2 - text_height / 2 - box_padding
        box_width = text_width + 2 * box_padding
        box_height = text_height + 2 * box_padding

        # Draw the background box
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')  # Corrected shader type
        vertices = [
            (box_x, box_y),
            (box_x + box_width, box_y),
            (box_x + box_width, box_y + box_height),
            (box_x, box_y + box_height),
        ]
        indices = [(0, 1, 2), (2, 3, 0)]
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

        shader.bind()
        shader.uniform_float("color", (0.0, 0.0, 0.0, 0.4))  # Black with 50% transparency
        batch.draw(shader)

        # Set text color to light green
        blf.color(self._font_id, 0.5, 1.0, 0.5, 1.0)  # RGBA: Light green with full opacity

        # Draw the text
        blf.position(self._font_id, width / 2 - text_width / 2, height / 2 - text_height / 2, 0)
        blf.size(self._font_id, 20)
        blf.draw(self._font_id, text)

    def add_draw_handler(self, context):
        """Add the draw handler to display text."""
        if self._draw_handler is None:
            self._draw_handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_text_callback, (context,), 'WINDOW', 'POST_PIXEL'
            )
        # Force redraw of all areas in the current window
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

    def remove_draw_handler(self, context):
        """Remove the draw handler."""
        if self._draw_handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self._draw_handler, 'WINDOW')
            self._draw_handler = None
        # Force redraw of all areas in the current window
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()



def register():
    bpy.utils.register_class(SCULPT_OT_Weights2FaceSets)

def unregister():
    bpy.utils.unregister_class(SCULPT_OT_Weights2FaceSets)



if __name__ == "__main__":
    register()