import bpy

from .add_collider import MYADDON_OT_add_collider

# パネルコライダー
class OBJECT_PT_collider(bpy.types.Panel):
    """オブジェクトのコライダーパネル"""
    bl_idname = "OBJECT_PT_collider"
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # サブメニュー
    def draw(self, context):
        if "collider" in context.object:
            self.layout.prop(context.object.collider_type, "my_menu")
            self.layout.prop(context.object, '["collider_center"]', text = "Center")
            self.layout.prop(context.object, '["collider_size"]', text = "Size")
        else:
            self.layout.operator(MYADDON_OT_add_collider.bl_idname)