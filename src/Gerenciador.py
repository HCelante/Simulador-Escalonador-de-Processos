# GERENCIA DE PROCESSOS ######################
## CLASS MANAGER                    ##########
### METODOS CONTRUTORES             ##########
### METODOS DE GERENCIA             ##########
### METODOS DE FEEDBACK             ##########
##############################################

import sys
#sys.path.append('models')
#print(sys.path)

from src.models.bcp import BCP              # BLOCO DE CONTROLE DE PROCESSO
from src.models.Queue import Queue as Q     # FILA CIRCULAR
from src.schedulers.Dnmc import *           # PRIORIDADE DINAMICA
from src.schedulers.SJF import *            # JOB SHORTEST FIRST
from src.schedulers.RR  import *            # ROUND ROBIN


# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp       = 0                        # tempo da cpu
        self.QueueBloq       = Q(True)                  # fila de bloqueados
        self.List_QRdy       = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri       = Q(False)                 # fila de processos nao criados
        self.indexQRdy       = 0
        self.init_tms        = []                       # lista de tempos de entrada de processos

    # METODOS DE CONSTRUCAO ######################################################
    def construc_listQ(self, nfilas):
        listqrd = []
        for n in range(int(nfilas)):
            print("\nfila: ", n, "criada")
            listqrd.append(Q(False))
        return listqrd

    def construc_QNC(self, listadeBCPS): 
    # constroi a lista de processos nao criados e ordenados por tempo de entrada
        QueueNC = Q(False)
        tmsIN = []
        listaBCPorD = []
        for bcp in listadeBCPS:
            tmsIN.append( bcp.procArrivalTime)

        # lista de tempos de entrada criada
        self.init_tms = sorted(set(tmsIN))
        #for tmm in self.init_tms:
        #    listaBCPorD.append([tmm]) 
        # ordenado os processos por tempo de entrada    

        #print(listaBCPorD)
        for bcp in listadeBCPS:
            for init in self.init_tms:
                if(init == bcp.procArrivalTime):
                    listaBCPorD.append(bcp)
        #print(listaBCPorD[0].procArrivalTime)
        # coloca os processos na fila criada
        for processo in listadeBCPS:   
            #print(type(processo))                                     
            QueueNC.queueOne(processo)
        #print(QueueNC)
        print("\n Numero de processos enfileirados na de Nao Criados: ",len(listadeBCPS))

        self.QueueNCri = QueueNC                                        # retorna para a fila de nao criados





    # METODOS DE GERENCIA ########################################################
    def updateQ_Priority(self, cond):                      # consome os processos
        if ("AB" == cond):                               # consome primeiro a e debois b
            if(self.List_QRdy[self.indexQRdy].isEmpty() == True):
                self.indexQRdy = self.indexQRdy + 1


    def exec_loop(self, cond, optscheduler): # fluxo de execucao para os escalonadores


        # Se Round Robin escolhido
        if optscheduler == 'RR' or 'rr':
            self.Timestamp = 0
            while True: 
                # fluxo de execucao do RR
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_atual.procArrivalTime): # se sim, enfilera o novo processo criado
                        self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos

                if(len(self.List_QRdy[self.indexQRdy]) > 0):
                    #se tiver o que consumir 
                    #consome
                    pass
                        
                pass
   
                

            pass

        # Se Prioridade Dinamica        
        if optscheduler == 'DNMC' or 'dnmc':
            while True:
                # fluxo de execucao do DNMC 
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_atual.procArrivalTime): # se sim, enfilera o novo processo criado
                        # definir qual criterio para selacao de fila
                        #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos
                        
                pass
   

            pass
        
        if optscheduler == 'SJF' or 'sjf':
            while True:
                # fluxo de execucao do SJF
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_atual.procArrivalTime): # se sim, enfilera o novo processo criado
                        # definir qual criterio para selacao de fila
                        #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos

                    pass

            pass



    



    # METODOS DE FEEDBACK ########################################################

    def calc_TME(self):                   # calculo do tempo medio de espera
        pass

    def calc_TTE(self):                   # calculo tempo total de espera
        pass
    
    def calc_Thrgpt(self):                # calculo throughput do sistema
        pass

    def calc_TMTMF(self):                 # calculo tamanho maximo e medio das filas
        pass

    def calc_TRM(self):                   # calculo tempo de resposta medio
        pass
