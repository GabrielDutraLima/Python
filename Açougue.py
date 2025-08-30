import os



carnes = [
    {
    'id' : 1,    
    'tipo' : 'File Duplo',    
    'valor' : 4.90,
    },
    {
    'tipo' : 'Alcatra',
    'id' : 2,
    'valor' : '5,90',
    },
    {
    'tipo' : 'Picanha',
    'id' : 3,
    'valor' : '6,90',
    }
]


print('Escolha um tipo de carne')
print()

subTotal = 0
entrada_int = ''
carneEscolhida = ''
valorDeDesconto = 0
formaDePagamento = ''
valorApagar = 0

for carne in carnes:
    print(carne['id'],')', carne['tipo'])
print()    

entrada = input('Digite o código: ')   
os.system("cls")
kilosComprados = float(input('Digite os kilos: '))
os.system("cls")


if entrada.isdigit():    # Convertendo a entrada em INT | Verificando se é um valor valido
    entrada_int = int(entrada)  
    #print('foi-')

    if entrada_int <= carne['id']:   # Verificando o ID Digitado, se está no dicionário 
          
        if entrada_int == 1:
            
            carneEscolhida = "Filé Duplo"
            if kilosComprados <= 5:   # Verificando os Kilos comprados
                subTotal = (kilosComprados * 4.9)
            else:
                subTotal = (kilosComprados * 5.8)    
        
        elif entrada_int  == 2:   # Verificando o ID Digitado
            carneEscolhida = "Alcatra"
            if kilosComprados <= 5:
                subTotal = (kilosComprados * 5.9)
            else:
                subTotal = (kilosComprados * 6.8)

        elif entrada_int == 3:
            carneEscolhida = "Picanha"
            if kilosComprados <= 5:
                subTotal = (kilosComprados * 6.9)
            else:
                subTotal = (kilosComprados * 7.8)    

    else:   # Verificando o ID Digitado
        print(f'O código digitado {entrada_int} é invalodo')
        
else:   # Convertendo a entrada em INT | Verificando se é um valor valido
    print(f'ERRO o valor digitado " {entrada} " esta invalido')
    


#print(f'{carneEscolhida} {kilosComprados} KG | R$: {subTotal:.2f}')
print()


print('Forma de pagamento')
print('1) Cartão Tabajara')
print('2) Cartão Credito')
print('3) Cartão Debito')
print('4) PIX')
print('5) Dinheiro')
print()
opcaoDePagamento = int(input('Escolha a forma de pagamento: '))
os.system("cls")

if opcaoDePagamento == 1:   # Verificando forma de pagamento
    formaDePagamento = 'Cartão Tabajara'
    valorDeDesconto = (subTotal * 5) / 100

elif opcaoDePagamento == 2:
    formaDePagamento = 'Cartão Credito'


elif opcaoDePagamento == 3:
    formaDePagamento  =  'Cartão Debito' 

elif opcaoDePagamento == 4:
    formaDePagamento = 'PIX'

elif opcaoDePagamento == 5:
    formaDePagamento = 'Dinheiro'        

else:
    print('Opção invalida')        



valorApagar = (subTotal - valorDeDesconto)

print(
    f'        CUPOM FISCAL \n{carneEscolhida}\n{kilosComprados}kg\nSubTotalR$: {subTotal:.2f}\nDesconto R$: {valorDeDesconto:.2f}\nValor Total R$: {valorApagar:.2f}\nForma de pagamento: {formaDePagamento}'
    )


