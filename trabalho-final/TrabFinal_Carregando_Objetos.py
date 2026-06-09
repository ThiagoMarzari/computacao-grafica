# ==========================================================
# Ex7_Carregando_Objetos.py
# ==========================================================
#
# OpenGL Moderno
#
# Exemplo completo utilizando:
#
# - GLFW
# - VAO
# - VBO
# - Shader
# - OBJ
# - Textura
# - Câmera FPS
#
# Objetos:
#
# - Chibi
# - Gato
#
# ==========================================================


# ==========================================================
# IMPORTAÇÕES
# ==========================================================

# GLFW
#
# cria janela
# teclado
# mouse

import glfw


# OpenGL
#
# funções OpenGL

from OpenGL.GL import *

import OpenGL.GL.shaders


# numpy
#
# arrays numéricos

import numpy as np


# pyrr
#
# matrizes e vetores

import pyrr

from pyrr import Vector3


# ctypes
#
# ponteiros OpenGL

import ctypes

import cv2


# ==========================================================
# ARQUIVOS AUXILIARES
# ==========================================================

# carrega textura PNG/JPG
from TextureLoader import load_texture

# câmera FPS
from Camera import Camera

# loader OBJ
from ObjLoaderSimple import ObjLoaderSimple





# ==========================================================
# OBJETO CABANA (OBJ)
# ==========================================================

PASTA_CABANA = "objetos/Cabana/"

ARQUIVO_OBJ_CABANA = PASTA_CABANA + "cottage_obj.obj"

ARQUIVO_TEX_CABANA = PASTA_CABANA + "cottage_diffuse.png"


# ==========================================================
# OBJETO ARVORE (OBJ)
# ==========================================================

PASTA_TREE = "objetos/Arvore/"

ARQUIVO_OBJ_TREE = PASTA_TREE + "Tree.obj"

ARQUIVO_TEX_TREE_TRUNK = PASTA_TREE + "bark_0021.jpg"

ARQUIVO_TEX_TREE_LEAVES = PASTA_TREE + "DB2X2_L01.png"


# ==========================================================
# TERRENO (PLANO)
# ==========================================================

ARQUIVO_TEX_GROUND = "texturas/grama/rocky_terrain_02_diff_1k.jpg"


# ==========================================================
# CÉU (SKYBOX)
# ==========================================================

ARQUIVO_TEX_SKY = "texturas/kloofendal_overcast_puresky_1k.hdr"


# ==========================================================
# CONFIGURAÇÕES DA JANELA
# ==========================================================

WIDTH = 800

HEIGHT = 600


# ==========================================================
# VARIÁVEIS GLOBAIS
# ==========================================================

# janela GLFW
Window = None

# shader principal
Shader_programm = None





# ==========================================================
# CABANA
# ==========================================================

# VAO cabana
vao_cabana = None

# quantidade vértices
num_vertices_cabana = 0

# textura cabana
textura_cabana = None


# ==========================================================
# GATO
# ==========================================================

# VAO gato
vao_cat = None

# quantidade vértices
num_vertices_cat = 0

# textura gato
textura_cat = None


# ==========================================================
# TERRENO
# ==========================================================

# VAO terreno
vao_ground = None

# quantidade vértices
num_vertices_ground = 0

# textura terreno
textura_ground = None


# ==========================================================
# CÉU (SKYBOX)
# ==========================================================

# Shader céu
Shader_skybox = None

# VAO céu
vao_skybox = None

# textura céu (HDR)
textura_skybox = None


# ==========================================================
# ARVORE
# ==========================================================

# VAO arvore - tronco
vao_tree_trunk = None

# quantidade vértices - tronco
num_vertices_tree_trunk = 0

# textura - tronco
textura_tree_trunk = None

# VAO arvore - folhas
vao_tree_leaves = None

# quantidade vértices - folhas
num_vertices_tree_leaves = 0

# textura - folhas
textura_tree_leaves = None


# ==========================================================
# CÂMERA
# ==========================================================

cam = Camera()


# ==========================================================
# VARIÁVEIS MOUSE
# ==========================================================

# primeira leitura
first_mouse = True

# posição inicial mouse
lastX = WIDTH / 2

lastY = HEIGHT / 2


