from socketserver import DatagramRequestHandler


qtd = int(input("Entrar com a quantidade de volumes: "))
valor_inicial =  int(input("Entrar com o valor inicial: "))
# tamanho_volume = int(input("Entrar com o tamanho do volume: "))
tamanho_lun = int(input("Entrar com tamanho da LUN em GB : "))
vserver = (input("Entrar com o Vserver: "))
aggr = (input("Entrar com o aggregate: "))
volume = (input("Entrar com o nome do volume começando vol:"))
#lun = (input("Entrar com o nome da LUN"))
ambiente_destino = (input("Entrar com o ambiente de destino vmware, linux, aix: "))
espelhamento = input("Este volume terá espelhamento? (SIM/NÃO): ")
igroup = (input("Entrar com o igroup para mapear: "))

while espelhamento.upper() != "SIM" and espelhamento.upper() != "NÃO":
    print("Opção inválida. Por favor, digite 'SIM' ou 'NÃO'.")
    espelhamento = input("Este volume terá espelhamento? (SIM/NÃO): ")

if espelhamento.upper() == "SIM":
    
    print("Você escolheu SIM.")
else:
    
    print("Você escolheu NÃO.")






# Gerando um volume
def criar_volumes():
    global qtd, valor_volume, vserver, aggr, volume, tamanho_volume
    tamanho_volume = tamanho_lun + (tamanho_lun * 0.2)
    valor_volume = valor_inicial
    x = 0
    with open('prod.txt', 'a') as f:  # Abre o arquivo em modo de adição (append)
        while x < qtd:
            vol =  (f"vol create -vserver {vserver} -volume {volume}_{valor_volume} -aggregate {aggr} -size {tamanho_volume}G -state online -space-guarantee none -tiering-policy none -snapshot-policy none")
            valor_volume = valor_volume + 1
            x = x + 1
            print(vol, file=f)  # Grava a saída no arquivo

# Gerando LUN
def criar_luns():
    global qtd, valor_lun, vserver, volume, tamanho_lun
    valor_lun = valor_inicial
    x = 0
    with open('prod.txt', 'a') as f:
        while x < qtd:
            lun_name = volume.replace('vol', 'lun')
            lun =  (f"lun create -vserver {vserver} -path /{volume}_{valor_lun}/{lun_name}_{valor_lun} -size {tamanho_lun}G -ostype {ambiente_destino} -space-reserve disabled -space-allocation disabled -class regular " )
            valor_lun = valor_lun + 1
            x = x + 1
            print(lun, file=f)
    return lun_name

# Gerando o LUN MAP
def map_lun():
    global qtd, vserver, valor_map, volume, igroup
    valor_map = valor_inicial
    #nome_lun = criar_luns()
    x = 0
    with open('prod.txt', 'a') as f:
        while x < qtd:
            lun_name = volume.replace('vol', 'lun')
            lun_map = (f"lun map -vserver {vserver} -path /{volume}_{valor_map}/{lun_name}_{valor_map}  -igroup {igroup}")
            x = x + 1
            valor_map = valor_map + 1
            print(lun_map, file=f)

# Lidando com espelhamento
criar_volumes()
criar_luns()
map_lun()