from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D,anneau, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

def main():
    
    viewer = ViewerGL()
    
    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()
    

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
<<<<<<< HEAD
    #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.y = 50
    tr.translation.z = 2
=======
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
>>>>>>> 940178d9979bb835bdb8cc80b7c92129c804c475
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    
    
    viewer.add_object(("p",o))
    viewer.transfer(program3d_id, programGUI_id, m)

<<<<<<< HEAD

    m = Mesh.load_obj('stegosaurus2.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    for i in range (50):
        
        tr = Transformation3D()
        #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation. x=1* random.randrange(-100, 100)
        tr.translation.y = 50
        tr.translation.z = 1* random.randrange(-100, 100)
        tr.rotation_euler[1]= random.randrange(-1,1)
        tr.rotation_euler[0]= 1.5
        tr.rotation_euler[2]= 2
        texture = glutils.load_texture('jaune.jpg')
        o = anneau(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,1)
        viewer.add_object(o)

    m = Mesh.load_obj('cube.obj')
    m.normalize
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    for i in range (10):
        
        tr = Transformation3D()
        #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation. x=1* random.randrange(-100, 100)
        tr.translation.y = 50
        tr.translation.z = 1* random.randrange(-100, 100)
        texture = glutils.load_texture('jaune.jpg')
        o = anneau(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,1)
        viewer.add_object(o)
    

    m=Mesh()
    p0, p1, p2, p3 = [-50*50, 0, -50*50], [50*50, 0, -50*50], [50*50, 0, 50*50], [-50*50, 0, 50*50]
=======
    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
>>>>>>> 940178d9979bb835bdb8cc80b7c92129c804c475
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(("floor",o))

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
<<<<<<< HEAD
   # o = Text(' bonjour', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)
    #o = Text(' les ', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)
    #o = Text(' 3ETI', np.array([-0.5,-1], np.float32), np.array([1.3, 0.4], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)
=======
    o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(("text",o))
    o = Text('3ETI', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(("txt",o))

>>>>>>> 940178d9979bb835bdb8cc80b7c92129c804c475
    viewer.run()


if __name__ == '__main__':
    main()