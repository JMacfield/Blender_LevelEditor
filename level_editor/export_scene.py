import bpy
import bpy_extras
import json
import math
import mathutils

# オペレータ シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"

    filename_ext = ".json"

    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')

    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再起関数"""

        #深さ分インデントする（タブを挿入）
        indent = ''
        for i in range(level):
            indent += "\t"

        #オブジェクト名書き込み
        self.write_and_print(file, indent + object.type)
        # ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
        trans, rot, scale = object.matrix_local.decompose()
        # Quaternion -> Euler
        rot = rot.to_euler()
        # 度数法に
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        # トランスフォーム情報を表示
        self.write_and_print(file, indent + "T %f %f %f" % (trans.x, trans.y, trans.z))
        self.write_and_print(file, indent + "R %f %f %f" % (rot.x, rot.y, rot.z))
        self.write_and_print(file, indent + "S %f %f %f" % (scale.x, scale.y, scale.z))
        # カスタムプロパティ 'file_name'
        if "file_name" in object:
            self.write_and_print(file, indent + "N %s" % object["file_name"])
        if "collider" in object:
            self.write_and_print(file, indent + "C %s" % object["collider"])
            self.write_and_print(file, indent + "CC %f %f %f" % (object["collider_center"][0], object["collider_center"][1], object["collider_center"][2]))
            self.write_and_print(file, indent + "CS %f %f %f" % (object["collider_size"][0], object["collider_size"][1], object["collider_size"][2]))

        self.write_and_print(file, indent + 'END')
        self.write_and_print(file, '')

        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)

    def export(self):
        """ファイルに出力"""
        print("シーン情報出力開始... %r" % self.filepath)

        # ファイルをテキスト形式で書き出し用にオープン
        with open(self.filepath, "wt") as file:

            # ファイルに文字列を書き込む
            self.write_and_print(file, "SCENE")
            # シーン内の全オブジェクトについて
            for object in bpy.context.scene.objects:               
                if object.parent:
                    continue

                #シーン直下のオブジェクトをルートノード
                self.parse_scene_recursive(file, object, 0)

    def parse_scene_recursive_json(self, data_parent, object, level):
        # シーンのオブジェクト1個分のjsonオブジェクト生成
        json_object = dict()
        # オブジェクト種類
        json_object["type"] = object.type
        # オブジェクト名
        json_object["name"] = object.name

        # ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
        trans, rot, scale = object.matrix_local.decompose()
        # Quaternion -> Euler
        rot = rot.to_euler()
        # 度数法に
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        # トランスフォーム情報をディクショナリに登録
        transform = dict()
        transform["translate"] = (trans.x, trans.z, trans.y)
        transform["rotate"] = (-rot.x, -rot.z, -rot.y)
        transform["scale"] = (scale.x, scale.z, scale.y)
        # まとめて1個分のjsonオブジェクトに登録
        json_object["transform"] = transform

        # カスタムプロパティ 'disabled'
        if "disabled" in object:
            json_object["disabled"] = object["disabled"]

        # カスタムプロパティ'model_name'
        if "model_name" in object:
            json_object["model_name"] = object["model_name"]

        # カスタムプロパティ'collider'
        if "collider" in object:
            collider = dict()
            collider["type"] = object["collider"]
            collider["center"] = object["collider_center"].to_list()
            collider["size"] = object["collider_size"].to_list()
            json_object["collider"] = collider

        # 1個分のjsonオブジェクトを親オブジェクトに登録
        data_parent.append(json_object)

        # 子ノードがあれば
        if len(object.children) > 0:
            # 子ノードリストを作成
            json_object["children"] = list()

            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"], child, level + 1)


    def export_json(self):
        """json形式でファイルに出力"""

        json_object_root = dict()

        # ノード名
        json_object_root["name"] = "scene"
        # オブジェクトリストを作成
        json_object_root["objects"] = list()

        # シーン内の全オブジェクトについて
        for object in bpy.context.scene.objects:
            if (object.parent):
                continue

            self.parse_scene_recursive_json(json_object_root["objects"], object, 0)

        # オブジェクトをjson文字列にエンコード
        json_text = json.dumps(json_object_root, ensure_ascii=False, cls=json.JSONEncoder, indent=4)
        # コンソールに表示してみる
        print(json_text)

        # ファイルをテキスト形式で書き出し用にオープン
        with open(self.filepath, "wt", encoding="utf-8") as file:
            #ファイルに文字列を書き込む
            file.write(json_text)

    def execute(self, context):

        print("シーン情報をExportします")

        # 出力
        self.export_json()

        print("シーン情報をExportしました")
        self.report({'INFO'}, "シーン情報をExportしました")
        
        return {'FINISHED'}