# ==========================================================
# CALLBACK REDIMENSIONAMENTO
# ==========================================================

def redimensiona_callback(window, w, h):

    """
    Executado quando janela muda tamanho.
    """

    global WIDTH
    global HEIGHT

    WIDTH = w

    HEIGHT = h

    # ajusta viewport OpenGL
    glViewport(0, 0, WIDTH, HEIGHT)


# ==========================================================
# CALLBACK TECLADO
# ==========================================================

def teclado_callback(window, key, scancode, action, mods):

    """
    Fecha aplicação ao pressionar ESC.
    """

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:

        glfw.set_window_should_close(window, True)


# ==========================================================
# CALLBACK MOUSE
# ==========================================================

def mouse_callback(window, xpos, ypos):

    """
    Controla rotação câmera com mouse.
    """

    global first_mouse

    global lastX
    global lastY

    # evita movimento brusco inicial
    if first_mouse:

        lastX = xpos

        lastY = ypos

        first_mouse = False

    # deslocamento horizontal
    xoffset = xpos - lastX

    # deslocamento vertical
    yoffset = lastY - ypos

    # atualiza posição
    lastX = xpos

    lastY = ypos

    # envia para câmera
    cam.process_mouse_movement(xoffset, yoffset)


# ==========================================================
# INICIALIZA OPENGL
# ==========================================================

def inicializa_opengl():

    """
    Inicializa:
    - GLFW
    - Janela
    - OpenGL
    """

    global Window

    # inicializa GLFW
    if not glfw.init():

        raise RuntimeError("Erro GLFW")

    # Configurações para macOS (OpenGL Core Profile)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    # cria janela
    Window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "OpenGL Moderno",
        None,
        None
    )

    # verifica erro
    if not Window:

        glfw.terminate()

        raise RuntimeError("Erro Janela")

    # torna contexto OpenGL atual
    glfw.make_context_current(Window)

    # callbacks
    glfw.set_window_size_callback(
        Window,
        redimensiona_callback
    )

    glfw.set_key_callback(
        Window,
        teclado_callback
    )

    glfw.set_cursor_pos_callback(
        Window,
        mouse_callback
    )

    # captura mouse
    glfw.set_input_mode(
        Window,
        glfw.CURSOR,
        glfw.CURSOR_DISABLED
    )

    # ======================================================
    # DEPTH TEST
    # ======================================================

    # importante em cenas 3D
    #
    # evita objetos atrás aparecerem na frente

    glEnable(GL_DEPTH_TEST)

    # ======================================================
    # DESATIVA CULL FACE
    # ======================================================

    # alguns OBJ possuem faces invertidas
    #
    # evita objeto "furado"

    glDisable(GL_CULL_FACE)

    # mostra versão OpenGL
    print(glGetString(GL_VERSION).decode())


# ==========================================================
# CRIA TERRENO (PLANO REPETIDO)
# ==========================================================

