import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from numpy import array, float32
import ctypes
#Clase temporal
class Buffer(object):
    def __init__(self, data) -> None:
        self.data = data 
        self.vertBuffer = None
        self.VBO = None
        self.VAO = None
        self.createVertexBuffer()

    def createVertexBuffer(self):
        self.vertBuffer  = array(self.data, dtype = float32)
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

    def setShadders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragmentShader, GL_FRAGMENT_SHADER)) 
            return
        self.active_shader = None

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.active_shader is not None: glUseProgram(self.active_shader)
        for obj in self.scene: obj.render()
