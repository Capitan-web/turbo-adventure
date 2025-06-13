import bpy

# === Знайти об'єкт Shell*
shell = next((obj for obj in bpy.data.objects if obj.name.startswith("Shell")), None)
if not shell:
    raise Exception("Об'єкт 'Shell*' не знайдено в сцені")

# === Очистити попередні ножі
for name in ["CutterX", "CutterY"]:
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

# === Створити різак по X (відтинає ліву половину, до X=0)
bpy.ops.mesh.primitive_cube_add(size=2, location=(-7.5, 0, 0))
cutter_x = bpy.context.active_object
cutter_x.name = "CutterX"
cutter_x.scale = (7.6, 50, 50)

# === Створити різак по Y (відтинає задню половину, до Y=0)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -7.5, 0))
cutter_y = bpy.context.active_object
cutter_y.name = "CutterY"
cutter_y.scale = (50, 7.6, 50)

# === Boolean CutterX
mod_x = shell.modifiers.new(name="CutX", type='BOOLEAN')
mod_x.object = cutter_x
mod_x.operation = 'DIFFERENCE'

# === Boolean CutterY
mod_y = shell.modifiers.new(name="CutY", type='BOOLEAN')
mod_y.object = cutter_y
mod_y.operation = 'DIFFERENCE'

# === Застосувати модифікатори
bpy.context.view_layer.objects.active = shell
bpy.ops.object.modifier_apply(modifier=mod_x.name)
bpy.ops.object.modifier_apply(modifier=mod_y.name)

# === Видалити ножі
bpy.data.objects.remove(cutter_x, do_unlink=True)
bpy.data.objects.remove(cutter_y, do_unlink=True)
