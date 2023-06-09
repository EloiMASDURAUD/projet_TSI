#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import time
import pyrr
import numpy as np
from cpe3d import Object3D, Transformation3D
import glutils

class ViewerGL:

    #AAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBB
    cursor_x = 0
    cursor_y = 0
    last_shot_time  = time.time()

    # Les touches quand on appui etc
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)

        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE)
        #glfw.set_cursor_pos_callback(self.window, self.cursor_callback)

        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}

    def run(self):
        # boucle d'affichage


        

        while not glfw.window_should_close(self.window):
        


            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.update_key()

            #Personnage qui avance en permanence
            self.objs[0][1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0][1].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.10]))

            #Stégosaure copié imite le stégosaure initiale caché :
            self.objs[1][1].transformation.translation = self.objs[0][1].transformation.translation.copy()

            self.objs[1][1].transformation.rotation_euler = self.objs[0][1].transformation.rotation_euler.copy()
            if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
                self.objs[1][1].transformation.rotation_euler[0] = self.objs[1][1].transformation.rotation_euler[2]

            # Caméra ten permanence derrière le personnage
            self.cam.transformation.rotation_euler = self.objs[0][1].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.translation = self.objs[0][1].transformation.translation + pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0][1].transformation.rotation_euler), pyrr.Vector3([0,0, -8]))
            self.cam.transformation.rotation_center = self.cam.transformation.translation


    

            self.update_camera(self.objs[0][1].program)
            for item in self.objs:
                id = item[0]
                obj = item[1] 
                GL.glUseProgram(obj.program)
                if id == "shot":   
                    obj.transformation.translation += \
                        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(obj.transformation.rotation_euler), pyrr.Vector3([0, 0, 0.5]))            
                if id == "anneau" :
                    distance = 0
                    for i in range (3):
                        distance += (obj.transformation.translation[i] - self.objs[0][1].transformation.translation[i])**2
                    if distance < 1 :
                        print ("aaaaa")
                        obj.visible = False
                        self.objs.remove(item)
                        
                if id == "shot" :
                    for item2 in self.objs:
                        if item2[0] == "cube" :
                            distance = 0
                            for i in range (3):
                                distance += (obj.transformation.translation[i] - item2[1].transformation.translation[i])**2
                            if distance < 1 :
                                print ("aaaaa")
                                obj.visible = False
                                item2[1].visible = False
                                self.objs.remove(item2)
                                self.objs.remove(item)
                                
                        
                        
                                        
                obj.draw()
            

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def mouse_button_callback(self, window, button, action, mods):
        self.touch[button] = action
        
    def add_object(self, obj):
        self.objs.append(obj)
    
    def transfer (self, program3d_id, programGUI_id, m):
        self.program3d_id = program3d_id
        self.programGUI_id = programGUI_id
        self.m= m


    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):


        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.objs[0][1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0][1].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0][1].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0][1].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.02]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0][1].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0][1].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.01

            # self.objs[1][1].transformation.rotation_euler[pyrr.euler.index().yaw] = self.objs[0][1].transformation.rotation_euler[pyrr.euler.index().yaw]
            # self.objs[1][1].transformation.translation += pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_z_rotation(np.pi/4,None),  pyrr.Vector3([0, 0, 0.02]))
            

        #if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
        #    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        #if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
        #    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 40
        #if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
        #    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 40
        #if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
        #    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
            
#         if glfw.MOUSE_BUTTON_LEFT in self.touch and self.touch[glfw.MOUSE_BUTTON_LEFT] > 0:
           
#             if time.time()-self.last_shot_time > 1 :
#                 tr =  Transformation3D(self.objs[0][1].transformation.rotation_euler, self.objs[0][1].transformation.rotation_center, self.objs[0][1].transformation.translation)
#                 texture = glutils.load_texture('stegosaurus.jpg')
#                 o = Object3D(self.m.load_to_gpu(), self.m.get_nb_triangles(), self.program3d_id, texture, tr)
#                 self.add_object(("shot",o))    
#                 self.last_shot_time = time.time()

#         if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
#             self.cam.transformation.rotation_euler = self.objs[0][1].transformation.rotation_euler.copy() 
#             self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
#             #self.cam.transformation.rotation_center = self.objs[0][1].transformation.translation + self.objs[0][1].transformation.rotation_center
#             self.cam.transformation.translation = self.objs[0][1].transformation.translation +\
#                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0][1].transformation.rotation_euler), pyrr.Vector3([0,0, -8]))
# # pyrr.Vector3([0, 1, 5])
#             self.cam.transformation.rotation_center = self.cam.transformation.translation
