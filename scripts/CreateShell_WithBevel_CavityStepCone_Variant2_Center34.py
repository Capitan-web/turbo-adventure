import bpy
import bmesh

# Очистити сцену
for obj in bpy.data.objects:
    obj.select_set(True)
bpy.ops.object.delete()

# === Shell (Ø25×80 мм) ===
shell_mesh = bpy.data.meshes.new("Shell")
shell_obj = bpy.data.objects.new("Shell", shell_mesh)
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
bm.to_mesh(shell_mesh)
bm.free()
shell_obj.location = (0, 0, 0)

# === Cavity (Ø21×70 мм), центр = -5 мм ===
bpy.ops.mesh.primitive_cylinder_add(
    radius=10.5,
    depth=70,
    location=(0, 0, -5)
)
cavity = bpy.context.object
cavity.name = "Cavity"

# === StepCone (Ø16 → Ø12, 8 мм), центр = Z = 34
bpy.ops.mesh.primitive_cone_add(
    radius1=8,
    radius2=6,
    depth=8,
    location=(0, 0, 34)
)
step_cone = bpy.context.object
step_cone.name = "StepCone"

# === Boolean: Cavity → Shell
bpy.context.view_layer.objects.active = shell_obj
bpy.ops.object.modifier_add(type='BOOLEAN')
mod1 = shell_obj.modifiers[-1]
mod1.name = "CavityCut"
mod1.object = cavity
mod1.operation = 'DIFFERENCE'

# === Boolean: StepCone → Shell
bpy.ops.object.modifier_add(type='BOOLEAN')
mod2 = shell_obj.modifiers[-1]
mod2.name = "StepConeCut"
mod2.object = step_cone
mod2.operation = 'DIFFERENCE'

# === Застосувати модифікатори
bpy.ops.object.select_all(action='DESELECT')
shell_obj.select_set(True)
bpy.context.view_layer.objects.active = shell_obj
bpy.ops.object.convert(target='MESH')
