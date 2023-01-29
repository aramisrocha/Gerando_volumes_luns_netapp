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


# Gerando um volume
def criar_volumes():
 global qtd, valor_inicial, vserver, aggr, volume, tamanho_volume
 tamanho_volume = tamanho_lun + (tamanho_lun * 0.2)
 x = 0
 while x < qtd:
      vol =  (f"vol create -vserver {vserver} -volume {volume}_{valor_inicial} -aggregate {aggr} -size {tamanho_volume}G -state online -space-guarantee none -tiering-policy none -snapshot-policy none")
      valor_inicial = valor_inicial + 1
      x = x + 1
      print(vol)

# Gerando LUN
def criar_luns():
   global qtd, valor_inicial, vserver, volume, tamanho_lun
   x = 0
   while x < qtd:
      lun_name = volume.replace('vol', 'lun')
      lun =  (f"lun create -vserver {vserver} -path /{volume}_{valor_inicial}/{lun_name}_{valor_inicial} -size {tamanho_lun}G -ostype {ambiente_destino} -space-reserve disabled -space-allocation disabled -class regular " )
      valor_inicial = valor_inicial + 1
      x = x + 1
      print(lun)  

# Gerando o LUN MAP

def map_lun():
  global qtd, vserver, valor_inicial, volume


criar_volumes()
criar_luns()


# Gerando os arquivos
