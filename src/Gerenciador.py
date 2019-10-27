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

    # método de reset do gerenciador
    def reset_Manager(self, nfilas):
        self.Timestamp       = 0
        self.QueueBloq       = Q(True)
        self.List_QRdy       = self.construc_listQ(nfilas)
        self.QueueNCri       = Q(False)
        self.indexQRdy       = 0
        self.init_tms        = []
        
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
        listaBCPOrd = []
        for bcp in listadeBCPS:
            tmsIN.append( bcp.procArrivalTime)

        # lista de tempos de entrada criada
        self.init_tms = sorted(set(tmsIN))
        #for tmm in self.init_tms:
        #    listaBCPOrd.append([tmm]) 
        # ordenado os processos por tempo de entrada    

        #print(listaBCPOrd)
        for bcp in listadeBCPS:
            for init in self.init_tms:
                if(init == bcp.procArrivalTime):
                    listaBCPOrd.append(bcp)
        #print(listaBCPOrd[0].procArrivalTime)
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


    def exec_loop(self, optscheduler, confs): # fluxo de execucao para os escalonadores
    #optscheduler = tipo do schedule  confs = configuraçoes do escalonadores
        finished = []

        # Se Round Robin escolhido
        ########################
        ## ROUND ROBIN  ########
        ########################
        if optscheduler == 'RR' or 'rr':
            self.Timestamp = 0
            qt = confs[0][0]
            RR = RR(qt)
            while True: 
                # fluxo de execucao do RR


                ## ENTRADA DE PROCESSOS
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
                        self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri[self.QueueNCri.get_AIndex()]) # processo inserido na fila de prontos

                ## EXECUCAO DE PROCESSOS
                if(len(self.List_QRdy[self.indexQRdy]) > 0):
                    #se tiver o que consumir 

                    # atualiza o tempo de espera nas listas de prontos
                    self.List_QRdy[self.indexQRdy].update_WaitingTimeRR()
                    #consome
                    RR.update_BCPQt( self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()]) # consome o quantum
                    self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons += 1 #adiciona no quantum consumido
                    terminado = self.List_QRdy[self.indexQRdy].check_Status(self.List_QRdy[self.indexQRdy].get_AIndex()) # checa o status do processo, se terminado é retirado da queue 
                    
                    # variavel pra ficar mais legivel
                    consumo_atual = self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons + 1
                    
                    if terminado != None: # se o processo terminou
                        finished.append(terminado) # vai pra lista de terminados
                    elif consumo_atual == qt : # se ja consumiu todo o quantum que pode nessa rodada
                        self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons = 0 # seu quantum consumido zera 
                        self.List_QRdy[self.indexQRdy].next_index() # e é vez do proximo
                
                ## CONDICAO DE PARADA
                else: # se nao tiver mais o que consumir
                    break # quebra o loop  de execucao
                        
                
   
                

            pass

        # Se Prioridade Dinamica        
        if optscheduler == 'DNMC' or 'dnmc':
            while True:
                # fluxo de execucao do DNMC 
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
                        # definir qual criterio para selacao de fila
                        #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos
                        
                        pass
                    pass

            pass
        
        if optscheduler == 'SJF' or 'sjf':
            while True:
                # fluxo de execucao do SJF
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
                        # definir qual criterio para selacao de fila
                        #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos

                        pass
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
