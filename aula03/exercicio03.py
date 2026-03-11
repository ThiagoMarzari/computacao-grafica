import matplotlib.pyplot as plt


# Função para calcular a escala dos pontos
def escala(pontos, Sx, Sy):
	pontos_escala = []
	for ponto in pontos:
		x_u = ponto[0] * Sx
		y_u = ponto[1] * Sy
		pontos_escala.append((x_u, y_u))
	return pontos_escala


# Pontos originais
p1 = (-1, -1)
p2 = (1, 1)

# Fatores de escala
Sx = 2
Sy = 2

# Calcular a escala dos pontos
pontos_escala = escala([p1, p2], Sx, Sy)
print("Pontos escalados:")
for ponto in pontos_escala:
	print(ponto)

# Plotar os pontos originais e os pontos escalados
plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "bo-", label="Pontos originais")

# 1. Primeiro, damos nomes claros aos pontos que a função criou
p1_esc = pontos_escala[0]  # Ponto 1 escalado
p2_esc = pontos_escala[1]  # Ponto 2 escalado

# 2. Agora criamos as listas para o gráfico usando nomes
lista_x = [p1_esc[0], p2_esc[0]]  # Pega o X do primeiro e o X do segundo
lista_y = [p1_esc[1], p2_esc[1]]  # Pega o Y do primeiro e o Y do segundo

# 3. O plot fica limpo
plt.plot(lista_x, lista_y, "ro-", label="Pontos escalados")

# Definir os limites dos eixos
plt.xlim(-7, 10)  # Define o limite do eixo X de 0 a 15
plt.ylim(-7, 10)  # Define o limite do eixo Y de 0 a 15

# Configurações do gráfico
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Escala de pontos no plano cartesiano")
plt.grid(True)
plt.legend()

# Mostrar o gráfico
plt.show()