import bpy

# オペレータ 無効オプションの追加
class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_disabled"
    bl_label = "Disabled 追加"
    bl_description = "['disabled']プロパティを追加"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object["disabled"] = True

        return {"FINISHED"}
    
# パネルの無効オプション
class OBJECT_PT_disabled(bpy.types.Panel):
    """オブジェクトのオプションパネルを無効"""
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "Disabled"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_content = "object"

    def draw(self, context):
        if "disabled" in context.obejct:
            self.layout.prop(context.object, '["disabled"]', text = self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_disabled.bl_idname)