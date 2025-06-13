import bpy
import bmesh
import math

# Створення основної гільзи
mesh = bpy.data.meshes.new("Shell")
obj = bpy.data.objects.new("Shell", mesh)
bpy.context.collection.objects.link(obj)
bm = bmesh.new()

bmesh.ops.create_cone(bm,
    cap_ends=True,
    cap_tris=False,
    segments=64,
    radius1=14,
    radius2=14,
    depth=70
)

bm.to_mesh(mesh)
bm.free()

# Фаска
bevel = bpy.data.objects.new("BevelGuide", bpy.data.meshes.new("BevelMesh"))
bpy.context.collection.objects.link(bevel)
bpy.context.view_layer.objects.active = bevel
bpy.ops.object.select_all(action='DESELECT')
bevel.select_set(True)
bpy.context.view_layer.objects.active = bevel
bpy.ops.object.modifier_add(type='BEVEL')
bevel.modifiers["Bevel"].width = 4
bevel.modifiers["Bevel"].segments = 4

# Додаємо cavity (внутрішній отвір)
bpy.ops.mesh.primitive_cylinder_add(radius=10.5, depth=70, location=(0, 0, 0))
cavity = bpy.context.object
cavity.name = "Cavity"

# Додаємо step cone
bpy.ops.mesh.primitive_cone_add(radius1=8, radius2=6, depth=8, location=(0, 0, 31))
step_cone = bpy.context.object
step_cone.name = "StepCone"

# Boolean вирізи
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_add(type='BOOLEAN')
obj.modifiers["Boolean"].object = cavity
obj.modifiers["Boolean"].operation = 'DIFFERENCE'

bpy.ops.object.modifier_add(type='BOOLEAN')
obj.modifiers["Boolean.001"].object = step_cone
obj.modifiers["Boolean.001"].operation = 'DIFFERENCE'
