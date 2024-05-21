from image_segmentation import image_segmentation

filename = "test_files/test1.png"
smallest_segment_size = 256

print("--------------------------")
print("Welcome! | Bem-vindo!\n")
print("--------------------------\n")
print("Choose you language | Escolha sua língua")
i = int(input("0 - English | 1 - Portuguese\n"))

if i == 0:
	line1 = "This is a program that segments images with the intention of higlighting certain elements."
	line2 = "Please, input the path to the file you want the program to run on"
	line3 = "Processing... This process is O(n) so please be patient"
	line4 = "Done! Generated file "

if i == 1:
	line1 = "Esse é um programa que segmenta imagens com a intenção de destacar certos elementos."
	line2 = "Por favor, insira o caminho para o arquivo o qual você deseje que o programa processe"
	line3 = "Processando... Esse processo é O(n) então por favor tenha paciência"
	line4 = "Pronto! Criado arquivo "
	
if i != 1 and i != 0:
	print("Lingua inválida...terminando o programa")
	exit()

print(line1)
print(line2 + " (Ex: test_files/test1.png)")
filename = input("")

print(line3)

generatedfile_name = image_segmentation(filename, smallest_segment_size)

print(line4 + generatedfile_name)