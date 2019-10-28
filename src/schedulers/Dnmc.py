# ESCALONADOR DE PRIORIDADE DINAMICA ######
## CLASS DNMC                       #######
###

from src.models.bcp import BCP              # BLOCO DE CONTROLE DE PROCESSO
from src.models.Queue import Queue as Q     # FILA CIRCULAR

from random import randint                  # biblioteca da função randint

class DNMC: 
  def __init__(self, IO):
    self.__A = Q(False)            # Fila dos processos que não usaram todo o Quantum, prioridade interna do processo
    self.__B = Q(False)            # RR, sem prioridades, Quantum fixo, CPU Bound. 
    self.__Bloq = Q(True)     # Fila de bloqueados
    self.__Quantum = 1  # Quantum RR B()
    self.__IO = IO            # IO = [2] com o tempo/interval de IO

  def isTheEnd(self):                         # 1 se não há mais processos para serem escalonados, 0 caso contrário
    if(self.__A.isEmpty() and self.__B.isEmpty() and self.__Bloq.isEmpty()):
      return True

    return False

  def getFromA(self):                         # insere o processo na fila A
    return self.__A.pop()
  
  def putOnA(self, proc):                     # insere o processo na fila A
    self.__A.append(proc)

  def getFromB(self):                         # insere o processo na fila B
    return self.__B.pop()

  def putOnB(self, proc):                     # insere o processo na fila B
    self.__B.append(proc)

  def getFromBloq(self):                      # insere o processo na fila B
    return self.__Bloq.pop()

  def putOnBloqu(self, proc):                 # insere o processo na fila A
    self.__Bloq.append(proc)
  
  def getIOtime(self):                        # retorna o tempo de IO definido no arquivo de configuração
    if(len(self.__IO) == 2): # Caso seja um intervalo
      return randint(self.__IO[0], self.__IO[1])# calcula um valor aleatório no intervalo IO[0] ... IO[1]

    return self.__IO 

  def getQuantum(self):                       # retorna o quantum
    return self.__Quantum

  def changePriority(self, proc) :              # Calcula e atualiza a prioridade do processo com base no quantum consumido
    proc.procPriority = proc.procQtCons/100

