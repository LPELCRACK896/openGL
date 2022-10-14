VERTEX_SHADER = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vColor;

out vec4 outColor; 

void main()
{
    gl_Position = vec4(position, 1.0);
    outColor = vec4(vColor, 1.0);
}
'''
FRAGMENT_SHADER = '''
#version 450 core

out vec4 fragColor;
in vec4 outColor;

void main()
{
    fragColor = outColor;
}
'''