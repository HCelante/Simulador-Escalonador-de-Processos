# GERENCIA DE PROCESSOS ######################
## CLASS MANAGER                    ##########
### METODOS CONTRUTORES             ##########
### METODOS DE GERENCIA             ##########
### METODOS DE FEEDBACK             ##########
##############################################

import sys
#sys.path.append('models')
#print(sys.path)

from src.models.bcp import BCP             # BLOCO DE CONTROLE DE PROCESSO
from src.models.Queue import Queue as Q     # FILA CIRCULAR
from src.schedulers.Dnmc import * # PRIORIDADE DINAMICA
from src.schedulers.SJF import * # JOB SHORTEST FIRST
from src.schedulers.RR  import * # ROUND ROBIN


# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp       = 0                        # tempo da cpu
        self.QueueBloq       = Q(True)            # fila de bloqueados
        self.List_QRdy       = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri       = Q(False)           # fila de processos nao criados
        self.indexQRdy       = 0


    # METODOS DE CONSTRUCAO ######################################################
    def construc_listQ(self, nfilas):
        listqrd = []
        for n in range(nfilas):
            listqrd.append(Q(False))
        return listqrd



    # METODOS DE GERENCIA ########################################################
    def updateQ_Priority(self, cond):                      # consome os processos
        if ("AB" == cond):                               # consome primeiro a e debois b
            if(self.List_QRdy[self.indexQRdy].isEmpty() == True):
                self.indexQRdy = self.indexQRdy + 1

    
    



    # METODOS DE FEEDBACK ########################################################
    def calculaTME(self):                   # calcula tempos medio de espera
        pass

    def calculaTTE(self):                   # calcula tempo total de espera
        pass
    
    def calculaThrgpt(self):                # calcula throughput do sistema
        pass

    def calculaTMTMF(self):                 # calcula tamanho maximo e medio das filas
        pass

    def calculaTRM(self):                   # calcula tempo de resposta medio
        pass
