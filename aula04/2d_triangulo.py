
import pygame  # Importa a biblioteca Pygame para gerenciar gráficos e entrada do usuário
from pygame.locals import *  # Importa constantes do Pygame para eventos de teclado e mouse
from OpenGL.GL import *  # Importa funções do OpenGL para renderização gráfica
from OpenGL.GLUT import *  # Importa GLUT para utilitários gráficos do OpenGL
from OpenGL.GLU import *  # Importa GLU para operações gráficas auxiliares

# Variáveis de posição dos triângulos
tx1, ty1 = 0, 0    # Triângulo central (setas)
tx2, ty2 = -6, 0   # Triângulo da esquerda (WASD)
tx3, ty3 = 6, 0    # Triângulo da direita (IJKL)
zoom = -30         # Posição inicial no eixo Z (aproxima/afasta da câmera)

# Ângulo de rotação individual de cada triângulo
r1 = 0.0  # central
r2 = 0.0  # esquerda
r3 = 0.0  # direita


# Variáveis de escala globais
ex = 2  # Escala global no eixo X
ey = 2  # Escala global no eixo Y
ez = 2  # Escala global no eixo Z

# "Zoom" individual (escala) de cada triângulo
sz1 = 1.0  # Triângulo central
sz2 = 1.0  # Triângulo da esquerda
sz3 = 1.0  # Triângulo da direita

# Função de inicialização do OpenGL
def init():
    glClearColor(1, 1, 1, 1)  # Define a cor de fundo branca (R=1, G=1, B=1, A=1)
    glClearDepth(1.0)  # Define a profundidade máxima para renderização
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade para ocultação de objetos
    glDepthFunc(GL_LEQUAL)  # Define o tipo de teste de profundidade
    glShadeModel(GL_SMOOTH)  # Habilita sombreamento suave
    glMatrixMode(GL_PROJECTION)  # Define a matriz de projeção (perspectiva)
    glLoadIdentity()  # Reinicializa a matriz de projeção
    gluPerspective(45, 640/480, 0.1, 100)  
    # gluPerspective(fov, aspectRatio, near, far)
    # 45 → Campo de visão (FOV) em graus
    # 640/480 → Razão de aspecto (largura/altura da tela)
    # 0.1 → Distância mínima de renderização (near plane)
    # 100 → Distância máxima de renderização (far plane)
    
    glMatrixMode(GL_MODELVIEW)  # Define a matriz de visualização

# Função para desenhar o triângulo
def draw():
    glLoadIdentity()  # Reinicia a matriz de visualização para evitar acúmulo de transformações

    # Transformações globais (câmera / escala geral)
    glTranslatef(0, 0, zoom)
    glScalef(ex, ey, ez)

    # Triângulo central (setas)
    glPushMatrix()
    glTranslatef(tx1, ty1, 0)
    glScalef(sz1, sz1, sz1)
    glRotatef(r1, 0, 1, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 0)  # preto
    glVertex3f(0, 3, 0)
    glVertex3f(-2, -2, 0)
    glVertex3f(2, -2, 0)
    glEnd()
    glPopMatrix()

    # Triângulo esquerda (WASD)
    glPushMatrix()
    glTranslatef(tx2, ty2, 0)
    glScalef(sz2, sz2, sz2)
    glRotatef(r2, 0, 1, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # vermelho
    glVertex3f(0, 3, 0)
    glVertex3f(-2, -2, 0)
    glVertex3f(2, -2, 0)
    glEnd()
    glPopMatrix()
    

    # Triângulo direita (IJKL)
    glPushMatrix()
    glTranslatef(tx3, ty3, 0)
    glScalef(sz3, sz3, sz3)
    glRotatef(r3, 0, 1, 0)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 1)  # azul
    glVertex3f(0, 3, 0)
    glVertex3f(-2, -2, 0)
    glVertex3f(2, -2, 0)
    glEnd()
    glPopMatrix()


def main():
    pygame.init()  # Inicializa o Pygame
    pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)  
    # Cria a janela com buffer duplo (DOUBLEBUF) e suporte OpenGL (OPENGL)
    init()  # Chama a função de inicialização do OpenGL

    global tx1, ty1, tx2, ty2, tx3, ty3, zoom, r1, r2, r3, ex, ey, ez, sz1, sz2, sz3  # Declara as variáveis globais para uso dentro da função

    running = True  # Variável de controle do loop principal
    while running:
        for event in pygame.event.get():  # Captura eventos do sistema (teclado, mouse, etc.)
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                running = False  # Sai do loop e encerra o programa
            if event.type == KEYDOWN:  # Se uma tecla for pressionada
                if event.key == K_ESCAPE:  # Se a tecla ESC for pressionada
                    running = False  # Sai do loop e fecha o programa
                # Triângulo central – setas
                if event.key == K_LEFT:
                    tx1 -= 0.2
                if event.key == K_RIGHT:
                    tx1 += 0.2
                if event.key == K_UP:
                    ty1 += 0.2
                if event.key == K_DOWN:
                    ty1 -= 0.2

                # Triângulo da esquerda – WASD
                if event.key == K_a:
                    tx2 -= 0.2
                if event.key == K_d:
                    tx2 += 0.2
                if event.key == K_w:
                    ty2 += 0.2
                if event.key == K_s:
                    ty2 -= 0.2

                # Triângulo da direita – IJKL
                if event.key == K_j:
                    tx3 -= 0.2
                if event.key == K_l:
                    tx3 += 0.2
                if event.key == K_i:
                    ty3 += 0.2
                if event.key == K_k:
                    ty3 -= 0.2

                # Zoom individual (escala) de cada triângulo
                # Triângulo central: Z / X
                if event.key == K_z:
                    sz1 += 0.1
                if event.key == K_x:
                    sz1 = max(0.1, sz1 - 0.1)

                # Triângulo da esquerda: R / F
                if event.key == K_r:
                    sz2 += 0.1
                if event.key == K_f:
                    sz2 = max(0.1, sz2 - 0.1)

                # Triângulo da direita: U / O
                if event.key == K_u:
                    sz3 += 0.1
                if event.key == K_o:
                    sz3 = max(0.1, sz3 - 0.1)

                # Zoom global com PageUp/PageDown (câmera)
                if event.key == K_PAGEUP:
                    zoom += 0.2
                if event.key == K_PAGEDOWN:
                    zoom -= 0.2

                    
        # Limpa a tela e o buffer de profundidade antes de desenhar
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Chama a função que desenha o triângulo
        draw()
        
        # Atualiza a tela com a nova renderização
        pygame.display.flip()

        # Aguarda um pequeno tempo para suavizar a execução
        pygame.time.wait(10)

        # Atualiza o ângulo de rotação para dar efeito de giro contínuo
        r1 -= 2   # triângulo central
        r2 -= 4   # triângulo da esquerda
        r3 -= 6   # triângulo da direita

    pygame.quit()  # Finaliza o Pygame quando o loop termina

# Executa o programa se ele for chamado diretamente
if __name__ == "__main__":
    main()