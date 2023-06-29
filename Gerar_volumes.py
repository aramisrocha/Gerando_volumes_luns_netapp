# Script para autmatizar a criação de luns e esoelhamento de LUN no ambiente NETAPP
# Autor: Aramis de Oliveira Andrade Rocha



qtd = int(input("Entrar com a quantidade de Luns: "))
valor_inicial = int(input("Entrar com o valor inicial das luns: "))
tamanho_lun = int(input("Entrar com tamanho da LUN em GB: "))
vserver = input("Entrar com o Vserver: ")
aggr = input("Entrar com o aggregate: ")
volume = input("Entrar com o nome do volume começando vol: ")
ambiente_destino = input("Qual plataforma de destino (vmware, linux, aix): ")
igroup = input("Entrar com o igroup para mapear: ")
resposta_espelhamento = input("Este volume terá espelhamento? (SIM/NÃO): ")


def limpar_arquivo_bkp():
    with open('bkp.txt', 'w') as f:
         f.write('')

def espelhamento(aggr_bkp, vserver_bkp):
    global qtd, vserver, valor_esp, volume, igroup, tamanho_lun, tamanho_volume
    valor_esp = valor_inicial
    tamanho_volume = tamanho_lun + (tamanho_lun * 0.2)
    x = 0
    with open('bkp.txt', 'a') as f:
        while x < qtd:
            vol_esp = f"volume create -volume {volume}_{valor_esp}_vault -aggregate {aggr_bkp} -size {tamanho_volume:.0f}G -state online -type DP -space-guarantee none -vserver {vserver_bkp}"
            mirror_create = f"snapmirror create -source-path {vserver}:{volume}_{valor_esp} -aggregate {aggr_bkp} -destination-path {vserver_bkp}:{volume}_{valor_esp}_vault"
            mirror_init = f"snapmirror initialize -destination-path {vserver_bkp}:{volume}_{valor_esp}_vault"
            x = x + 1
            valor_esp = valor_esp + 1
            print(vol_esp, file=f)
            print(mirror_create, file=f)
            print(mirror_init, file=f)
            #print(vol_esp, mirror_create, mirror_init, file=f)


# Verificando resposta para espelhamento
while resposta_espelhamento.upper() != "SIM" and resposta_espelhamento.upper() != "NAO":
    print("Opção inválida. Por favor, digite 'SIM' ou 'NAO'.")
    resposta_espelhamento = input("Este volume terá espelhamento? (SIM/NAO): ")

if resposta_espelhamento.upper() == "SIM":
    limpar_arquivo_bkp()
    aggr_bkp = input("Entrar com o aggregate de Backup: ")
    vserver_bkp = input("Entrar com o Vserver de Backup: ")
    espelhamento(aggr_bkp, vserver_bkp)
else:
    print("Sem Espelhamento")


# Realizando limpeza dos arquivos antes de prosseguir


def limpar_arquivo():
    with open('prod.txt', 'w') as f:
         f.write('')


# Gerando um volume
def criar_volumes():
    global qtd, valor_volume, vserver, aggr, volume, tamanho_volume
    tamanho_volume = tamanho_lun + (tamanho_lun * 0.2)
    valor_volume = valor_inicial
    x = 0
    with open('prod.txt', 'a') as f:
        while x < qtd:
            vol = f"vol create -vserver {vserver} -volume {volume}_{valor_volume} -aggregate {aggr} -size {tamanho_volume:.0f}G -state online -space-guarantee none -tiering-policy none -snapshot-policy none"
            valor_volume = valor_volume + 1
            x = x + 1
            print(vol, file=f)


# Gerando LUN
def criar_luns():
    global qtd, valor_lun, vserver, volume, tamanho_lun
    valor_lun = valor_inicial
    x = 0
    with open('prod.txt', 'a') as f:
        while x < qtd:
            lun_name = volume.replace('vol', 'lun')
            lun = f"lun create -vserver {vserver} -path /{volume}_{valor_lun}/{lun_name}_{valor_lun} -size {tamanho_lun}G -ostype {ambiente_destino} -space-reserve disabled -space-allocation disabled -class regular"
            valor_lun = valor_lun + 1
            x = x + 1
            print(lun, file=f)


# Gerando o LUN MAP
def map_lun():
    global qtd, vserver, valor_map, volume, igroup
    valor_map = valor_inicial
    x = 0
    with open('prod.txt', 'a') as f:
        while x < qtd:
            lun_name = volume.replace('vol', 'lun')
            lun_map = f"lun map -vserver {vserver} -path /{volume}_{valor_map}/{lun_name}_{valor_map} -igroup {igroup}"
            x = x + 1
            valor_map = valor_map + 1
            print(lun_map, file=f)


# Lidando com espelhamento
limpar_arquivo()
criar_volumes()
criar_luns()
map_lun()