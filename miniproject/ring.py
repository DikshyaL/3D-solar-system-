import numpy as np
from OpenGL.GL import *
from texture_loader import load_texture

class Ring:
    def __init__(self, inner_radius=1.5, outer_radius=2.5, segments=60):
        """
        Generate ring geometry (flat disk with hole)
        
        Args:
            inner_radius: Inner radius of ring
            outer_radius: Outer radius of ring
            segments: Number of segments around the ring
        """
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.segments = segments
        
        vertices = []
        
        # Generate ring vertices
        for i in range(segments + 1):
            angle = 2.0 * np.pi * i / segments
            
            cos_a = np.cos(angle)
            sin_a = np.sin(angle)
            
            # Inner vertex
            x_inner = inner_radius * cos_a
            z_inner = inner_radius * sin_a
            u_inner = i / segments
            
            # Outer vertex
            x_outer = outer_radius * cos_a
            z_outer = outer_radius * sin_a
            u_outer = i / segments
            
            # Normal pointing up (y-axis)
            nx, ny, nz = 0.0, 1.0, 0.0
            
            # Inner vertex: position (3), normal (3), texcoord (2)
            vertices.extend([x_inner, 0.0, z_inner, nx, ny, nz, u_inner, 0.0])
            
            # Outer vertex
            vertices.extend([x_outer, 0.0, z_outer, nx, ny, nz, u_outer, 1.0])
        
        # Generate indices (triangle strip pattern)
        indices = []
        for i in range(segments):
            # Two triangles per segment
            base = i * 2
            
            # Triangle 1
            indices.extend([base, base + 1, base + 2])
            # Triangle 2
            indices.extend([base + 1, base + 3, base + 2])
        
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.vertex_count = len(indices)
        
        # Setup OpenGL buffers
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        
        glBindVertexArray(self.vao)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
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
    
    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.vertex_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)