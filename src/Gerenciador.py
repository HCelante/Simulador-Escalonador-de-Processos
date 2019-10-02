# GERENCIA DE PROCESSOS ######################
## CLASS MANAGER                    ##########
### METODOS CONTRUTORES             ##########
### METODOS DE GERENCIA             ##########
### METODOS DE FEEDBACK             ##########
##############################################


import bcp             # BLOCO DE CONTROLE DE PROCESSO
import Queue as Q      # FILA CIRCULAR
import schedulers.Dnmc # PRIORIDADE DINAMICA
import schedulers.JSF  # JOB SHORTEST FIRST
import schedulers.RR   # ROUND ROBIN


# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp       = 0                        # tempo da cpu
        self.QueueBloq       = Q.Queue(True)            # fila de bloqueados
        self.List_QRdy       = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri       = Q.Queue(False)           # fila de processos nao criados

    # METODOS DE CONSTRUCAO ######################################################
    def construc_listQ(self, nfilas):
        listqrd = []
        for n in range(nfilas):
            listqrd.append(Q.Queue(False))
        return listqrd
    # METODOS DE GERENCIA ########################################################
    def consome(self):                      # consome os processos
        pass
    



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
