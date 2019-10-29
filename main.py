# import src.Gerenciador
import sys
import array as arr
from src.models.bcp import BCP
from src.Gerenciador import Manager

def getConfigurations(filename):  # pega o tempo de I/O de cada escalonador de um arquivo de configuração 
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

def getProcess(filename):         # Adiciona os processos a uma lista de processos
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
    confs = getConfigurations(sys.argv[1])  # contém as informações de execução do IO de todos os escalonadores 
    procList = getProcess(sys.argv[2])      # contém os processos a serem escalonados
    
    mainProcess = []
    for i in range (len(procList)):
      mainProcess.append(BCP(procList[i]))
    # print(mainProcess[0].procIOTime)
    # print(type(mainProcess[0]))

    rrProcess = mainProcess.copy()  # cópia dos processos
    sjfProcess = mainProcess.copy()
    dnmcProcess = mainProcess.copy()
    
    # # Recebe o numero de filas
    # nfilas = 1
    
    # # # Instanciando a classe Manager
    # Managed = Manager(nfilas)
    
    # # # Populando a fila de nao criados
    # Managed.construc_QNC(sjfProcess)
    # Managed.exec_loop('SJF', confs)

   
    # Managed.reset_Manager(nfilas)

    # Managed2 = Manager(1)
    # Managed2.construc_QNC(rrProcess)
    # Managed2.exec_loop('RR', confs)
    
    # Exec DNMC -----------------------
    Managed3 = Manager(2)
    Managed3.construc_QNC(dnmcProcess)
    Managed3.exec_loop('DNMC', confs)


main()