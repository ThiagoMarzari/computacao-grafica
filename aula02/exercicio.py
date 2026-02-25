import math
import os
import numpy as np
x = 0
y = 0
z = 0

x2 = 0
y2 = 0
z2 = 0

def limpa_console():
  os.system('cls' if os.name == 'nt' else 'clear')

limpa_console()

def pega_coordenadas():
  print("Digite as coordenadas do vetor:")
  x_input = int(input("x: "))
  y_input = int(input("y: "))
  z_input = int(input("z: "))
  return x_input, y_input, z_input

def calcular_tamanho_vetor(x, y, z):
  return math.sqrt(x**2 + y**2 + z**2)

def subtrair_vetores(x1, y1, z1, x2, y2, z2):
  #converte os vetores para arrays numpy
  v1 = np.array([x1, y1, z1])
  v2 = np.array([x2, y2, z2])
  #subtrai os vetores
  return v1 - v2

def escalar_multiplicar_vetor(x, y, z, escalar):
  return np.array([x, y, z]) * escalar

def escalar_dividir_vetor(x, y, z, escalar):
  return np.array([x, y, z]) / escalar

x, y, z = pega_coordenadas()

while True:
    print("Digite a operação:")
    print("0. Inserir novo vetor")
    print("1. Calcular tamanho do vetor")
    print("2. Normalizar vetor")
    print("3. Adicionar outro vetor")
    print("4. Subtrair vetores")
    print("5. Multiplicar vetor por escalar")
    print("6. Dividir vetor por escalar")
    print("7. Sair")
    op = int(input("Opção: "))
    if op == 0:
        limpa_console()
        x, y, z = pega_coordenadas()
    elif op == 1:
        limpa_console()
        print("Tamanho do vetor: ", calcular_tamanho_vetor(x, y, z))
    elif op == 2:
        limpa_console()
        print("Normalizar vetor: ", normalizar_vetor(x, y, z))
    elif op == 3:
        limpa_console()
        x2, y2, z2 = pega_coordenadas()
        print("Vetor 1: ", x, y, z)
        print("Vetor 2: ", x2, y2, z2)
    elif op == 4:
        limpa_console()
        print("Resultado da subtração de vetores: ", subtrair_vetores(x, y, z, x2, y2, z2))
    elif op == 5:
        limpa_console()
        escalar = int(input("Digite o escalar: "))
        print("Resultado da multiplicação do vetor por escalar: ", escalar_multiplicar_vetor(x, y, z, escalar))
    elif op == 6:
        limpa_console()
        escalar = int(input("Digite o escalar: "))
        print("Resultado da divisão do vetor por escalar: ", escalar_dividir_vetor(x, y, z, escalar))
    elif op == 7:
        limpa_console()
        break
  
