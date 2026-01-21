import numpy as np
import pyrr

class Camera:
    def __init__(self):
        # Camera starts very close to the Sun
        self.start_distance = 3.0
        self.target_distance = 80.0  # Increased for better view
        self.zoom_duration = 45.0  # Even SLOWER - 45 seconds
        
        self.distance = self.start_distance
        
        # Camera at 45-degree elevation angle, viewing from the side
        # elevation: 0° = side view, 90° = top view, 45° = perfect diagonal
        elevation_angle = np.radians(30)  # 30 degrees up from horizontal (not too steep)
        azimuth_angle = np.radians(45)    # 45 degrees around (top-right direction)
        
        # Calculate position using spherical coordinates
        # X and Z create the circular position, Y is the height
        self.position = np.array([
            self.distance * np.cos(elevation_angle) * np.cos(azimuth_angle),  # X: right
            self.distance * np.sin(elevation_angle),                           # Y: elevated (not straight down)
            self.distance * np.cos(elevation_angle) * np.sin(azimuth_angle)   # Z: back
        ], dtype=np.float32)
        
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Projection settings
        self.fov = 45.0
        self.aspect = 16.0 / 9.0
        self.near = 0.1
        self.far = 1000.0
        
        # Animation tracking
        self.elapsed_time = 0.0
        self.zoom_complete = False
    
    def update(self, dt):
        """Update camera position (automatic zoom-out)"""
        if not self.zoom_complete:
            self.elapsed_time += dt
            
            # Calculate zoom progress (0 to 1)
            progress = min(self.elapsed_time / self.zoom_duration, 1.0)
            
            # Smooth easing function (ease-out cubic)
            eased_progress = 1.0 - pow(1.0 - progress, 3.0)
            
            # Interpolate distance
            self.distance = self.start_distance + (self.target_distance - self.start_distance) * eased_progress
            
            # Update position - maintain 30° elevation, 45° azimuth
            elevation_angle = np.radians(30)  # 30 degrees up (not too steep)
            azimuth_angle = np.radians(45)    # 45 degrees around
            
            self.position[0] = self.distance * np.cos(elevation_angle) * np.cos(azimuth_angle)  # X
            self.position[1] = self.distance * np.sin(elevation_angle)                           # Y: height
            self.position[2] = self.distance * np.cos(elevation_angle) * np.sin(azimuth_angle)  # Z
            
            if progress >= 1.0:
                self.zoom_complete = True
    
    def get_view_matrix(self):
        """Returns the view matrix"""
        return pyrr.matrix44.create_look_at(
            self.position,
            self.target,
            self.up
        )
    
    def get_projection_matrix(self):
        """Returns the projection matrix"""
        return pyrr.matrix44.create_perspective_projection(
            self.fov,
            self.aspect,
            self.near,
            self.far
        )