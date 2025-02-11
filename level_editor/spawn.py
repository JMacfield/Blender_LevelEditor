import bpy
import bpy.ops
import os

class SpawnNames():
    # インデックス
    PROTOTYPE = 0 # プロトタイプのオブジェクト名
    INSTANCE = 1 # 量産時のオブジェクト名
    FILENAME = 2 # リソースのファイル名

    names = {}
    # name["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースのファイル名)
   


# オペレータ 出現ポイントのシンボルを読み込む
class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをImportします"
    prototype_object_name = "ProttypeSpawn"
    object_name = "Spawn"

    def load_obj(self, type):
        print("出現ポイントのシンボルをImportします")

        # 重複ロードを防止
        spawn_object = bpy.data.objects.get(SpawnNames.names[type][SpawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {'CANCELLED'}
        
        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory = os.path.dirname(__file__)
        # ディレクトリからモデルファイルの相対パスを記述
        relative_path = "player/player.obj"
        # 合成してモデルファイルのフルパスを得る
        full_path = os.path.join(addon_directory,relative_path)
        # オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',filepath=full_path,display_type='THUMBNAIL',forward_axis='Z',up_axis='Y')
        # 回転を適用
        bpy.ops.object.transform_apply(location=False,rotation=True,scale=False,properties=False)
        
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name = SpawnNames.names[type][SpawnNames.PROTOTYPE]
        # オブジェクトの種類を設定
        object["type"]=SpawnNames.names[type][SpawnNames.INSTANCE]
        object["objectName"]=type
        # メモリ上には置いておく
        bpy.context.collection.objects.unlink(object)

        return {"FINISHED"}
    
    def execute(self,context):
        # Enemyオブジェクト読み込み
        self.load_obj("Enemy")
        # Playerオブジェクト読み込み
        self.load_obj("Player")
        
        return {"FINISHED"}
    
# オペレーター　出現ポイントのシンボルを作成・配置する
class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを制作します"
    bl_options = {'REGISTER','UNDO'}

    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        # 読み込み済みのコピー元オブジェクトを検索
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        # まだ読み込んでいない場合
        if spawn_object is None:
            # 読み込みオペレータを実行する
            bpy.ops.myaddon.myaddon_ot_spawn_import_symbol('EXEC_DEFAULT')
            # 再検索。今度は見つかるはず
            spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])
        
        print("出現ポイントのシンボルを制作します")

        # Blender出の選択を解除する
        bpy.ops.object.select_all(action = 'DESELECT')
        
        # 複製元の非表示オブジェクトを複製する
        object = spawn_object.copy()

        # 複製したオブジェクトを現在のシーンにリンク（出現させる）
        bpy.context.collection.objects.link(object)

        # オブジェクト名を変更
        object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        return {"FINISHED"}
    
class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):

    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤーの出現シンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Player")
        
        return {"FINISHED"}
    
    
#トップバーの拡張メニュー
class MYADDON_OT_spawn_create_player_symbol_menu(bpy.types.Menu):
    bl_idname = "MYADDON_OT_spawn_create_player_symbol_menu"
    bl_label="プレイヤーの出現ポイントの作成"
    bl_description="プレイヤーの出現ポイントの作成します"
    bl_options = {'REGISTER','UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.operator(MYADDON_OT_spawn_create_player_symbol.bl_idname, text="プレイヤーの出現ポイントを作成")


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):

    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "エネミーの出現シンボルの作成"
    bl_description = "エネミー出現ポイントのシンボルを作成します"

    def execute(self,context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Enemy")
        
        return {"FINISHED"}

#トップバーの拡張メニュー
class MYADDON_OT_spawn_create_enemy_symbol_menu(bpy.types.Menu):
    bl_idname ="MYADDON_OT_spawn_create_enemy_symbol_menu"
    bl_label="エネミーの出現ポイントの作成"
    bl_description="プレイヤエネミーの出現ポイントの作成します"

    def draw(self, context):
        layout = self.layout
        layout.operator(MYADDON_OT_spawn_create_enemy_symbol.bl_idname, text="エネミーの出現ポイントを作成")