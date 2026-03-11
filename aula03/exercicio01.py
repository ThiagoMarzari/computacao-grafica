import numpy as np
import matplotlib.pyplot as plt


# Função para calcular a translação dos pontos
def translacao(pontos, Tx, Ty):
	pontos_transladados = []
	for ponto in pontos:
		x_u = ponto[0] + Tx
		y_u = ponto[1] + Ty
		pontos_transladados.append((x_u, y_u))
	return pontos_transladados


# Pontos originais
p1 = (0, 0)
p2 = (2, 2)
p3 = (8, 5)

# Vetor de translação
Tx = 3
Ty = 2

# Calcular a translação dos pontos
pontos_transladados = translacao([p1, p2, p3], Tx, Ty)

# Plotar os pontos originais e os pontos transladados
plt.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], "bo-", label="Pontos originais")

# Plotar os pontos transladados da mesma forma
# Pegando o X do primeiro [0][0] e o X do segundo [1][0]
lista_x = [pontos_transladados[0][0], pontos_transladados[1][0], pontos_transladados[2][0]]

# Pegando o Y do primeiro [0][1] e o Y do segundo [1][1]
lista_y = [pontos_transladados[0][1], pontos_transladados[1][1], pontos_transladados[2][1]]
plt.plot(lista_x, lista_y, "ro-", label="Pontos transladados")

# Definir os limites dos eixos
plt.xlim(-5, 7)  # Define o limite do eixo X de 0 a 10
plt.ylim(-5, 7)  # Define o limite do eixo Y de 0 a 10

# Configurações do gráfico
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Translação de pontos no plano cartesiano")
plt.grid(True)
plt.legend()

# Mostrar o gráfico
plt.show()