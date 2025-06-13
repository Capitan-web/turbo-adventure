import bpy

target_color = (1.0, 0.0, 0.0, 1.0)  # червоний
apply_to_selected = True

if apply_to_selected:
    objects = bpy.context.selected_objects
else:
    objects = bpy.data.objects

mat = bpy.data.materials.new(name="ColorMaterial")
mat.diffuse_color = target_color

for obj in objects:
    if obj.type == 'MESH':
        if not obj.data.materials:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat
