import glfw
from OpenGL.GL import *
import numpy as np
from camera import Camera
from planet import Planet
from stars import Stars
from utils import load_shader_program
import os

class SolarSystem:
    def __init__(self):
        # Initialize GLFW
        if not glfw.init():
            raise Exception("GLFW initialization failed")
        
        # Create window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        
        self.window = glfw.create_window(1280, 720, "Solar System", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")
        
        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)
        
        # OpenGL settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Load shaders
        self.shader = load_shader_program("shader.vert", "shader.frag")
        
        # Create camera
        self.camera = Camera()
        
        # Create stars
        self.stars = Stars(self.shader)
        
        # Create planets (they'll appear as camera zooms out)
        self.planets = []
        self.create_planets()
        
        # Time tracking
        self.start_time = glfw.get_time()
        self.last_time = self.start_time
    
    def create_planets(self):
        """Create all planets with their properties"""
        # Sun (center, no revolution)
        sun = Planet(
            shader=self.shader,
            radius=2.0,
            distance=0.0,
            rotation_speed=0.1,
            revolution_speed=0.0,
            texture_path="textures/sun.png",
            name="Sun",
            is_sun=True
        )
        self.planets.append(sun)
        
        # Mercury
        mercury = Planet(
            shader=self.shader,
            radius=0.4,
            distance=5.0,
            rotation_speed=0.5,
            revolution_speed=4.0,
            texture_path="textures/mercury.png",
            name="Mercury"
        )
        self.planets.append(mercury)
        
        # Venus
        venus = Planet(
            shader=self.shader,
            radius=0.9,
            distance=8.0,
            rotation_speed=0.3,
            revolution_speed=3.0,
            texture_path="textures/venus.png",
            name="Venus"
        )
        self.planets.append(venus)
        
        # Earth
        earth = Planet(
            shader=self.shader,
            radius=1.0,
            distance=12.0,
            rotation_speed=0.10,
            revolution_speed=2.0,
            texture_path="textures/earth.png",
            name="Earth"
        )
        self.planets.append(earth)
        
        # Mars
        mars = Planet(
            shader=self.shader,
            radius=1.0,
            distance=16.0,
            rotation_speed=0.09,
            revolution_speed=1.5,
            texture_path="textures/mars.png",
            name="Mars"
        )
        self.planets.append(mars)
        
        # Jupiter
        jupiter = Planet(
            shader=self.shader,
            radius=1.8,
            distance=22.0,
            rotation_speed=0.20,
            revolution_speed=0.8,
            texture_path="textures/jupiter.png",
            name="Jupiter"
        )
        self.planets.append(jupiter)
        
        # Saturn
        saturn = Planet(
            shader=self.shader,
            radius=1.6,
            distance=28.0,
            rotation_speed=0.18,
            revolution_speed=0.6,
            texture_path="textures/saturn.png",
            name="Saturn",
            has_rings=True,
            ring_texture="textures/saturn_ring.png"
        )
        self.planets.append(saturn)
        
        # Uranus
        uranus = Planet(
            shader=self.shader,
            radius=1.2,
            distance=35.0,
            rotation_speed=0.12,
            revolution_speed=0.04,
            texture_path="textures/uranus.png",
            name="Uranus"
        )
        self.planets.append(uranus)
        
        # Neptune
        neptune = Planet(
            shader=self.shader,
            radius=1.1,
            distance=42.0,
            rotation_speed=0.11,
            revolution_speed=0.03,
            texture_path="textures/neptune.png",
            name="Neptune"
        )
        self.planets.append(neptune)
    
    def framebuffer_size_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        self.camera.aspect = width / height
    
    def run(self):
        while not glfw.window_should_close(self.window):
            # Calculate delta time
            current_time = glfw.get_time()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # Input
            self.process_input(dt)
            
            # Update
            self.camera.update(dt)
            for planet in self.planets:
                planet.update(dt)
            
            # Render
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Draw stars
            self.stars.draw(self.camera)
            
            # Draw planets
            for planet in self.planets:
                planet.draw(self.camera)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        
        self.cleanup()
    
    def process_input(self, dt):
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)
    
    def cleanup(self):
        glfw.terminate()

if __name__ == "__main__":
    app = SolarSystem()
    app.run()