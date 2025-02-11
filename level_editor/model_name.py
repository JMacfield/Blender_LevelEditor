import bpy

from .add_modelname import MYADDON_OT_add_modelname

class OBJECT_PT_model_name(bpy.types.Panel):
    """オブジェクトのファイル　ネームパネル"""
    bl_idname = "OBJECT_PT_model_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        if "model_name" in context.object:
            self.layout.prop(context.object, '["model_name"]', text = self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_modelname.bl_idname)