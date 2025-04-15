import bpy
from bpy_extras import view3d_utils
import gpu
from gpu_extras.batch import batch_for_shader
import math
import time
from mathutils import Vector
import threading

transfer_mode_wp = []

def flash_object(context, obj, duration=0.2, color=(1.0, 0.5, 0.0, 1.0), steps=10):
    """Flash an overlay on the object to indicate a swap."""
    if not obj or obj.type != 'MESH':
        return

    # Temporarily disable all modifiers except the armature modifier to improve performance
    original_modifier_states = {}
    for modifier in obj.modifiers:
        if modifier.type in {'ARMATURE', 'CORRECTIVE_SMOOTH', 'LATTICE'}:
            original_modifier_states[modifier.name] = modifier.show_viewport
        else:
            original_modifier_states[modifier.name] = modifier.show_viewport
            modifier.show_viewport = False

    # Use the evaluated mesh with only the allowed modifiers applied
    depsgraph = context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()

    # Get the world-space coordinates of the mesh vertices and create edges for the wireframe
    vertices = [obj.matrix_world @ v.co for v in mesh.vertices]
    edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]

    # Restore the original modifier states
    for modifier_name, state in original_modifier_states.items():
        obj.modifiers[modifier_name].show_viewport = state

    # Create a shader for drawing the wireframe
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=edges)

    # Fade effect variables
    fade_step = 0
    fade_in = True
    handler = None

    def draw_callback():
        """Draw the object's wireframe with a fading effect."""
        nonlocal fade_step, fade_in

        # Calculate the fade factor
        factor = fade_step / steps if fade_in else (1 - fade_step / steps)
        fade_color = (color[0], color[1], color[2], factor)  # Adjust alpha (transparency)

        # Draw the wireframe
        shader.bind()
        shader.uniform_float("color", fade_color)
        batch.draw(shader)

    # Add the draw callback to the viewport
    handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback, (), 'WINDOW', 'POST_VIEW')

    # Timer to update fade steps
    def update_fade():
        nonlocal fade_step, fade_in, handler

        fade_step += 1 if fade_in else -1

        # Stop the effect after one full fade-in and fade-out cycle
        if fade_step > steps:
            fade_in = False
        elif fade_step < 0:
            # Remove the draw handler and stop the effect
            if handler:
                bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
                handler = None

            # Force a final redraw of all 3D Viewport areas
            for area in context.window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

            # Clean up the evaluated mesh
            eval_obj.to_mesh_clear()
            return None  # Stop the timer

        # Force a redraw of all 3D Viewport areas
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return duration / steps

    # Start the fade effect
    bpy.app.timers.register(update_fade)

class OBJECT_OT_swap_weight_paint(bpy.types.Operator):
    """Swap Mesh in Weight Paint Mode while preserving the selected pose bone and activating the matching vertex group"""
    bl_idname = "object.transfer_mesh_weight_paint"
    bl_label = "Swap Weight Paint Mesh"
    bl_options = {'UNDO'}

    # Store mouse coordinates from the invoke event
    mouse_x: bpy.props.IntProperty()
    mouse_y: bpy.props.IntProperty()

    def invoke(self, context, event):
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y
        return self.execute(context)

    def get_object_under_mouse(self, context):
        """Ray-cast from mouse coordinates to find a mesh under the mouse"""
        region = context.region
        rv3d = context.region_data
        coord = (self.mouse_x, self.mouse_y)
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        view_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        depsgraph = context.evaluated_depsgraph_get()
        hit, location, normal, index, obj, matrix = context.scene.ray_cast(depsgraph, view_origin, view_vector)
        return obj if hit else None

    def execute(self, context):
        # Ensure the active object is a mesh in weight paint mode.
        if not (context.active_object and context.active_object.mode == 'WEIGHT_PAINT'):
            self.report({'WARNING'}, "Active object must be a mesh in Weight Paint mode")
            return {'CANCELLED'}

        # Store the currently active (weight painted) mesh.
        active_mesh = context.active_object

        # Find the armature in the selection
        armature = None
        for obj in context.selected_objects:
            if obj.type == 'ARMATURE':
                armature = obj
                break
        if armature is None:
            self.report({'WARNING'}, "No armature selected")
            return {'CANCELLED'}

        # Temporarily switch active object to the armature so we can read its selected pose bones.
        original_active = context.active_object
        context.view_layer.objects.active = armature
        selected_pose_bones = bpy.context.selected_pose_bones_from_active_object

        if not (selected_pose_bones and len(selected_pose_bones) > 0):
            self.report({'WARNING'}, "No selected pose bone found on the armature")
            # Restore the original active object.
            context.view_layer.objects.active = original_active
            return {'CANCELLED'}
        # Use the first selected pose bone.
        selected_bone_name = selected_pose_bones[0].name

        # Restore the original active object (the mesh) for now.
        context.view_layer.objects.active = active_mesh

        # Ray-cast to find the target mesh under the mouse.
        new_mesh = self.get_object_under_mouse(context)
        if new_mesh is None or new_mesh.type != 'MESH':
            self.report({'WARNING'}, "No valid mesh under the mouse")
            return {'CANCELLED'}

        # --- Swap the mesh ---
        # Switch to Object mode so we can change selections.
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # Select the new mesh and also re-select the armature.
        new_mesh.select_set(True)
        armature.select_set(True)
        context.view_layer.objects.active = new_mesh

        # Switch back to Weight Paint mode on the new mesh.
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

        # --- Activate the vertex group on the new mesh matching the selected pose bone ---
        # Check if the new mesh has a vertex group with the same name.
        vg = new_mesh.vertex_groups.get(selected_bone_name)
        if vg:
            new_mesh.vertex_groups.active = vg
        else:
            active_vg_name = new_mesh.vertex_groups.active.name if new_mesh.vertex_groups.active else "None"
            self.report({'WARNING'}, f"Vertex group '{selected_bone_name}' not found in the mesh: '{new_mesh.name}'... Displaying: '{active_vg_name}'.")

        # Flash the new mesh to indicate the swap
        flash_object(context, new_mesh)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_swap_weight_paint)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        # Find or create the Weight Paint mode keymap
        km = kc.keymaps.new(name='Weight Paint', space_type='EMPTY')
        # Create a new keymap item for Alt+Q
        kmi = km.keymap_items.new(
            OBJECT_OT_swap_weight_paint.bl_idname,
            type='Q',
            value='PRESS',
            alt=True
        )
        transfer_mode_wp.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_swap_weight_paint)

    # Remove keymap entry
    for km, kmi in transfer_mode_wp:
        km.keymap_items.remove(kmi)
    transfer_mode_wp.clear()