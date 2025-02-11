import bpy

# インフォクラス
bl_info = {
    "name": "level_editor",
    "author": "Yuto Isogai",
    "version": (1, 0),
    "blender": (4, 1),
    "location": "",
    "description": "level_editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# モジュールインポート
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .export_scene import MYADDON_OT_export_scene
from .add_modelname import MYADDON_OT_add_modelname
from .model_name import OBJECT_PT_model_name
from .add_collider import MYADDON_OT_add_collider
from .collider import OBJECT_PT_collider
from .draw_collider import DrawCollider
from .disabled import MYADDON_OT_add_disabled
from .disabled import OBJECT_PT_disabled
from .spawn import MYADDON_OT_spawn_import_symbol
from .spawn import MYADDON_OT_spawn_create_symbol
from .spawn import MYADDON_OT_spawn_create_player_symbol
from .spawn import MYADDON_OT_spawn_create_player_symbol_menu
from .spawn import MYADDON_OT_spawn_create_enemy_symbol
from .spawn import MYADDON_OT_spawn_create_enemy_symbol_menu

# メニュー項目
def draw_menu_manual(self,context):
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

# トップバー拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "Mymenu"
    bl_description = "拡張メニュー by" + bl_info["author"]

    # サブメニューの描画
    def draw(self,context):
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text = MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text = MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)
        self.layout.menu(MYADDON_OT_spawn_create_player_symbol_menu.bl_idname,text=MYADDON_OT_spawn_create_player_symbol_menu.bl_label)
        self.layout.menu(MYADDON_OT_spawn_create_enemy_symbol_menu.bl_idname,text=MYADDON_OT_spawn_create_enemy_symbol_menu.bl_label)

    # 既存のメニューにサブメニューを追加
    def submenu(self,context):
        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_modelname,
    OBJECT_PT_model_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    MYADDON_OT_add_disabled,
    OBJECT_PT_disabled,
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
    MYADDON_OT_spawn_create_player_symbol,
    MYADDON_OT_spawn_create_player_symbol_menu,
    MYADDON_OT_spawn_create_enemy_symbol,
    MYADDON_OT_spawn_create_enemy_symbol_menu
)

# Add-On有効化時コールバック
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューから項目の追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")
    print("レベルエディタが有効化されました")

# Add-On無効化時コールバック
def unregister():
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    # メニューから項目の削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました")

# テスト サンプルコード
if __name__ == "__main__":
    register()