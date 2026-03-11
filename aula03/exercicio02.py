import os

import matplotlib.pyplot as plt


def translacao(pontos, tx, ty):
	pontos_transladados = []
	for x, y in pontos:
		pontos_transladados.append((x + tx, y + ty))
	return pontos_transladados


def plotar(pontos_originais, pontos_transformados, titulo):
	x0 = [p[0] for p in pontos_originais]
	y0 = [p[1] for p in pontos_originais]
	xt = [p[0] for p in pontos_transformados]
	yt = [p[1] for p in pontos_transformados]

	plt.plot(x0, y0, "bo-", label="Originais")
	plt.plot(xt, yt, "ro-", label="Transladados")
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.title(titulo)
	plt.grid(True)
	plt.legend()


def main():
	headless = os.environ.get("HEADLESS") == "1"

	# Exercício 02 (slide 8): aplicar translação nos pontos do exemplo
	pontos = [(0, 0), (2, 2), (8, 5)]
	tx, ty = 3, 2
	pontos_t = translacao(pontos, tx, ty)

	print("Exercício 02 (slide 8)")
	print(f"Pontos originais: {pontos}")
	print(f"Vetor de translação: Tx={tx}, Ty={ty}")
	print(f"Pontos transladados: {pontos_t}")

	plt.figure()
	plotar(pontos, pontos_t, "Exercício 02 (Slide 8) — Translação")

	# Teste adicional: exemplo 3b (pontos diferentes, mesma operação)
	pontos_3b = [(2, 2), (4, 4)]
	tx_3b, ty_3b = -2, 3
	pontos_3b_t = translacao(pontos_3b, tx_3b, ty_3b)

	print("\nExemplo 3b) (teste)")
	print(f"Pontos originais: {pontos_3b}")
	print(f"Vetor de translação: Tx={tx_3b}, Ty={ty_3b}")
	print(f"Pontos transladados: {pontos_3b_t}")

	plt.figure()
	plotar(pontos_3b, pontos_3b_t, "Exemplo 3b) — Translação (teste)")

	if headless:
		out1 = os.path.join(os.path.dirname(__file__), "exercicio02_slide8.png")
		out2 = os.path.join(os.path.dirname(__file__), "exercicio02_exemplo3b.png")
		plt.figure(1)
		plt.savefig(out1, dpi=150, bbox_inches="tight")
		plt.figure(2)
		plt.savefig(out2, dpi=150, bbox_inches="tight")
		print(f"\nFiguras salvas em:\n- {out1}\n- {out2}")
	else:
		plt.show()


if __name__ == "__main__":
	main()
