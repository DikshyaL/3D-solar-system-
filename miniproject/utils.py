from OpenGL.GL import *
import os

def load_shader_program(vertex_path, fragment_path):
    """Compile and link vertex and fragment shaders"""
    
    # Read shader source
    with open(vertex_path, 'r') as f:
        vertex_src = f.read()
    
    with open(fragment_path, 'r') as f:
        fragment_src = f.read()
    
    # Compile vertex shader
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_src)
    glCompileShader(vertex_shader)
    
    # Check vertex shader compilation
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex_shader).decode()
        raise RuntimeError(f"Vertex shader compilation failed:\n{error}")
    
    # Compile fragment shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_src)
    glCompileShader(fragment_shader)
    
    # Check fragment shader compilation
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment_shader).decode()
        raise RuntimeError(f"Fragment shader compilation failed:\n{error}")
    
    # Link program
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    # Check linking
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(shader_program).decode()
        raise RuntimeError(f"Shader program linking failed:\n{error}")
    
    # Clean up shaders (no longer needed after linking)
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return shader_program