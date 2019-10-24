# import src.Gerenciador
import sys
import array as arr
from src.models.bcp import BCP

def getConfigurations(filename): # pega o tempo de I/O de cada escalonador de um arquivo de configuração 
  scheduler = ""
  RR = []   # vetor com os valores do processamento de I/O utilizando o algoritmo Round Robin
  DNMC = [] # // utilizando o escalonador com prioridade dinâmica
  SJF = []  # // utilizando o escalonador SJF
  flag = 0

  with open(filename) as f:   # abre o arquivo 
    while True:               # até o fim do arquivo 
      c = f.read(1)           # lê caractere por caractere
      if not c:               # caso seja o final do arquivo
        print ("End of file") 
        break

      # IDENTIFICA COMO NOME DO ESCALONADOR SOMENTE O QUE ESTIVER ENTRE '*' E ':'
      if(c == ':'):  
        flag = 0          # nega a leitura do nome do escalonador
        
      if(flag):           # caso esteja autorizado a leitura:
        scheduler = scheduler + c  # insere caractere por caractere na string 

      if(c == '*'):       # autoriza a leitura do nome do escalonador
        flag = 1
        scheduler = ""
        # i = 0
      # -------------------------------------------------------------------------
      
      if(not flag):       # pega o valor após o ":"  
        if(c != ' ' and c != ',' and c != ':' and c != '\n'): 

          if(scheduler == 'RR'):
            RR.append(int(c))

          if(scheduler == 'DNMC'):
            DNMC.append(int(c))

          if(scheduler == 'SJF'):
            SJF.append(int(c))

  return [RR,DNMC,SJF]

def getProcess(filename):   #Adiciona os processos a uma lista de processos
  processList = []
  singleProcess = []
  
  with open(filename) as f:
    for val in f.read().splitlines():
      for i in val.strip().split():
        singleProcess.append(int(i))
      processList.append(singleProcess)
      singleProcess = []
      
  return processList

def main():
    print(getConfigurations(sys.argv[1]))
    print (getProcess(sys.argv[2]))

main()