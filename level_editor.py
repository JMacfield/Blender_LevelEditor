import bpy
import bpy_extras
import copy
import json
import gpu
import gpu_extras.batch
from gpu_extras.batch import batch_for_shader
import math
import mathutils

# インフォクラス
bl_info = {
    "name": "level_editor",
    "author": "Yuto Isogai",
    "version": (1, 0),
    "blender": (3, 5),
    "location": "",
    "description": "level_editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# メニュー選択画面
# オペレーター 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    bl_options = {'REGISTER','UNDO'}

    # コールバック関数
    def execute(self,context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました")

        # オペレーターの命令終了を通知
        return{'FINISHED'}

# オペレーター ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_cbject"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER','UNDO'}

    # コールバック関数
    def execute(self,context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        return{'FINISHED'}


# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "Mymenu"
    bl_description = "拡張メニュー by" + bl_info["author"]

    # サブメニューの描画
    def draw(self,context):
        # トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text = MYADDON_OT_stretch_vertex.bl_label)

        # トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
            text = MYADDON_OT_create_ico_sphere.bl_label)


    # 既存のメニューにサブメニューを追加
    def submenu(self,context):
        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


# オペレーター シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をエクスポートします"
    filename_ext = ".json"

    def parse_scene_recursive_json(self, data_parent, object, level):
        json_object = dict()
        json_object["type"] = object.type
        json_object["name"] = object.name

        ##AAA
        trans, rot, scale = object.matrix_local.decompose()
        rot = rot.to_euler()
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        transform = dict()
        transform["translation"] = (trans.x,trans.y,trans.z)
        transform["rotation"] = (rot.x,rot.y,rot.z)
        transform["scaling"] = (scale.x,scale.y,scale.z)
        json_object["transform"] = transform

        if "file_name" in object:
            json_object["file_name"] = object["file_name"]
        if "collider" in object:
            collider = dict()
            collider["type"] = object["collider"]
            collider["center"] = object["collider_center"].to_list()
            collider["size"] = object["collider_size"].to_list()
            json_object["collider"] = collider

        data_parent.append(json_object)
        
        if len(object.children)>0:
            json_object["children"]=list()
            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"],child,level+1)

    def export_json(self):
        """JSON形式でファイルに出力"""
        json_object_root = dict()
        json_object_root["name"] = "scene"
        json_object_root["objects"] = list()
    
        for obj in bpy.context.scene.objects:
            if obj.parent:
                continue
            self.parse_scene_recursive_json(json_object_root["objects"], obj, 0)
    
        json_text = json.dumps(json_object_root, ensure_ascii=False,cls=json.JSONEncoder, indent=4)
        print(json_text)
    
        with open(self.filepath, "wt", encoding="utf-8") as file:
            file.write(json_text)

    def execute(self, context):
        print("シーン情報をエクスポートします")
        for obj in bpy.context.scene.objects:
            print(f"{obj.type} - {obj.name}")
            trans, rot, scale = obj.matrix_local.decompose()
            rot = rot.to_euler()
            rot.x = math.degrees(rot.x)
            rot.y = math.degrees(rot.y)
            rot.z = math.degrees(rot.z)
            print(f"Trans({trans.x:.6f}, {trans.y:.6f}, {trans.z:.6f})")
            print(f"Rot({rot.x:.6f}, {rot.y:.6f}, {rot.z:.6f})")
            print(f"Scale({scale.x:.6f}, {scale.y:.6f}, {scale.z:.6f})")
            if obj.parent:
                print(f"Parent: {obj.parent.name}")
            print()

        self.export_json()
        print("シーン情報をエクスポートしました")
        self.report({'INFO'}, "シーン情報をエクスポートしました")
        return {'FINISHED'}

    def export(self):
        """ファイルに出力"""
        print(f"シーン情報出力開始... {self.filepath!r}")
        with open(self.filepath, "wt") as file:
            file.write("SCENE\n")
            for obj in bpy.context.scene.objects:
                if obj.parent:
                    continue
                self.parse_scene_recursive(file, obj, 0)

    def write_and_print(self, file, string):
        print(string)
        file.write(string + '\n')

    def parse_scene_recursive(self, file, obj, level):
        """シーン解析用再帰関数"""
        indent = '\t' * level
        self.write_and_print(file, indent + obj.type)
        trans, rot, scale = obj.matrix_local.decompose()
        rot = rot.to_euler()
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        self.write_and_print(file, indent + "T %f %f %f" % (trans.x, trans.y, trans.z))
        self.write_and_print(file, indent + "R %f %f %f" % (rot.x, rot.y, rot.z))
        self.write_and_print(file, indent + "S %f %f %f" % (scale.x, scale.y, scale.z))

        if "file_name" in obj:
            self.write_and_print(file, indent + "N %s" % obj["file_name"])
            #####
        if "collider" in obj:
            self.write_and_print(file, indent + "C %s" % obj["collider"])
            temp_str = indent + "CC %f %f %f"
            temp_str %= (obj["collider_center"][0], obj["collider_center"][1], obj["collider_center"][2])
            self.write_and_print(file, temp_str)
            temp_str = indent + "CS %f %f %f"
            temp_str %= (obj["collider_size"][0], obj["collider_size"][1], obj["collider_size"][2])
            self.write_and_print(file, temp_str)

        
        self.write_and_print(file, indent + 'END')
        self.write_and_print(file, '')

        for child in obj.children:
            self.parse_scene_recursive(file, child, level + 1)

    
# オペレータ カスタムプロパティ
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    
    bl_description = "['file_name'] カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # カスタムプロパティを追加
        context.object["file_name"] = ""

        return {"FINISHED"}

# パネルファイル
class OBJECT_PT_file_name(bpy.types.Panel):
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # サブメニュー
    def draw(self, context):
        # パネルに項目を追加
        if "file_name" in context.object:
            self.layout.prop(context.object, '["file_name"]', text=self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)
    
# オペレータ カスタムプロパティ
class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName 追加"
    
    bl_description = "['file_name'] カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # カスタムプロパティを追加
        context.object["file_name"] = ""

        return {"FINISHED"}

# パネルファイル
class OBJECT_PT_file_name(bpy.types.Panel):
    bl_idname = "OBJECT_PT_file_name"
    bl_label = "FileName"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # サブメニュー
    def draw(self, context):
        # パネルに項目を追加
        if "file_name" in context.object:
            self.layout.prop(context.object, '["file_name"]', text=self.bl_label)
        else:
            self.layout.operator(MYADDON_OT_add_filename.bl_idname)
            
# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    # Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    # メニューのラベルとして表示される文字列
    bl_label = "Mymenu"
    # 著者表示用の文字列
    bl_description = "拡張メニュー by" + bl_info["author"]

    # サブメニューの描画
    def draw(self,context):

        # トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
            text = MYADDON_OT_stretch_vertex.bl_label)

        # トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
            text = MYADDON_OT_create_ico_sphere.bl_label)
        
         # トップバーの「エディターメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
            text = MYADDON_OT_export_scene.bl_label)


    # 既存のメニューにサブメニューを追加
    def submenu(self,context):
        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

