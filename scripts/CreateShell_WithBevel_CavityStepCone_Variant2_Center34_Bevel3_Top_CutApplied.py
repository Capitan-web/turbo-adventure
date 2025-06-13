import bpy
import bmesh

# Очистити попередні об'єкти
for obj in bpy.data.objects:
    if obj.name in ["Shell", "Cavity", "StepCone"]:
        bpy.data.objects.remove(obj, do_unlink=True)

# === Shell (Ø25×80 мм) ===
mesh = bpy.data.meshes.new("Shell")
shell_obj = bpy.data.objects.new("Shell", mesh)
bpy.context.collection.objects.link(shell_obj)

bm = bmesh.new()
bmesh.ops.create_cone(
    bm,
    cap_ends=True,
    cap_tris=False,
    segments=64,
    radius1=12.5,
    radius2=12.5,
    depth=80
)
bm.to_mesh(mesh)
bm.free()
shell_obj.location = (0, 0, 0)

# === Vertex Group для верхнього торця
bpy.context.view_layer.objects.active = shell_obj
vg = shell_obj.vertex_groups.new(name="TopEdge")
for i, v in enumerate(shell_obj.data.vertices):
    if v.co.z > 39.9:
        vg.add([i], 1.0, 'ADD')

# === Bevel по верхньому торцю
bevel = shell_obj.modifiers.new(name="TopBevel", type='BEVEL')
bevel.width = 3
bevel.segments = 4
bevel.limit_method = 'VGROUP'
bevel.vertex_group = "TopEdge"

# === Створення Cavity
cavity_mesh = bpy.data.meshes.new("Cavity")
cavity = bpy.data.objects.new("Cavity", cavity_mesh)
bpy.context.collection.objects.link(cavity)

bm = bmesh.new()
bmesh.ops.create_cone(
    bm,
    cap_ends=True,
    cap_tris=False,
    segments=64,
    radius1=10.5,
    radius2=10.5,
    depth=70
)
bm.to_mesh(cavity_mesh)
bm.free()
cavity.location = (0, 0, -5)

# === Створення StepCone
stepcone_mesh = bpy.data.meshes.new("StepCone")
step_cone = bpy.data.objects.new("StepCone", stepcone_mesh)
bpy.context.collection.objects.link(step_cone)

bm = bmesh.new()
bmesh.ops.create_cone(
    bm,
    cap_ends=True,
    cap_tris=False,
    segments=64,
    radius1=8,
    radius2=6,
    depth=8
)
bm.to_mesh(stepcone_mesh)
bm.free()
step_cone.location = (0, 0, 34)

# === Boolean вирізання
bpy.context.view_layer.objects.active = shell_obj

mod1 = shell_obj.modifiers.new(name="CavityCut", type='BOOLEAN')
mod1.object = cavity
mod1.operation = 'DIFFERENCE'

mod2 = shell_obj.modifiers.new(name="StepConeCut", type='BOOLEAN')
mod2.object = step_cone
mod2.operation = 'DIFFERENCE'

# === Застосувати всі модифікатори
bpy.ops.object.select_all(action='DESELECT')
shell_obj.select_set(True)
bpy.context.view_layer.objects.active = shell_obj
bpy.ops.object.convert(target='MESH')

# === Видалити об'єкти вирізання
bpy.data.objects.remove(cavity, do_unlink=True)
bpy.data.objects.remove(step_cone, do_unlink=True)
