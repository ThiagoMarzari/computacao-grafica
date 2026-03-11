import matplotlib.pyplot as plt

# Vamos modelar o nosso 'cubo' utilizando a linguagem python:
# a) Passo 1: definir as coordenadas de cada ponto
# Definição dos pontos que definem os vértices do cubo
P1 = (-0.5, -0.5, -0.5)
P2 = (-0.5, -0.5,  0.5)
P3 = (-0.5,  0.5, -0.5)
P4 = (-0.5,  0.5,  0.5)
P5 = ( 0.5, -0.5, -0.5)
P6 = ( 0.5, -0.5,  0.5)
P7 = ( 0.5,  0.5, -0.5)
P8 = ( 0.5,  0.5,  0.5)

arestas = [(P1, P2), (P2, P4), (P4, P3), (P3, P1),
           (P5, P6), (P6, P8), (P8, P7), (P7, P5),
           (P1, P5), (P2, P6), (P3, P7), (P4, P8)]

# Plotando o cubo
fig = plt.figure()  # Criando uma figura
ax = fig.add_subplot(projection='3d')  # Adicionando um subplot tridimensional à figura
# Plotando as arestas do cubo
for aresta in arestas:
    ponto1 = aresta[0]  # Obtendo as coordenadas do primeiro ponto da aresta (x,y,z)
    ponto2 = aresta[1]  # Obtendo as coordenadas do segundo ponto da aresta (x,y,z)
    # Plotando uma linha entre os dois pontos para representar a aresta
    ax.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], [ponto1[2], ponto2[2]], 'g')
    # Coordenadas 3D (x,y,z)
# Configurações do gráfico 3D
ax.set_xlabel('X')  # Configurando o rótulo do eixo x
ax.set_ylabel('Y')  # Configurando o rótulo do eixo y
ax.set_zlabel('Z')  # Configurando o rótulo do eixo z
ax.set_title('Cubo no Espaço 3D')  # Configurando o título do gráfico
ax.set_xlim(-0.5, 0.5)  # Limites do eixo X * 
ax.set_ylim(-0.5, 0.5)  # Limites do eixo Y
ax.set_zlim(-0.5, 0.5)  # Limites do eixo Z
# Adicionando manualmente uma legenda para o eixo Z
ax.text(0.7, 0.5, 0.6, 'Z', color='black')  # Adicionando o texto 'Z' na posição desejada
# Mostrando o gráfico
plt.show()