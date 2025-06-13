import bpy

obj = bpy.context.active_object
modifier = obj.modifiers.new(name="QuarterCut", type='BOOLEAN')

# Створення об'єкта для вирізання
bpy.ops.mesh.primitive_cube_add(size=2, location=(1, 1, 0))
cutter = bpy.context.object
cutter.scale = (5, 5, 5)
cutter.location = (10, 10, 0)
cutter.name = "QuarterCutter"

modifier.object = cutter
modifier.operation = 'DIFFERENCE'
