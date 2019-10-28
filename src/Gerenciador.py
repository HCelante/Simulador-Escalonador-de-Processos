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
from src.schedulers.SJF import SJF as sjf            # JOB SHORTEST FIRST
from src.schedulers.RR  import RR as rr            # ROUND ROBIN


# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp      = 0                        # tempo da cpu
        self.QueueBloq      = Q(True)                  # fila de bloqueados
        self.List_QRdy      = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri      = Q(False)                 # fila de processos nao criados
        self.indexQRdy      = 0
        self.init_tms       = []                       # lista de tempos de entrada de processos
        self.QueueFinished  = []                        # fila de processos terminados
        self.numberOfProc   = 0                         # numero total de processos
        
    # método de reset do gerenciador
    def reset_Manager(self, nfilas):
        self.Timestamp      = 0
        self.QueueBloq      = Q(True)
        self.List_QRdy      = self.construc_listQ(nfilas)
        self.QueueNCri      = Q(False)
        self.indexQRdy      = 0
        self.init_tms       = []
        self.QueueFinished  = []
        self.numberOfProc   = 0 
        
    # METODOS DE CONSTRUCAO ######################################################
    def construc_listQ(self, nfilas):
        listqrd = []
        for n in range(int(nfilas)):
            #print("\nfila: ", n, "criada")
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

        print(self.init_tms)
        for init in self.init_tms:
            for bcp in listadeBCPS:
                if(init == bcp.procArrivalTime):
                    print ("teste ", bcp.procID, bcp.procArrivalTime)
                    listaBCPOrd.append(bcp)
        #print(listaBCPOrd[0].procArrivalTime)
        # coloca os processos na fila criada
        print (listaBCPOrd[0].procID)
        for processo in listaBCPOrd:                                   
            QueueNC.queueOne(processo)
        #print(QueueNC)
        print("\n Numero de processos enfileirados na de Nao Criados: ",len(listadeBCPS))

        self.numberOfProc = len(listadeBCPS)
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
            # tms = 2
            # self.Timestamp = 0
            # qt = confs[0][0]
            # RR = rr(qt)
            # while True: 
            #     # fluxo de execucao do RR

            #     ## ENTRADA DE BLOQUEADOS
            #     if(len(self.QueueBloq.sentinel) > 0):
            #         for bcpindex in range(len(self.QueueBloq.sentinel)):
            #             self.QueueBloq.sentinel[bcpindex].procResponseTime -= 1
            #             if(0 == self.QueueBloq.sentinel[bcpindex].procResponseTime):
            #                 self.List_QRdy[0].queueOne(self.QueueBloq.sentinel[bcpindex])
                        
                           
            #     ## ENTRADA DE PROCESSOS
            #     if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
            #         #confere se tem processos para serem criados
            #         if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
            #             self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri[self.QueueNCri.get_AIndex()]) # processo inserido na fila de prontos

            #     ## EXECUCAO DE PROCESSOS
            #     if(len(self.List_QRdy[self.indexQRdy]) > 0):
            #         #se tiver o que consumir
            #         #  
            #         processo = self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()]

            #         # atualiza o tempo de espera nas listas de prontos
            #         self.List_QRdy[self.indexQRdy].update_WaitingTimeRR()
            #         #consome
            #         RR.update_BCPQt( self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()]) # consome o quantum
            #         self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons += 1 #adiciona no quantum consumido
            #         terminado = self.List_QRdy[self.indexQRdy].check_Status(self.List_QRdy[self.indexQRdy].get_AIndex()) # checa o status do processo, se terminado é retirado da queue 
                    
            #         # variavel pra ficar mais legivel
            #         consumo_atual = self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons + 1
                    
            #         if terminado != None: # se o processo terminou
            #             finished.append(terminado) # vai pra lista de terminados

            #         if (processo.procTurnaroundTime in processo.procIOTime): # se tempo de execucao do processo consta em sua lista de IO
            #             processo.procState = -1
            #             self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procState = -1
                    
            #         # checagem de status apos execucao
            #         if ((terminado == None) and (processo.procState == -1)): # se status bloqueado
            #             processo.procQtCons = 0
            #             processo.procResponseTime = tms         # recebe o contador de tempo de espera
            #             self.QueueBloq.queueOne(processo)       # vai para a fila de bloqueados
            #             self.List_QRdy[self.indexQRdy].sentinel.pop(self.List_QRdy[self.indexQRdy].get_AIndex()) # e eh retirado da fila de prontos


            #         elif consumo_atual == qt : # se ja consumiu todo o quantum que pode nessa rodada
            #             self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()].procQtCons = 0 # seu quantum consumido zera 
            #             self.List_QRdy[self.indexQRdy].next_index() # e é vez do proximo

                    


            #     ## SE OCIOSO
            #     else: # se nao tiver mais o que consumir
            #         print("Ocioso...") # quebra o loop  de execucao
            #         if((len(self.QueueBloq.sentinel) == 0) and (len(finished) == qtdProcess)):
            #             print("Resultados")
            #             return 1

            #     self.Timestamp += 1
            pass                
                
   
                

        

        # Se Prioridade Dinamica        
        if optscheduler == 'DNMC' or 'dnmc':
            # while True:
            #     # fluxo de execucao do DNMC 
            #     if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
            #         #confere se tem processos para serem criados
            #         if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
            #             # definir qual criterio para selacao de fila
            #             #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos
                        
            #             pass
            #         pass

            pass
        
        if optscheduler == 'SJF' or 'sjf':
            
            self.Timestamp = 0
            SJF = sjf(confs[2])
            i = 0
            j = 0

            #print(self.QueueNCri.sentinel[2].procArrivalTime)
            while True:
                # fluxo de execucao do SJF
                print("filancri ",  self.QueueNCri.sentinel[i].procID)
                if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                    if(self.Timestamp >= self.QueueNCri.sentinel[i].procArrivalTime): # se sim, enfilera o novo processo criado
                        # definir qual criterio para selacao de fila
                        self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri.sentinel[i]) # processo inserido na fila de prontos
                        print("TimeStamp: ", self.Timestamp)
                        #print(self.List_QRdy[0].sentinel[i].procArrivalTime)
                        i+=1
                        self.QueueNCri.indexQueue = i

                if((len(self.QueueFinished) != self.numberOfProc) ):
                    #print (len(self.List_QRdy[self.indexQRdy].sentinel) > 0 and len(self.QueueFinished) != self.numberOfProc)
                    if (len(self.List_QRdy[self.indexQRdy].sentinel) > 0):
                       
                        index = SJF.selectProc(self.List_QRdy[0])
                        executingProc = self.List_QRdy[0].sentinel[index]
                        self.List_QRdy[0].sentinel.pop(index)

                        if (executingProc):
                            print (executingProc)
                            print(executingProc.procID, executingProc.procIOTime, executingProc.procState, executingProc.procBurstTime)

                            if ((executingProc.procState == 0) or (executingProc.procState == 1)):
                                executingProc = SJF.executeSJF(executingProc, self.Timestamp)
                            elif (executingProc.procState == -1):
                                self.QueueBloq.sentinel.append(executingProc)
                                executingProc = []
                                # print (executingProc)
                                #print("aqui1")
                                # print (self.QueueBloq.sentinel)
                                # print (self.QueueBloq.sentinel[0].timeBlockRemain)
                            elif(executingProc.procState == 2):
                                self.QueueFinished.append(executingProc)
                                executingProc = []
                    
                    if (len(self.QueueBloq.sentinel) > 0):    
                        for i in range (len(self.QueueBloq.sentinel)):
                            if ((self.QueueBloq.sentinel[i] != None ) and (self.QueueBloq.sentinel[i].timeBlockRemain == 0)):
                                self.QueueBloq.sentinel[i].procState = 0
                                self.List_QRdy[0].sentinel.append(self.QueueBloq.sentinel[i])
                                print("Tirei o processo " + str(self.QueueBloq.sentinel[i].procID) + " da fila de bloqueados, pelo tempo de bloqueio estar com " + str(self.QueueBloq.sentinel[i].timeBlockRemain) + " unidades de tempo")
                                print(self.List_QRdy[0].sentinel[0].procIOTime)
                                self.QueueBloq.sentinel.pop(i)
                                # print (self.QueueBloq.sentinel)
                            else:
                                print ("Falta " + str(self.QueueBloq.sentinel[i].timeBlockRemain) + " unidades para desbloquear o processo " + str(self.QueueBloq.sentinel[i].procID))
                                self.QueueBloq.sentinel[i].timeBlockRemain -= 1      

                else:
                    break
                self.Timestamp += 1

            # print(len(self.List_QRdy[0].sentinel))



    
 


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
