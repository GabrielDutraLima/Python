"""nome = input("Digite seu nome: ")
altura = float(input("Digite sua altura: "))
peso = float(input("Digite seu peso: "))

 

imc = peso / (altura * altura)

print(
    f'{nome} tem {altura} de altura, \n pesa {peso} quilos e seu IMC é {imc:.2f}'

)

primeiroValor = int(input("Digite qualquer numero: ")) 
segundoValor = int(input("Digite qualquer numero: ")) 


if primeiroValor > segundoValor:
    print(
        f'O numero {primeiroValor} é maior que o numero {segundoValor}'
        )

else:
    print(
        f' O numero {segundoValor} é maior que o numero {primeiroValor}'
          )       
 
numero_str = input("Digite um numero: ")


try:
    numero_int = int(numero_str)
    
    if numero_int >= 0:
        print(f'O numero {numero_int} é par')

    else:
        print(f'O numero {numero_int} é impar')    

except:
    print("Esse numero não é inteiro!!")
 

horasRecebidas = input("Digite que horas são agora: ")

try:
    horasConvertidas = int(horasRecebidas)

    if horasConvertidas >= 0 and horasConvertidas <= 11:
        print("Bom dia")
    elif horasConvertidas >= 12 and horasConvertidas <= 17:
        print("Boa tarde")
    else:
        print("Boa noite")    


except:
    print("Digite um valor valido Ex: 07 | 8 | 22")



nomeRecebido = input("Digite seu nome: ")


try:
    nomeConvertido = len(nomeRecebido)
    if nomeConvertido <= 4:
        print("Seu nome é curto")

    elif nomeConvertido <= 6:
        print("Seu nome é normal")

    else:
        print("Seu nome é grande")    


except:
    print("Você não digitou um nome !!")



numeroDigitado = int(input("Digite um numero: "))

contador = 0
numero = 0 
lista = []


while contador <= 5:
    numero = numeroDigitado + numero
    contador += 1
    lista.append(numero)
   
print(lista)



nome = 'Gabriel Dutra'


contador = 0 
novoNome = ''

while contador < len(nome):
    letra = nome[contador]
    novoNome += f' {letra}'
    contador += 1


print(novoNome)



    

while True:
    primeiroNumeroRecebido = input("Digite o primeiro numero: ")
    segundoNumeroRecebido = input("Digite o segundo numero: ")
    operador = input("Escolha o operador (+ - * /): ")

    numeros_validos = None
    operador_valido = '+-*/'
    try:
        num_1 = float(primeiroNumeroRecebido)
        num_2 = float(segundoNumeroRecebido)
        numeros_validos = True

    except:
        numeros_validos = None

    if numeros_validos is None:
        print(f'Um dos numeros digitados esta incorreto!!  {primeiroNumeroRecebido} ou {segundoNumeroRecebido}')    
        continue

    if operador not in operador_valido:
        print("Operador invalido!!")
        continue
    if operador == '+':
        print(f'{num_1} + {num_2} = {num_1 + num_2}')
    elif operador == '-':
        print(f'{num_1} - {num_2} = {num_1 - num_2}')    
    elif operador == '*':
        print(f'{num_1} x {num_2} = {num_1 * num_2}')    
    else:
        print(f'{num_1} / {num_2} = {num_1 / num_2}')    

    sair = input("Deseja sair? [s]im: ").lower().startswith('s')
    
    if sair is True:
        break


resultado = 0

def soma(x, y):
    if x > 5:
        
        return   x + y
    else:
        return (f'{x} é menor que 5')
    

  
resultado = soma(3, 9)

print(resultado)




def multi(*args):
    resultado = 1

    for i in args:
        resultado *= i  
    return resultado
    
result = multi(6, 7, 9)


def Verification(result):
    
    if result % 2 == 0:
        return (f'O numero {result} é Par')
  
    return (f'O numero {result} é Impar')

verf = Verification(result)

print(verf)



num_1 = input('Digite um numero: ')
print("Você quer [D]uplicar | [T]riplicar | [Q]uadruplicar")
entrada = input()
controle = entrada.lower()
primeiroNumero = int(num_1)


def criarMultiplicador(multiplicador):
    def multi(numero):
        return numero * multiplicador
    return multi
duplicar = criarMultiplicador(2)
triplicar = criarMultiplicador(3)
quadruplicar = criarMultiplicador(4)



if controle == 'd':
    resultado = duplicar(primeiroNumero)
    print(resultado)

elif controle == 't':
    resultado = triplicar(primeiroNumero)
    print(resultado)

elif controle == 'q':
    resultado = quadruplicar(primeiroNumero)
    print(resultado)

else:
    print("Opção invalida!!")


O Hipermercado Tabajara está com uma promoção de carnes que é imperdível. Confira:
                      Até 5 Kg           Acima de 5 Kg
File Duplo      R$ 4,90 por Kg          R$ 5,80 por Kg
Alcatra         R$ 5,90 por Kg          R$ 6,80 por Kg
Picanha         R$ 6,90 por Kg          R$ 7,80 por Kg
Para atender a todos os clientes, cada cliente poderá levar apenas um dos tipos de carne da promoção, porém não há limites para a quantidade de carne por cliente. Se compra for feita no cartão Tabajara o cliente receberá ainda um desconto de 5% sobre o total da compra.

 Escreva um programa que peça o tipo e a quantidade de carne comprada pelo usuário e gere um cupom fiscal, contendo as informações da compra: tipo e quantidade de carne, preço total, tipo de pagamento, valor do desconto e valor a pagar.
   
 


def porcentagem(numero, porcento):
        return (porcento * numero) / 100

porcentagens = set()
somas = set()




while True:
    n1 = int(input('Digite um numero: '))
    pergunta = input('Quer fazer porcentagem? [SIM] ou [NÃO]: ')

    if pergunta.lower() == 'sim':
        porcento = int(input('Digite a porcentagem: '))
        porcentagens.add(porcentagem(n1, porcento))
        #print(porcentagem(n1, porcento))
    else:
         n2 = int(input('Digite mais um numero: '))
         soma = n1 + n2
         somas.add(soma)
         #print(soma)
    saida = input('Quer sair? [1]: ')

    if saida == '1':
         print(porcentagens, somas)
         break
    


# Introdução à função lambda (função anônima de uma linha)
# A função lambda é uma função como qualquer
# outra em Python. Porém, são funções anônimas
# que contém apenas uma linha. Ou seja, tudo
# deve ser contido dentro de uma única
# expressão.
# lista = [
#     {'nome': 'Luiz', 'sobrenome': 'miranda'},
#     {'nome': 'Maria', 'sobrenome': 'Oliveira'},
#     {'nome': 'Daniel', 'sobrenome': 'Silva'},
#     {'nome': 'Eduardo', 'sobrenome': 'Moreira'},
#     {'nome': 'Aline', 'sobrenome': 'Souza'},
# ]
# lista = [4, 32, 1, 34, 5, 6, 6, 21, ]
# lista.sort(reverse=True)
# sorted(lista)
lista = [
    {'nome': 'Luiz', 'sobrenome': 'miranda'},
    {'nome': 'Maria', 'sobrenome': 'Oliveira'},
    {'nome': 'Daniel', 'sobrenome': 'Silva'},
    {'nome': 'Eduardo', 'sobrenome': 'Moreira'},
    {'nome': 'Aline', 'sobrenome': 'Souza'},
]


def exibir(lista):
    for item in lista:
        print(item)
    print()


l1 = sorted(lista, key=lambda item: item['nome'])
l2 = sorted(lista, key=lambda item: item['sobrenome'])

exibir(l1)
exibir(l2)

cadastros = [
    {'nome': 'João', 'rua': 'Avenida Paulista', 'numero': 1583},
    {'nome': 'Fernanda', 'rua': 'Teodoro Sampaio', 'numero': 834},
    {'nome': 'Bianca', 'rua': 'Avenida Paulista', 'numero': 912}
]


#def mostrar(cadastro):
#    for item in cadastro:
#        print(item)

def ordena(item):
    return item['rua']

cadastros.sort(key=lambda item: item['numero'])   # Lambda funciona como um def para ordenar um dicionario

for item in cadastros:
    print(item)


cadastros = [
    {'nome': 'João', 'rua': 'Avenida Paulista', 'numero': 1583},
    {'nome': 'Fernanda', 'rua': 'Teodoro Sampaio', 'numero': 834},
    {'nome': 'Bianca', 'rua': 'Avenida Paulista', 'numero': 912}
]



def mostrar(cadastros):
    for item in cadastros:
         print(item)
    print()     

lista1 = sorted(cadastros, key=lambda item: item['nome'])
lista2 = sorted(cadastros, key=lambda item: item['rua'])


mostrar(lista1)
mostrar(lista2)


lista = [ 
    numero * 2 
    for numero in range(10)
]


 
print(lista)



carnes = [
    {'tipo' : 'File Duplo','id' : 1,  'valor' : 4.90},
    {'tipo' : 'Alcatra','id' : 2,'valor' : 5.90},
    {'tipo' : 'Picanha','id' : 3,'valor' : 6.90}
]


novasCarnes = [
        carne['valor']
        for carne in carnes
  ]

print(*novasCarnes, sep='\n')


lista = [1,2,3,4,5]

novaLista = [numero for numero in lista]

print(novaLista)



lista = [1,2,3,4,5,6]
soma = [numero + 2 for numero in lista]
sub = [numero - 2 for numero in lista]
multi = [numero * 2 for numero in lista]
divi = [numero / 2 for numero in lista]
quad = [numero ** 2 for numero in lista]

print(soma)
print(sub)
print(multi)
print(divi)
print(quad)
"""

def soma(x, y):
    return x + y

def multi(x, y):
    return x * y 

def potencia(x, y):
    return x ** y


lista = [1, 2, 3, 4, 5, 6, 7]

listaSoma = [soma(numero, 2) for numero in lista]
listaMulti = [multi(numero, 2) for numero in lista]
listaPot = [potencia(numero, 2) for numero in lista]



print(listaSoma)
print(listaMulti)
print(listaPot)
















