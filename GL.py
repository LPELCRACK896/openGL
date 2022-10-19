import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from numpy import array, float32
import ctypes
#Clase temporal
class Model(object):
    def __init__(self, data) -> None:
        self.data = data 
        self.vertBuffer = None
        self.VBO = None
        self.VAO = None
        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

        self.polyCount = 0

    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.position)
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0)) #x 
        yaw =  glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))#y
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))#z

        rotationMat = pitch * yaw * roll
        
        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def createVertexBuffer(self):
        buffer = []
        self.polyCount = 0
        for face in self.model.faces:
            self.polyCount += 1
            for i in range(3): #Asume que son triangulos
                #positions
                pos = self.model.vertices[face[i][0]-1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])
                # texcoords
                uvs = self.model.texcoords[face[i][1] -1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])
                #normals
                norm = self.model.normals[face[i][2] -1 ]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])
            if len(face) == 4:
                pass #a, ps no termine aqui me quede
        # Vertex Buffer Object 
        self.VBO = glGenBuffers(1)

        # Vertex array object
        self.VAO = glGenVertexArrays(1)

    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Mandar la informacion de vertices, size es de bytes
        glBufferData(target = GL_ARRAY_BUFFER, size = self.vertBuffer.nbytes, data = self.vertBuffer, usage = GL_STATIC_DRAW) # Buffer ID, Buffer size in bytes 

        # Atributos -

        # Atributo de posiciones
        glVertexAttribPointer(index = 0, size = 3, type =  GL_FLOAT, normalized = GL_FALSE, stride = 24, pointer = ctypes.c_void_p(0) ) # Attribute number,  size (cuantos floats hay), tipo de dato
        glEnableVertexAttribArray(0)


        glVertexAttribPointer(index = 1, size = 3, type =  GL_FLOAT, normalized = GL_FALSE, stride = 24, pointer = ctypes.c_void_p(12) ) # Attribute number,  size (cuantos floats hay), tipo de dato
        glEnableVertexAttribArray(1)


        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer)))


class Renderer(object):
    def __init__(self, screen) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        self.scene:list = []
        self.active_shader = None

        # Viex matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)
        self.viewMatrix = self.getViewMatrix()

        #Projection matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),                #FOV
                                                self.width/self.height,         #Aspect ratio
                                                0.1,                            #Near plane
                                                1000                            #Far plane
                                                )
        

    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.camPosition)
        pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1, 0, 0)) #x 
        yaw =  glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0, 1, 0))#y
        roll = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0, 0, 1))#z

        rotationMat = pitch * yaw * roll

        camMatrix = translateMat * rotationMat

        return glm.inverse(camMatrix)
    
    def setShadders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragmentShader, GL_FRAGMENT_SHADER)) 
            return
        self.active_shader = None

    def update(self):
        self.viewMatrix = self.getViewMatrix()

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.active_shader is not None: 
            glUseProgram(self.active_shader)
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'viewMatrix'), 1 , GL_FALSE, glm.value_ptr(self.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'projectionMatrix'), 1 , GL_FALSE, glm.value_ptr(self.projectionMatrix))

            for obj in self.scene: 
                if self.active_shader is not None:
                    glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'modelMatrix'), 1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))
                obj.render()
