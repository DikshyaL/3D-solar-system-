# 3D Solar System Simulation using OpenGL (Python)

## Abstract
This project implements a real-time three-dimensional Solar System simulation using OpenGL and GLFW in Python, focusing on the practical application of modern computer graphics principles. The simulation models the Sun and planets as textured spherical objects, where each planet independently performs axial rotation and orbital revolution around a central reference point. A programmable graphics pipeline is employed through vertex and fragment shaders to achieve realistic lighting and texture mapping. Core graphics concepts such as Model–View–Projection (MVP) transformations, camera view and perspective projection matrices, depth testing for correct object visibility, and alpha blending for transparent elements such as planetary rings are integrated. Time-based animation using delta time ensures smooth and consistent motion across varying frame rates. The project serves as an educational visualization system that demonstrates how real-time 3D rendering and animation are achieved in modern OpenGL-based applications.

**Keywords:**  
3D Simulation, OpenGL, Computer Graphics, Solar System Visualization, Shader Programming, Transformation Matrices, Texture Mapping, Real-Time Rendering, Delta Time Animation

---

## Project Overview
This project is a Python-based 3D Solar System simulation developed using modern OpenGL (3.3 core profile) and GLFW. It visually represents the Sun and planets as textured spheres and demonstrates axial rotation and orbital revolution using transformation matrices and real-time rendering techniques.

The project is intended for academic and learning purposes and focuses on graphics programming concepts rather than astronomical accuracy.

---

## Features
- Textured 3D rendering of the Sun and planets  
- Axial rotation and orbital revolution for each planet  
- Programmable OpenGL pipeline using GLSL shaders  
- Model–View–Projection (MVP) matrix-based transformations  
- Perspective camera with depth testing  
- Alpha blending for transparent objects such as planetary rings  
- Time-based animation using delta time for smooth motion  
- Star field background rendering  

---

## Technologies Used
- Python 3  
- OpenGL (Modern OpenGL 3.3 Core Profile)  
- GLFW (Window and input handling)  
- PyOpenGL  
- NumPy  
- Pillow (Texture loading)  
- GLSL (Vertex and Fragment Shaders)  

---

## How to Run the Project

### Prerequisites
- Python 3.8 or higher  
- A system with OpenGL 3.3 or higher support  

### Install Dependencies
Install the required Python packages using pip:
```bash
pip install glfw PyOpenGL PyOpenGL_accelerate numpy pillow




