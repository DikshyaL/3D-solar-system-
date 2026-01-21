from OpenGL.GL import *
from PIL import Image
import numpy as np

def load_texture(path):
    """
    Load texture from image file
    
    Args:
        path: Path to image file (JPG or PNG)
    
    Returns:
        OpenGL texture ID
    """
    # Generate texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Load image
    try:
        img = Image.open(path)
        
        # Check if image has alpha channel
        has_alpha = img.mode == 'RGBA'
        
        # Convert to RGB or RGBA
        if has_alpha:
            img = img.convert('RGBA')
            format = GL_RGBA
        else:
            img = img.convert('RGB')
            format = GL_RGB
        
        # Flip image (OpenGL expects origin at bottom-left)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Get image data
        img_data = np.array(img, dtype=np.uint8)
        
        # Upload texture data
        glTexImage2D(GL_TEXTURE_2D, 0, format, img.width, img.height, 
                     0, format, GL_UNSIGNED_BYTE, img_data)
        
        # Generate mipmaps
        glGenerateMipmap(GL_TEXTURE_2D)
        
        print(f"Loaded texture: {path} ({img.width}x{img.height})")
        
    except Exception as e:
        print(f"Error loading texture {path}: {e}")
        # Create a default texture (white)
        default_data = np.array([255, 255, 255], dtype=np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1, 1, 0, GL_RGB, GL_UNSIGNED_BYTE, default_data)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    
    return texture