def criar_terreno(arquivo_tex):
    """
    Cria uma malha plana de terreno (quadrado) com coordenadas de textura
    que se repetem para criar um ladrilhamento (tiling).
    """
    # 2 triângulos para um quad plano no chão (Y = -1.5)
    # x y z u v
    vertices = np.array([
        # Triângulo 1
        -100.0, -1.5, -100.0,  0.0, 50.0,
        -100.0, -1.5,  100.0,  0.0,  0.0,
         100.0, -1.5, -100.0, 50.0, 50.0,
         
        # Triângulo 2
         100.0, -1.5, -100.0, 50.0, 50.0,
        -100.0, -1.5,  100.0,  0.0,  0.0,
         100.0, -1.5,  100.0, 50.0,  0.0,
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride = vertices.itemsize * 5

    # Atributo 0: Posição
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(0)
    )

    # Atributo 1: Coordenadas UV
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(
        1,
        2,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(vertices.itemsize * 3)
    )

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Carrega a textura
    textura = glGenTextures(1)
    load_texture(arquivo_tex, textura)

    return vao, 6, textura


# ==========================================================
# CRIA CÉU (SKYBOX CÚBICO)
# ==========================================================

def criar_skybox():
    vertices = np.array([
        # Posições do cubo unitário
        -1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0,  1.0,

         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 3, ctypes.c_void_p(0))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao, 36


# ==========================================================
# SHADERS DO CÉU (EQUIRRETANGULAR HDR)
# ==========================================================

def inicializa_shaders_skybox():
    vertex_src = """
        #version 400
        layout(location = 0) in vec3 in_pos;
        uniform mat4 projection;
        uniform mat4 view;
        out vec3 local_pos;
        void main()
        {
            local_pos = in_pos;
            mat4 view_no_translate = mat4(mat3(view));
            vec4 pos = projection * view_no_translate * vec4(in_pos, 1.0);
            gl_Position = pos.xyww;
        }
    """
    
    fragment_src = """
        #version 400
        in vec3 local_pos;
        uniform sampler2D sky_texture;
        out vec4 FragColor;
        void main()
        {
            vec3 dir = normalize(local_pos);
            // Mapeamento equirretangular de coordenadas 3D para 2D UV
            float u = atan(dir.z, dir.x) / (2.0 * 3.14159265359) + 0.5;
            float v = asin(dir.y) / 3.14159265359 + 0.5;
            vec3 color = texture(sky_texture, vec2(u, v)).rgb;
            
            // Tonemapping de Reinhard e correção gama
            color = color / (color + vec3(1.0));
            color = pow(color, vec3(1.0 / 2.2));
            
            // Escurece significativamente para criar a noite de terror
            vec3 night_color = color * 0.08;
            
            FragColor = vec4(night_color, 1.0);
        }
    """
    
    vertex_shader = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
    return OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)


# ==========================================================
# CARREGA TEXTURA HDR (FLUTUANTE)
# ==========================================================

def carregar_textura_hdr(caminho):
    img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise RuntimeError(f"Erro ao carregar imagem HDR no caminho: {caminho}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape

    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Upload dos dados como float (usando GL_RGB16F para HDR)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB16F,
        width,
        height,
        0,
        GL_RGB,
        GL_FLOAT,
        img
    )
    return textura


# ==========================================================
# CARREGA OBJETO
# ==========================================================

def carregar_objeto(arquivo_obj, arquivo_tex, material_filter=None):

    """
    Carrega:
    - OBJ
    - VAO
    - VBO
    - textura
    """

    # ======================================================
    # CARREGA OBJ
    # ======================================================

    # retorna:
    #
    # buffer
    # quantidade vértices

    buffer, num_vertices = ObjLoaderSimple.load_obj(
        arquivo_obj,
        material_filter=material_filter
    )

    # converte para float32
    buffer = buffer.astype(np.float32)

    # ======================================================
    # CRIA VAO
    # ======================================================

    vao = glGenVertexArrays(1)

    # ativa VAO
    glBindVertexArray(vao)

    # ======================================================
    # CRIA VBO
    # ======================================================

    vbo = glGenBuffers(1)

    # ativa VBO
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # ======================================================
    # ENVIA BUFFER GPU
    # ======================================================

    glBufferData(
        GL_ARRAY_BUFFER,
        buffer.nbytes,
        buffer,
        GL_STATIC_DRAW
    )

    # ======================================================
    # CONFIGURA ATRIBUTOS
    # ======================================================

    # cada vértice:
    #
    # x y z u v

    stride = buffer.itemsize * 5

    # ======================================================
    # POSIÇÃO
    # ======================================================

    # ativa atributo posição
    glEnableVertexAttribArray(0)

    # configura leitura:
    #
    # x y z

    glVertexAttribPointer(
        0,                          # location shader
        3,                          # x y z
        GL_FLOAT,                  # tipo
        GL_FALSE,                  # normalizar
        stride,                    # tamanho vértice
        ctypes.c_void_p(0)         # offset
    )

    # ======================================================
    # UV
    # ======================================================

    # ativa atributo UV
    glEnableVertexAttribArray(1)

    # configura leitura:
    #
    # u v

    glVertexAttribPointer(
        1,                                  # location shader
        2,                                  # u v
        GL_FLOAT,                           # tipo
        GL_FALSE,                           # normalizar
        stride,                             # tamanho vértice
        ctypes.c_void_p(buffer.itemsize * 3)
    )

    # ======================================================
    # DESATIVA
    # ======================================================

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

    # ======================================================
    # TEXTURA
    # ======================================================

    textura = glGenTextures(1)

    load_texture(
        arquivo_tex,
        textura
    )

    return vao, num_vertices, textura


# ==========================================================
# SHADERS
# ==========================================================

def inicializa_shaders():

    """
    Cria shaders.
    """

    global Shader_programm

    # ======================================================
    # VERTEX SHADER
    # ======================================================

    vertex_src = """

        #version 400

        layout(location = 0) in vec3 in_pos;

        layout(location = 1) in vec2 in_uv;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        out vec2 frag_uv;
        out vec3 frag_pos_view;
        out vec3 frag_pos_world;

        void main()
        {
            frag_uv = in_uv;
            vec4 world_pos = model * vec4(in_pos, 1.0);
            frag_pos_world = world_pos.xyz;
            
            vec4 view_pos = view * world_pos;
            frag_pos_view = view_pos.xyz;
            gl_Position = projection * view_pos;
        }

    """

    # ======================================================
    # FRAGMENT SHADER
    # ======================================================

    fragment_src = """

        #version 400

        in vec2 frag_uv;
        in vec3 frag_pos_view;
        in vec3 frag_pos_world;

        uniform sampler2D texture1;
        uniform float time;

        out vec4 FragColor;

        void main()
        {
            vec4 color = texture(texture1, frag_uv);
            
            // Descarta fragmentos transparentes para remover bordas brancas
            if (color.a < 0.1)
                discard;
                
            // 1. Iluminação ambiente da noite (sem lanterna)
            float ambient = 0.25;
            
            // 2. Luz vermelha pulsante de terror vindo da cabana (World Space)
            // Posição ajustada para a janela/porta da cabana
            vec3 red_light_pos = vec3(5.0, -5.0, 2.0);
            float red_dist = distance(frag_pos_world, red_light_pos);
            float red_attenuation = 1.0 / (1.0 + 0.15 * red_dist + 0.08 * red_dist * red_dist);
            
            float pulse = 0.7 + 0.3 * sin(time * 3.0);
            vec3 red_light_color = vec3(0.9, 0.0, 0.0) * red_attenuation * 6.0 * pulse;
            
            // Combina as iluminações
            vec3 final_lighting = vec3(ambient) + red_light_color;
            vec3 lit_color = color.rgb * final_lighting;
            
            // 3. Efeito de Neblina Escura (Fog de Terror)
            float dist = length(frag_pos_view);
            float fog_start = 5.0;
            float fog_end = 75.0;
            float fog_factor = clamp((dist - fog_start) / (fog_end - fog_start), 0.0, 1.0);
            
            // Tom de cinza escuro da noite de terror
            vec3 fog_color = vec3(0.035, 0.04, 0.05);
            
            vec3 final_color = mix(lit_color, fog_color, fog_factor);
            
            FragColor = vec4(final_color, color.a);
        }

    """

    # ======================================================
    # COMPILA VERTEX
    # ======================================================

    vertex_shader = OpenGL.GL.shaders.compileShader(
        vertex_src,
        GL_VERTEX_SHADER
    )

    # ======================================================
    # COMPILA FRAGMENT
    # ======================================================

    fragment_shader = OpenGL.GL.shaders.compileShader(
        fragment_src,
        GL_FRAGMENT_SHADER
    )

    # ======================================================
    # PROGRAMA FINAL
    # ======================================================

    Shader_programm = OpenGL.GL.shaders.compileProgram(
        vertex_shader,
        fragment_shader
    )


# ======================================================
# LOOP PRINCIPAL DA APLICAÇÃO
# ======================================================
#
# A partir deste ponto a aplicação entra
# em um loop contínuo de renderização.
#
# O render_loop():
#
# - processa teclado
# - processa mouse
# - atualiza câmera
# - limpa tela
# - desenha objetos
# - atualiza janela
#
# Esse loop permanece executando até
# o usuário fechar a aplicação.

# ======================================================
def render_loop():

    # ======================================================
    # MATRIZ MODEL - CABANA
    # ======================================================

    escala_cabana = pyrr.matrix44.create_from_scale(
        Vector3([0.2, 0.2, 0.2])
    )

    # Deixa sem rotação inicial
    rotacao_cabana = pyrr.matrix44.create_from_y_rotation(
        np.radians(0)
    )

    # Coloca a cabana no cenário
    translacao_cabana = pyrr.matrix44.create_from_translation(
        Vector3([5.0, -8.0, 0.0])
    )

    model_cabana = pyrr.matrix44.multiply(
        rotacao_cabana,
        escala_cabana
    )

    model_cabana = pyrr.matrix44.multiply(
        translacao_cabana,
        model_cabana
    )

    # ======================================================
    # MATRIZ MODEL - GATO
    # ======================================================

    escala_cat = pyrr.matrix44.create_from_scale(
        Vector3([0.05, 0.05, 0.05])
    )

    # O modelo do gato está rotacionado. Usamos rot_x de 90 graus para deixá-lo em pé.
    rot_x = pyrr.matrix44.create_from_x_rotation(np.radians(90))
    rot_y = pyrr.matrix44.create_from_y_rotation(np.radians(-45))
    rotacao_cat = pyrr.matrix44.multiply(rot_x, rot_y)

    # Posiciona no chão da cabana (a base da cabana fica por volta de Y = -9.8)
    translacao_cat = pyrr.matrix44.create_from_translation(
        Vector3([6.8, 100.8, -30.0])
    )

    model_cat = pyrr.matrix44.multiply(
        rotacao_cat,
        escala_cat
    )

    model_cat = pyrr.matrix44.multiply(
        translacao_cat,
        model_cat
    )

    # ======================================================
    # ARRANJO DE ÁRVORES (Matrizes model pré-calculadas para a floresta)
    # ======================================================

    model_arvores = []
    import random
    # Usando semente fixa para reprodutibilidade
    rng = random.Random(42)

    # Geramos cerca de 550 árvores espalhadas para formar uma floresta densa
    posicoes_arvores = []
    while len(posicoes_arvores) < 600:
        x = rng.uniform(-85.0, 85.0)
        z = rng.uniform(-85.0, 85.0)
        
        # Evita colocar árvores em cima ou muito próximo da cabana (localizada no centro de [5.0, -8.0, 0.0])
        dist_cabana = np.sqrt((x - 5.0)**2 + z**2)
        if dist_cabana < 10.0:
            continue
            
        posicoes_arvores.append(Vector3([x, -1.5, z]))

    for pos in posicoes_arvores:
        # Árvores menores e mais proporcionais (escala de 1.2 a 2.5) com variação de altura
        scale_val = rng.uniform(1.2, 2.5)
        escala = pyrr.matrix44.create_from_scale(
            Vector3([scale_val, scale_val, scale_val])
        )
        
        # Rotação aleatória de 0 a 360 graus no eixo Y
        rot_y = pyrr.matrix44.create_from_y_rotation(
            np.radians(rng.uniform(0, 360))
        )
        
        trans = pyrr.matrix44.create_from_translation(pos)
        
        m = pyrr.matrix44.multiply(rot_y, escala)
        m = pyrr.matrix44.multiply(trans, m)
        model_arvores.append(m)

    # ======================================================
    # CONTROLE TEMPO
    # ======================================================

    last_time = glfw.get_time()

    base_speed = 10.0

    # ======================================================
    # LOOP PRINCIPAL
    # ======================================================

    while not glfw.window_should_close(Window):

        # ==================================================
        # DELTA TIME
        # ==================================================

        current_time = glfw.get_time()

        delta = current_time - last_time

        last_time = current_time

        vel = base_speed * delta

        # ==================================================
        # MOVIMENTO CÂMERA
        # ==================================================

        if glfw.get_key(Window, glfw.KEY_W) == glfw.PRESS:

            cam.process_keyboard("FORWARD", vel)

        if glfw.get_key(Window, glfw.KEY_S) == glfw.PRESS:

            cam.process_keyboard("BACKWARD", vel)

        if glfw.get_key(Window, glfw.KEY_A) == glfw.PRESS:

            cam.process_keyboard("LEFT", vel)

        if glfw.get_key(Window, glfw.KEY_D) == glfw.PRESS:

            cam.process_keyboard("RIGHT", vel)

        # ==================================================
        # LIMPA TELA
        # ==================================================

        glClearColor(0.1, 0.1, 0.1, 1.0)

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # ==================================================
        # ATIVA SHADER
        # ==================================================

        glUseProgram(Shader_programm)

        # Envia tempo para oscilação da luz vermelha de terror da cabana
        glUniform1f(
            glGetUniformLocation(Shader_programm, "time"),
            glfw.get_time()
        )

        # ==================================================
        # VIEW
        # ==================================================

        view = cam.get_view_matrix()

        # ==================================================
        # PROJECTION
        # ==================================================

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45.0,
            WIDTH / HEIGHT,
            0.1,
            100.0
        )

        # ==================================================
        # ENVIA VIEW
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "view"),
            1,
            GL_FALSE,
            view
        )

        # ==================================================
        # ENVIA PROJECTION
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "projection"),
            1,
            GL_FALSE,
            projection
        )



        # ==================================================
        # DESENHA CÉU (SKYBOX)
        # ==================================================

        glDepthFunc(GL_LEQUAL)
        glUseProgram(Shader_skybox)

        # Envia view e projection para o shader do céu
        glUniformMatrix4fv(
            glGetUniformLocation(Shader_skybox, "view"),
            1,
            GL_FALSE,
            view
        )
        glUniformMatrix4fv(
            glGetUniformLocation(Shader_skybox, "projection"),
            1,
            GL_FALSE,
            projection
        )

        glBindVertexArray(vao_skybox)
        glBindTexture(GL_TEXTURE_2D, textura_skybox)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # Restaura o shader principal e o depth func padrão
        glDepthFunc(GL_LESS)
        glUseProgram(Shader_programm)
        glUniform1f(
            glGetUniformLocation(Shader_programm, "time"),
            glfw.get_time()
        )


        # ==================================================
        # DESENHA TERRENO (CHÃO)
        # ==================================================

        model_ground = pyrr.matrix44.create_identity()
        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_ground
        )

        glBindVertexArray(vao_ground)
        glBindTexture(GL_TEXTURE_2D, textura_ground)
        glDrawArrays(GL_TRIANGLES, 0, num_vertices_ground)


        # ==================================================
        # DESENHA CABANA
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_cabana
        )

        # ativa VAO
        glBindVertexArray(vao_cabana)

        # ativa textura
        glBindTexture(GL_TEXTURE_2D, textura_cabana)

        # desenha
        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_cabana
        )

        # ==================================================
        # DESENHA GATO
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_cat
        )

        glBindVertexArray(vao_cat)

        glBindTexture(GL_TEXTURE_2D, textura_cat)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_cat
        )

        # ==================================================
        # DESENHA ÁRVORES (Múltiplas instâncias)
        # ==================================================

        # 1. Desenha o tronco das árvores
        glBindVertexArray(vao_tree_trunk)
        glBindTexture(GL_TEXTURE_2D, textura_tree_trunk)
        for model_tree in model_arvores:
            glUniformMatrix4fv(
                glGetUniformLocation(Shader_programm, "model"),
                1,
                GL_FALSE,
                model_tree
            )
            glDrawArrays(
                GL_TRIANGLES,
                0,
                num_vertices_tree_trunk
            )

        # 2. Desenha as folhas das árvores
        glBindVertexArray(vao_tree_leaves)
        glBindTexture(GL_TEXTURE_2D, textura_tree_leaves)
        for model_tree in model_arvores:
            glUniformMatrix4fv(
                glGetUniformLocation(Shader_programm, "model"),
                1,
                GL_FALSE,
                model_tree
            )
            glDrawArrays(
                GL_TRIANGLES,
                0,
                num_vertices_tree_leaves
            )

        # ==================================================
        # ATUALIZA
        # ==================================================

        glfw.swap_buffers(Window)

        glfw.poll_events()

    glfw.terminate()


