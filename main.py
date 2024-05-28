import sys
from os.path import exists

from image_segmentation import image_segmentation


filename = "berkeley_tests/295087.jpg"
smallest_segment_size = 256
state = 1

# User input in command line
if len(sys.argv) > 1:
	filename = sys.argv[1]
	state = 2

# Receiving user input
if state == 1:
	print("--------------------------")
	print("Bem-vindo!\n")
	print("--------------------------\n")

	print("Esse é um programa que segmenta imagens com a intenção de destacar certos elementos.\n")
	i = input("Digite:\n0 - Para escolher um teste no banco de dados.\n1 - Para sair do programa.\n")

	if i == "1":
		sys.exit()

	if i == "0":
		print("Por favor, insira o caminho para o arquivo o qual você deseje que o programa processe (Ex: test_files/test1.png).")
		filename = input("")
		state = 2
		
	if i != "1" and i != "0":
		print("Entrada inválida!")
		sys.exit(0)

# Running the program
if state == 2:

	if not exists(filename):
		print("Arquivo não encontrado, verifique se digitou corretamente.")
		print("Terminando programa.")
		sys.exit(0)

	print("--------------------------")
	print("Processando... Esse processo é O(n) então por favor tenha paciência.")
	print("--------------------------\n")

	generatedfile_name, reportfile_name = image_segmentation(filename, smallest_segment_size)

	print("--------------------------\n")

	print("Arquivo criado em: " + generatedfile_name)
	print("Relatório de execução salvo em: " + reportfile_name)
