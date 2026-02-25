import math

# ---- Exercício 01 ----
# Agora tente implementar um código em python para o
# exemplo do slide anterior e fazer a multiplicação das
#matrizes A e B.
# As matrizes já podem iniciar preenchidas e é necessário
# fazer a verificação se o número de colunas da matriz A é
# Igual ao número de linhas da Matriz B. Imprimir as duas
#matrizes e depois imprimir o resultado final.
#OBS: não usar funções prontas para fazer a multiplicação
#das matrizes e sim usar ‘loops for’.

def multiplicar_matrizes(A, B):
  resultado = [[0 for j in range(len(B))] for i in range(len(A))]
  for i in range(len(A)):
    for j in range(len(B)):
      for k in range(len(B)):
        resultado[i][j] += A[i][k] * B[k][j]
  return resultado
  
A = [[2, 0, 0], [0, 1, 0], [0, 0, 1]]
B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print("A matriz resultante da multiplicação é: ", multiplicar_matrizes(A, B))

# ---- Exercício 02 ----
# Operações com matrizes
# Exercícios de aula:
# Agora tente implementar um código em python para o exemplo do
# slide anterior e descobrir se a matriz é diagonal.
# Regras: necessário verificar se a matriz é quadrada (número de
# linhas igual ao número de colunas lxc)
# E todos elementos fora da diagonal são zeros.
# ex: if i != j and A[i][j] != 0:
# eh_diagonal = False

def verificar_matriz_diagonal(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if i != j and matriz[i][j] != 0:
        return False
  return True

A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print("A matriz é diagonal: ", verificar_matriz_diagonal(A))
B = [[1, 0, 0], [0, 1, 0], [0, 2, 2]]
print("A matriz é diagonal: ", verificar_matriz_diagonal(B))

# ---- Exercício 03 ----
# Exercícios de aula:
# Agora tente implementar um código em python para o exemplo do
# slide anterior e descobrir se a matriz é Identidade.
# Regras: necessário verificar se a matriz é quadrada (número de
# linhas igual ao número de colunas lxc)
# E todos elementos da diagonal são igual a ‘1’ e os elementos fora
# da diagonal são igual a ‘0’.
# Ex: if (i == j and A[i][j] != 1) or (i != j and A[i][j] != 0):
# eh_identidade = False

def verificar_matriz_identidade(matriz): 
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if i == j and matriz[i][j] != 1:
        return False
      if i != j and matriz[i][j] != 0:
        return False
  return True

A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print("A matriz é identidade: ", verificar_matriz_identidade(A))
B = [[1, 0, 0], [0, 1, 0], [0, 0, 2]]
print("A matriz é identidade: ", verificar_matriz_identidade(B))

# ---- Exercício 04 ----
# Operações com matrizes
# Exercícios de aula:
# Agora tente implementar um código em python para o
# exemplo do slide anterior e transformar a matriz em
# ‘transposta’.
# Regras:
# Ex: for i in range(linhas):
# for j in range(colunas):
# transposta[j][i] = A[i][j] # Troca linhas por colunas
#
#  def transpor_matriz(matriz):
#    transposta = []
#    for i in range(len(matriz)):
#      for j in range(len(matriz[i])):
#        transposta[j][i] = matriz[i][j]
#    return transposta
#
#  A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#  print("A matriz transposta é: ", transpor_matriz(A))