# ==========================================================
# MAIN
# ==========================================================

def main():

    global vao_cabana
    global num_vertices_cabana
    global textura_cabana

    global vao_cat
    global num_vertices_cat
    global textura_cat

    global vao_tree_trunk
    global num_vertices_tree_trunk
    global textura_tree_trunk

    global vao_tree_leaves
    global num_vertices_tree_leaves
    global textura_tree_leaves

    global vao_ground
    global num_vertices_ground
    global textura_ground

    global Shader_skybox
    global vao_skybox
    global textura_skybox

    # inicializa OpenGL
    inicializa_opengl()

    # ======================================================
    # CÉU (SKYBOX)
    # ======================================================

    vao_skybox, _ = criar_skybox()
    textura_skybox = carregar_textura_hdr(ARQUIVO_TEX_SKY)
    glBindVertexArray(vao_skybox)
    Shader_skybox = inicializa_shaders_skybox()
    glBindVertexArray(0)

    # ======================================================
    # TERRENO
    # ======================================================

    vao_ground, num_vertices_ground, textura_ground = criar_terreno(
        ARQUIVO_TEX_GROUND
    )

    # ======================================================
    # CABANA
    # ======================================================

    vao_cabana, num_vertices_cabana, textura_cabana = carregar_objeto(
        ARQUIVO_OBJ_CABANA,
        ARQUIVO_TEX_CABANA
    )

    # ======================================================
    # GATO
    # ======================================================

    vao_cat, num_vertices_cat, textura_cat = carregar_objeto(
        "objetos/Cat/Cat.obj",
        "objetos/Cat/Cat_diffuse.jpg"
    )

    # ======================================================
    # ARVORE
    # ======================================================

    # Tronco
    vao_tree_trunk, num_vertices_tree_trunk, textura_tree_trunk = carregar_objeto(
        ARQUIVO_OBJ_TREE,
        ARQUIVO_TEX_TREE_TRUNK,
        material_filter="Trank_bark"
    )

    # Folhas
    vao_tree_leaves, num_vertices_tree_leaves, textura_tree_leaves = carregar_objeto(
        ARQUIVO_OBJ_TREE,
        ARQUIVO_TEX_TREE_LEAVES,
        material_filter="polySurface1SG1"
    )

    # shaders
    glBindVertexArray(vao_cabana)
    inicializa_shaders()
    glBindVertexArray(0)

    # loop renderização
    render_loop()


