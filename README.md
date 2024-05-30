# Repositório para o 3° trabalho da disciplina de Grafos (DIM0549 - T01 - 2024.1) da UFRN.

Aluno: Carlos Eduardo. Matrícula: 20220041017.
#

O objetivo deste programa é, dada uma imagem, segmentá-la de modo a destacar elementos. Este algoritmo utiliza conhecimentos da Teoria Espectral dos Grafos e foi fortemente inspirado na proposta apresentada em [*Spectral Image Segmentation using Image Decomposition and Inner Product-based metric*](https://sites.icmc.usp.br/apneto/pub/spectral_jmiv13.pdf) por Wallace Casaca et al.

## Execução

### Método 1
Para utilizar o programa, execute o arquivo ```main.py``` com um interpretador Python com versão 3.10 ou acima.
Sugestões de comandos de execução: ```python main.py``` ou ```python3 main.py```.

São necessárias as seguintes bibliotecas externas: `numpy`, `Python Imaging Library (PIL)` e `scipy`.

### Método 2
No Windows, há também a opção de rodar o executável `main.exe`, não necessitando de um interpretador Python nem das bibliotecas externas. Sugestão de comando de execução: `./main.exe`.

Similarmente, no Linux, tem-se a seguinte sugestão de comando: `./main_linux`. 

### Após execução

Após executar o programa, um menu deve aparecer com instruções de como escolher uma imagem para teste. (Dica: caso não queira abrir o menu toda vez, há um terceiro método de execução similar ao Método 1:  `python main.py <caminho da imagem>`).

Os resultados são salvos em `results` e os relatórios de execução em `reports`.

## Bancos de Dados

Há dois bancos de dado no projeto, [*Berkeley Data Base*](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) (mais especificamente [esta](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/gray/test-001-025.html) página) em `berkeley_tests` e um de criação própria denominado *test_files* em `test_files`. Vale notar que há uma versão da *Berkeley Data Base* com uma resolução menor em `berkeley_tests_low_res`.
