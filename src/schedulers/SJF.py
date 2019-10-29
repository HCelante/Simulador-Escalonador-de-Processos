# ESCALONADOR SHORTEST JOB FIRST

from src.models.bcp import BCP
from random import randrange

class SJF: 
  def __init__(self, confs):
    self.minIOTime = confs[0]
    self.maxIOTime = confs[1]
    self.IOTime = self.randomIOTime()
  
    
  def executeSJF(self, bcp, timestamp):       # executa o SJF no bcp

    for i in range (len(bcp.procIOTime)):       # verifica a lista de IO do processo
      if (bcp.procIOTime[i] == bcp.procCPUuse): # se o evento for acionado
        print("\nProcesso "+ str(bcp.procID) +" bloqueado para IO, durante " + str(self.IOTime) + " unidades de tempo\n")
        bcp.timeBlockRemain = self.IOTime       # atribui o tempo de bloqueio
        bcp.procState = -1                      # altera o estado
        bcp.procIOTime.pop(i)                   # remove o evento da lista do bcp
        break

    if (bcp.procState == 0 or bcp.procState == 1):  # caso o processo esteja executando
      if (bcp.procBurstTime > 0 ):                  # e o bt não for zerado
        bcp.procState = 1                           # aplica os valores no bcp
        bcp.procBurstTime -= 1
        bcp.procCompletionTime = timestamp
        bcp.procCPUuse += 1
      else:                                         # se o bt for 0
        bcp.procState = 2                           # o processo recebe o estado de finalizado

    return bcp

  def selectProc (self, ReadyQueue):  # seleciona o processo mais apto para a execução
    selectedIndex = 0
    burstTest = 999999999
    
    for i in range(len(ReadyQueue.sentinel)):                 # testa todos os processos da fila de pronto
      if (ReadyQueue.sentinel[i].procBurstTime < burstTest):  # verifica se o bt é o menor
        burstTest = ReadyQueue.sentinel[i].procBurstTime
        selectedIndex = i
        
    return selectedIndex, burstTest                           # retorna a posição do processo na lista e o bt
  
  def randomIOTime(self):   # define um valor aleatório para eventos de IO
    value = randrange(self.minIOTime, self.maxIOTime)
    return value