# ==========================================================
# INÍCIO
# ==========================================================

if __name__ == "__main__":

    main()




# ==========================================================
# FLUXO GERAL DA APLICAÇÃO - EXPLICAÇÃO
# ==========================================================
#
# INÍCIO DO PROGRAMA
#
# if __name__ == "__main__":
#         ↓
#       main()
#
#
# ==========================================================
# MAIN
# ==========================================================
#
# main()
#
# 1) inicializa_opengl()
#       ↓
#    - GLFW
#    - janela
#    - callbacks
#    - OpenGL
#    - depth test
#
#
# 2) carregar_objeto(chibi.obj, chibi.png)
#       ↓
#    ObjLoaderSimple.load_obj()
#       ↓
#    - lê OBJ
#    - triangula faces
#    - cria buffer
#       ↓
#    OpenGL:
#    - cria VAO
#    - cria VBO
#    - envia buffer GPU
#       ↓
#    TextureLoader.load_texture()
#       ↓
#    - carrega imagem
#    - cria textura GPU
#
#
# 3) carregar_objeto(cat.obj, cat.jpg)
#       ↓
#    mesmo processo acima
#
#
# 4) inicializa_shaders()
#       ↓
#    - compila vertex shader
#    - compila fragment shader
#    - cria shader program
#
#
# 5) render_loop()
#       ↓
#    LOOP PRINCIPAL DA APLICAÇÃO
#
#
# ==========================================================
# RENDER LOOP
# ==========================================================
#
# enquanto janela aberta:
#
#   ↓
#
# 1) calcula delta time
#
# 2) processa teclado
#       ↓
#    movimenta câmera
#
# 3) processa mouse
#       ↓
#    atualiza yaw/pitch
#
# 4) limpa tela
#
# 5) ativa shader
#
# 6) cria matrizes:
#       ↓
#    - model
#    - view
#    - projection
#
# 7) envia matrizes GPU
#
# 8) desenha CHIBI
#       ↓
#    - ativa VAO
#    - ativa textura
#    - glDrawArrays()
#
# 9) desenha GATO
#       ↓
#    - ativa VAO
#    - ativa textura
#    - glDrawArrays()
#
# 10) atualiza janela
#       ↓
#    glfw.swap_buffers()
#
# 11) processa eventos
#       ↓
#    glfw.poll_events()
#
#
# ==========================================================
# FINALIZAÇÃO
# ==========================================================
#
# janela fechada:
#       ↓
# glfw.terminate()
#
# ==========================================================
