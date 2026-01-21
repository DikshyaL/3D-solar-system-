#version 330 core

// Input from vertex shader
in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

// Output color
out vec4 FragColor;

// Uniforms
uniform sampler2D textureSampler;
uniform vec3 lightPos;    // Sun position (0, 0, 0)
uniform vec3 viewPos;     // Camera position
uniform int isSun;        // Is this the sun? (emissive, no lighting)

void main()
{
    // Sample texture
    vec4 texColor = texture(textureSampler, TexCoord);
    
    // If this is the sun or stars, just return texture color (emissive)
    if (isSun == 1) {
        FragColor = texColor;
        return;
    }
    
    // Phong lighting for planets
    
    // Ambient
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * texColor.rgb;
    
    // Diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * texColor.rgb;
    
    // Specular
    float specularStrength = 0.3;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * vec3(1.0, 1.0, 1.0);
    
    // Combine
    vec3 result = ambient + diffuse + specular;
    
    // Apply alpha from texture (for rings)
    FragColor = vec4(result, texColor.a);
}