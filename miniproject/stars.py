import numpy as np
from OpenGL.GL import *
import pyrr
from sphere import Sphere
from texture_loader import load_texture

class Stars:
    def __init__(self, shader, radius=500.0):
        """
        Create background star sphere
        
        Args:
            shader: Shader program
            radius: Very large radius to contain entire solar system
        """
        self.shader = shader
        self.radius = radius
        
        # Create large sphere
        self.sphere = Sphere(radius=radius, stacks=20, slices=20)
        
        # Load star texture
        self.texture = load_texture("textures/stars.png")
        
        # Setup OpenGL buffers
        self.setup_buffers()
    
    def setup_buffers(self):
        """Setup VAO, VBO, EBO"""
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        
        glBindVertexArray(self.vao)
        
        # Vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.sphere.get_vertices().nbytes,
                     self.sphere.get_vertices(), GL_STATIC_DRAW)
        
        # Element buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.sphere.get_indices().nbytes,
                     self.sphere.get_indices(), GL_STATIC_DRAW)
        
        # Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        # Texture coordinate attribute
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
    
    def draw(self, camera):
        """Draw the star sphere"""
        glUseProgram(self.shader)
        
        # Disable depth writing so stars are always behind everything
        glDepthMask(GL_FALSE)
        
        # Disable depth test temporarily for background
        glDisable(GL_DEPTH_TEST)
        
        # Model matrix (no transformation, centered at origin)
        model = pyrr.matrix44.create_identity()
        
        # Get view and projection
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix()
        
        # Set uniforms
        model_loc = glGetUniformLocation(self.shader, "model")
        view_loc = glGetUniformLocation(self.shader, "view")
        proj_loc = glGetUniformLocation(self.shader, "projection")
        
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        
        # Disable lighting for stars (they emit light)
        is_sun_loc = glGetUniformLocation(self.shader, "isSun")
        glUniform1i(is_sun_loc, 1)
        
        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        texture_loc = glGetUniformLocation(self.shader, "textureSampler")
        glUniform1i(texture_loc, 0)
        
        # Draw
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.sphere.get_vertex_count(), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        # Re-enable depth test and writing
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)