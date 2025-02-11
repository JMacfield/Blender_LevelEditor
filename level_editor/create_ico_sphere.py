import bpy

# オペレータ ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_ico_sphere"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitives_ico_sphere_add()
        
        print("ICO球を生成しました")

        return {"FINISHED"}