# コライダー描画
class DrawCollider:
    # 描画ハンドル
    handle = None

    # 3Dビューに登録する描画関数
    def draw_collider():

        # 頂点データ
        vertices = {"pos":[]}
        indices = []

        offsets = [
            [-0.5,-0.5,-0.5],
            [+0.5,-0.5,-0.5],
            [-0.5,+0.5,-0.5],
            [+0.5,+0.5,-0.5],
            [-0.5,-0.5,+0.5],
            [+0.5,-0.5,+0.5],
            [-0.5,+0.5,+0.5],
            [+0.5,+0.5,+0.5],
        ]

        size = [2,2,2]

        for object in bpy.context.scene.objects:

            # コライダープロパティがなければ描画スキップ
            if not "collider" in object:
                continue

            # 中心点・サイズの変数を宣言
            center = mathutils.Vector((0,0,0))
            size = mathutils.Vector((2,2,2))

            # プロパティから値を取得
            center[0] = object["collider_center"][0]
            center[1] = object["collider_center"][1]
            center[2] = object["collider_center"][2]
            size[0] = object["collider_size"][0]
            size[1] = object["collider_size"][1]
            size[2] = object["collider_size"][2]

            start = len(vertices["pos"])

            for offset in offsets:
                pos = copy.copy(center)
                pos[0] += offset[0] * size[0]
                pos[1] += offset[1] * size[1]
                pos[2] += offset[2] * size[2]

                pos = object.matrix_world @ pos
                vertices['pos'].append(pos)

                indices.append([start + 0, start + 1])
                indices.append([start + 2, start + 3])
                indices.append([start + 0, start + 2])
                indices.append([start + 1, start + 3])

                indices.append([start + 4, start + 5])
                indices.append([start + 6, start + 7])
                indices.append([start + 4, start + 6])
                indices.append([start + 5, start + 7])

                indices.append([start + 0, start + 4])
                indices.append([start + 1, start + 5])
                indices.append([start + 2, start + 6])
                indices.append([start + 3, start + 7])

        # ビルトインのシェーダを取得
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")

        # バッチを作成
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices = indices)

        # シェーダのパラメータ
        color = [0.5, 1.0, 1.0, 1.0]
        shader.bind()
        shader.uniform_float("color", color)
        
        # 描画
        batch.draw(shader)

# オペレータ カスタムプロパティ コライダー
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_collider"
    bl_label = "コライダー 追加"
    bl_description = "['collider']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object["collider"] = "BOX"
        context.object["collider_center"] = mathutils.Vector((0,0,0))
        context.object["collider_size"] = mathutils.Vector((2,2,2))

        return {"FINISHED"}
    
# パネルコライダー
class OBJECT_PT_collider(bpy.types.Panel):
    bl_idname = "OBJECT_PT_collider"
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        if "collider" in context.object:
            self.layout.prop(context.object, '["collider"]', text = "Type")
            self.layout.prop(context.object, '["collider_center"]', text = "Center")
            self.layout.prop(context.object, '["collider_size"]', text = "Size")
        else:
            self.layout.operator(MYADDON_OT_add_collider.bl_idname)

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
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
    # メニューから項目の削除
    for cls in classes:
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    print("レベルエディタが無効化されました")

if __name__ == "__main__":
    register()