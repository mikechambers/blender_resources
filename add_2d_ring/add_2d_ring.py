'''
Blender addon based on code created by batFINGER from:
https://blender.stackexchange.com/a/146097/65093

Creates a 2D circle with an inner radius.
'''

bl_info = {
    "name": "2D Ring",
    "author": "batFINGER",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > 2D Ring",
    "description": "Adds a 2D ring (circle with hole)",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}
import bpy
import bmesh
from mathutils import Matrix
from math import asin
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)


class MESH_OT_primitive_ring_add(AddObjectHelper, bpy.types.Operator):
    """Add a 2D filled ring mesh"""
    bl_idname = "mesh.primitive_ring_add"
    bl_label = "2D Ring"
    bl_options = {'REGISTER', 'UNDO'}

    outer_radius: FloatProperty(
        name="Outer Radius",
        description="Outer Radius",
        min=0,
        default=2.0,
    )

    inner_radius: FloatProperty(
        name="Inner Radius",
        description="Inner Radius",
        min=0,
        default=1.0,
    )

    segments: IntProperty(
        name="Segments",
        description="Number of Segments",
        min=3,
        default=8,
    )

    fill_types: EnumProperty(
        items=(
            ("QUADS", "Quads", ""),
            ("NGON", "Ngon", ""),
            ("NONE", "None", "")
            ),
        name="Fill Type",
        description="Type of geometry for face."
    )

    def execute(self, context):

        me = bpy.data.meshes.new("2DRing")

        bm = bmesh.new()
        bmesh.ops.create_circle(bm, radius=self.inner_radius, segments=self.segments)
        bmesh.ops.create_circle(bm, radius=self.outer_radius, segments=self.segments)

        if self.fill_types != "NONE":

            ret = bmesh.ops.bridge_loops(bm, edges=bm.edges)

            if self.fill_types == "NGON":
                edges = ret['edges']
                e = edges.pop()
                bmesh.ops.split_edges(bm, edges=[e])
                bmesh.ops.dissolve_edges(bm,
                                         edges=edges)

        bm.to_mesh(me)
        me.update()

        from bpy_extras import object_utils
        object_utils.object_data_add(context, me, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_primitive_ring_add.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(MESH_OT_primitive_ring_add)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_primitive_ring_add)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.primitive_ring_add()