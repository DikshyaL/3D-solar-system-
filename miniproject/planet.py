import numpy as np
from OpenGL.GL import *
import pyrr
from sphere import Sphere
from ring import Ring
from texture_loader import load_texture

class Planet:
    def __init__(self, shader, radius, distance, rotation_speed, revolution_speed, 
                 texture_path, name="Planet", is_sun=False, has_rings=False, ring_texture=None):
        """
        Create a planet
        
        Args:
            shader: Shader program
            radius: Planet radius
            distance: Distance from sun
            rotation_speed: Speed of rotation on axis
            revolution_speed: Speed of revolution around sun
            texture_path: Path to texture image
            name: Planet name
            is_sun: Whether this is the sun (affects lighting)
            has_rings: Whether planet has rings (Saturn)
            ring_texture: Path to ring texture if has_rings=True
        """
        self.shader = shader
        self.radius = radius
        self.distance = distance
        self.rotation_speed = rotation_speed
        self.revolution_speed = revolution_speed
        self.name = name
        self.is_sun = is_sun
        self.has_rings = has_rings
        
        # Angles for animation
        self.rotation_angle = 0.0
        self.revolution_angle = 0.0
        
        # Create sphere geometry
        self.sphere = Sphere(radius=radius)
        
        # Load texture
        self.texture = load_texture(texture_path)
        
        # Setup OpenGL buffers
        self.setup_buffers()
        
        # Create rings if needed
        self.ring = None
        self.ring_texture = None
        if has_rings and ring_texture:
            self.ring = Ring(inner_radius=radius * 1.2, outer_radius=radius * 2.0)
            self.ring_texture = load_texture(ring_texture)
    
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
        
        # Position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal attribute (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        # Texture coordinate attribute (location = 2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
    
    def update(self, dt):
        """Update rotation and revolution"""
        self.rotation_angle += self.rotation_speed * dt
        self.revolution_angle += self.revolution_speed * dt
    
    def draw(self, camera):
        """Draw the planet"""
        glUseProgram(self.shader)
        
        # Calculate model matrix
        model = pyrr.matrix44.create_identity()
        
        # Revolution around sun
        revolution_matrix = pyrr.matrix44.create_from_y_rotation(self.revolution_angle)
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.distance, 0.0, 0.0]))
        
        # Rotation on own axis
        rotation_matrix = pyrr.matrix44.create_from_y_rotation(self.rotation_angle)
        
        # Combine: revolution * translation * rotation
        model = pyrr.matrix44.multiply(revolution_matrix, translation)
        model = pyrr.matrix44.multiply(model, rotation_matrix)
        
        # Get view and projection matrices
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix()
        
        # Set uniforms
        model_loc = glGetUniformLocation(self.shader, "model")
        view_loc = glGetUniformLocation(self.shader, "view")
        proj_loc = glGetUniformLocation(self.shader, "projection")
        
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        
        # Light position (sun at origin)
        light_pos_loc = glGetUniformLocation(self.shader, "lightPos")
        glUniform3f(light_pos_loc, 0.0, 0.0, 0.0)
        
        # View position
        view_pos_loc = glGetUniformLocation(self.shader, "viewPos")
        glUniform3fv(view_pos_loc, 1, camera.position)
        
        # Is this the sun? (emissive)
        is_sun_loc = glGetUniformLocation(self.shader, "isSun")
        glUniform1i(is_sun_loc, 1 if self.is_sun else 0)
        
        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        texture_loc = glGetUniformLocation(self.shader, "textureSampler")
        glUniform1i(texture_loc, 0)
        
        # Draw planet
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.sphere.get_vertex_count(), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        # Draw rings if present
        if self.ring and self.ring_texture:
            # Apply same revolution and translation, but tilt the ring
            ring_model = pyrr.matrix44.multiply(revolution_matrix, translation)
            
            # Tilt ring slightly
            tilt = pyrr.matrix44.create_from_x_rotation(np.radians(15))
            ring_model = pyrr.matrix44.multiply(ring_model, tilt)
            ring_model = pyrr.matrix44.multiply(ring_model, rotation_matrix)
            
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, ring_model)
            
            # Bind ring texture
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.ring_texture)
            
            # Draw ring
            self.ring.draw()