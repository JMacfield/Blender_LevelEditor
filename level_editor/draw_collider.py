import bpy
import copy
import mathutils
import gpu
import gpu_extras.batch


# コライダー描画
class DrawCollider:
    handle = None
    
    def draw_collider():
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

        for object in bpy.context.scene.objects:
            if not "collider" in object:
                continue

            center = mathutils.Vector((0,0,0))
            size = mathutils.Vector((2,2,2))
            
            center[0]=object["collider_center"][0]
            center[1]=object["collider_center"][1]
            center[2]=object["collider_center"][2]
            size[0]=object["collider_size"][0]
            size[1]=object["collider_size"][1]
            size[2]=object["collider_size"][2]

            start = len(vertices["pos"])

            for offset in offsets:
                pos = copy.copy(center)
                
                pos[0]+=offset[0]*size[0]
                pos[1]+=offset[1]*size[1]
                pos[2]+=offset[2]*size[2]
                
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

        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices=indices)

        color = [0.5, 1.0, 1.0, 1.0]
        
        shader.bind()
        shader.uniform_float("color", color)
        
        batch.draw(shader)