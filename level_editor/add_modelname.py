import bpy

# カスタムプロパティ 
class MYADDON_OT_add_modelname(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_modelname"
    bl_label = "モデル名称追加"
    bl_description = "['model_name']プロパティを追加"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object["model_name"] = ""

        return {"FINISHED"}