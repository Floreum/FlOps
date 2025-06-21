import bpy

# Handles All menu additions for the addon

# Adds a separator to the Mask menu
def flops_mask_menu(self, context):
    self.layout.separator()
    self.layout.label(text="FlOps")
    
    self.layout.operator("sculpt.selected_vert_mask_tool", text="Mask From Edit Mode Selection")
    self.layout.operator("sculpt.face_set_from_vert_groups", text="Vertex Groups from Face Sets")
    self.layout.operator("sculpt.weights_to_face_sets", text="Weights to Face Sets")


class MESH_FLOPS_vertex_groups(bpy.types.Menu):
    bl_label = "FlOps Vertex Groups"
    bl_idname = "MESH_MT_FLOPS_vertex_groups"

    def draw(self, context):
        layout = self.layout
        layout.operator("sculpt.face_set_from_vert_groups", text="Vertex Groups from Face Sets")
        layout.operator("sculpt.weights_to_face_sets", text="Weights to Face Sets")
        layout.operator("mesh.select_boundary_blend", text="Blend Boundary Normals")
    
def flops_vertex_groups_menu(self, context):
    self.layout.menu(MESH_FLOPS_vertex_groups.bl_idname)
    
def flops_make_links_menu(self, context):
    self.layout.separator()
    self.layout.label(text="FlOps")
    self.layout.operator("mesh.select_boundary_blend", text="Blend Boundary Normals")

def flops_make_single_user_menu(self, context):
    self.layout.separator()
    self.layout.label(text="FlOps")
    self.layout.operator("mesh.select_boundary_blend", text="Blend Boundary Normals")

_is_registered = False

def register():
    global _is_registered
    bpy.types.VIEW3D_MT_mask.append(flops_mask_menu)
    bpy.types.MESH_MT_vertex_group_context_menu.append(flops_vertex_groups_menu)
    bpy.types.VIEW3D_MT_make_single_user.append(flops_make_single_user_menu)
    bpy.types.VIEW3D_MT_make_links.append(flops_make_links_menu)
    bpy.utils.register_class(MESH_FLOPS_vertex_groups)
    _is_registered = True

def unregister():
    global _is_registered
    bpy.types.VIEW3D_MT_mask.remove(flops_mask_menu)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(flops_vertex_groups_menu)
    bpy.types.VIEW3D_MT_make_single_user.remove(flops_make_single_user_menu)
    bpy.types.VIEW3D_MT_make_links.remove(flops_make_links_menu)
    bpy.utils.unregister_class(MESH_FLOPS_vertex_groups)
    _is_registered = False
