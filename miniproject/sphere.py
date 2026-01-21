import numpy as np
import math

class Sphere:
    def __init__(self, radius=1.0, stacks=30, slices=30):
        """
        Generate sphere geometry mathematically
        
        Args:
            radius: Sphere radius
            stacks: Number of horizontal divisions
            slices: Number of vertical divisions
        """
        self.radius = radius
        self.stacks = stacks
        self.slices = slices
        
        vertices = []
        
        # Generate vertices
        for stack in range(stacks + 1):
            phi = math.pi * stack / stacks  # 0 to PI
            
            for slice in range(slices + 1):
                theta = 2 * math.pi * slice / slices  # 0 to 2*PI
                
                # Spherical to Cartesian coordinates
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                
                # Normal (normalized position vector for sphere)
                nx = math.sin(phi) * math.cos(theta)
                ny = math.cos(phi)
                nz = math.sin(phi) * math.sin(theta)
                
                # Texture coordinates
                u = slice / slices
                v = stack / stacks
                
                # Append: position (3), normal (3), texcoord (2)
                vertices.extend([x, y, z, nx, ny, nz, u, v])
        
        # Generate indices
        indices = []
        for stack in range(stacks):
            for slice in range(slices):
                # Two triangles per quad
                first = stack * (slices + 1) + slice
                second = first + slices + 1
                
                # Triangle 1
                indices.extend([first, second, first + 1])
                # Triangle 2
                indices.extend([second, second + 1, first + 1])
        
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.vertex_count = len(indices)
    
    def get_vertices(self):
        return self.vertices
    
    def get_indices(self):
        return self.indices
    
    def get_vertex_count(self):
        return self.vertex_count