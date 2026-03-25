import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Estado do cubo
cube_pos = [0.0, 0.0]   # posição X, Y
cube_rot_x = 0.0         # rotação no eixo X
cube_rot_y = 0.0         # rotação no eixo Y
cube_zoom = -6.0         # zoom (distância da câmera)


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def draw_cube():
    glBegin(GL_QUADS)

    # Face traseira (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f( 1,  1, -1); glVertex3f(-1,  1, -1)
    glVertex3f(-1, -1, -1); glVertex3f( 1, -1, -1)

    # Face frontal (verde)
    glColor3f(0, 1, 0)
    glVertex3f( 1, -1,  1); glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1); glVertex3f( 1,  1,  1)

    # Face direita (azul)
    glColor3f(0, 0, 1)
    glVertex3f(1,  1,  1); glVertex3f(1,  1, -1)
    glVertex3f(1, -1, -1); glVertex3f(1, -1,  1)

    # Face esquerda (amarelo)
    glColor3f(1, 1, 0)
    glVertex3f(-1,  1, -1); glVertex3f(-1,  1,  1)
    glVertex3f(-1, -1,  1); glVertex3f(-1, -1, -1)

    # Face superior (ciano)
    glColor3f(0, 1, 1)
    glVertex3f( 1, 1,  1); glVertex3f(-1, 1,  1)
    glVertex3f(-1, 1, -1); glVertex3f( 1, 1, -1)

    # Face inferior (magenta)
    glColor3f(1, 0, 1)
    glVertex3f( 1, -1, -1); glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1,  1); glVertex3f( 1, -1,  1)

    glEnd()


def handle_keys():
    global cube_pos, cube_rot_x, cube_rot_y, cube_zoom
    keys = pygame.key.get_pressed()

    # Movimentação
    if keys[K_w]: cube_pos[1] += 0.05   # cima
    if keys[K_s]: cube_pos[1] -= 0.05   # baixo
    if keys[K_a]: cube_pos[0] -= 0.05   # esquerda
    if keys[K_d]: cube_pos[0] += 0.05   # direita

    # Rotação
    if keys[K_q]: cube_rot_x += 2.0     # rotaciona eixo X +
    if keys[K_e]: cube_rot_x -= 2.0     # rotaciona eixo X -
    if keys[K_r]: cube_rot_y += 2.0     # rotaciona eixo Y +
    if keys[K_f]: cube_rot_y -= 2.0     # rotaciona eixo Y -

    # Zoom
    if keys[K_z]: cube_zoom += 0.1      # zoom in
    if keys[K_x]: cube_zoom -= 0.1      # zoom out


def draw_scene():
    glLoadIdentity()
    glTranslatef(cube_pos[0], cube_pos[1], cube_zoom)
    glRotatef(cube_rot_x, 1, 0, 0)
    glRotatef(cube_rot_y, 0, 1, 0)
    draw_cube()


def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cubo 3D - Computação Gráfica")
    init()

    print("Controles:")
    print("  W/S    → cima / baixo")
    print("  A/D    → esquerda / direita")
    print("  Q/E    → rotacionar eixo X")
    print("  R/F    → rotacionar eixo Y")
    print("  Z/X    → zoom in / zoom out")
    print("  ESC    → sair")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        handle_keys()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()