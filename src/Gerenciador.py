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
from src.schedulers.Dnmc import DNMC as dnmc           # PRIORIDADE DINAMICA
from src.schedulers.SJF import SJF as sjf            # JOB SHORTEST FIRST
from src.schedulers.RR  import RR as rr            # ROUND ROBIN


# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp      = 0                         # tempo da cpu
        self.QueueBloq      = Q(True)                   # fila de bloqueados
        self.List_QRdy      = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri      = Q(False)                  # fila de processos nao criados
        self.indexQRdy      = 0
        self.init_tms       = []                        # lista de tempos de entrada de processos
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

        for init in self.init_tms:
            for bcp in listadeBCPS:
                if(init == bcp.procArrivalTime):
                    listaBCPOrd.append(bcp)
        # coloca os processos na fila criada

        for processo in listaBCPOrd:                                 
            QueueNC.queueOne(processo)
        #print(QueueNC)
        print("\nNumero de processos enfileirados na de Nao Criados: ",len(listadeBCPS))

        self.numberOfProc = len(listadeBCPS)
        self.QueueNCri = QueueNC                                        # retorna para a fila de nao criados





    # METODOS DE GERENCIA ########################################################
    def updateQ_Priority(self, cond):                       # consome os processos
        if ("AB" == cond):                                  # consome primeiro a e debois b
            if(self.List_QRdy[self.indexQRdy].isEmpty() == True):
                self.indexQRdy = self.indexQRdy + 1

    def isTheEnd(self): # True se não há mais processos para serem escalonados, False caso contrário
        cond = True
        for i in range(len(self.List_QRdy)):
            cond = cond and self.List_QRdy[i].isEmpty()
        cond = cond and self.QueueBloq.isEmpty()
        cond = cond and self.QueueNCri.isEmpty()

    def exec_loop(self, optscheduler, confs): # fluxo de execucao para os escalonadores
    #optscheduler = tipo do schedule  confs = configuraçoes do escalonadores
        finished = []
        
        # Se Round Robin escolhido
        #######################
        # ROUND ROBIN  ########
        #######################
        if optscheduler == 'RR' or 'rr':
            tms = 2
            self.Timestamp = 0
            qt = confs[0][0]
            RR = rr(qt)
            qtdProcess = self.numberOfProc
            while True: 
                # fluxo de execucao do RR

                #BQ1 Entrada de processos bloqueados
                print("\n\nainda nao criados",len(self.QueueNCri.sentinel)  )

                if(len(self.QueueBloq.sentinel) > 0): # se a fila de bloqueados nao for vazia
                    for bcpindex in range(len(self.QueueBloq.sentinel)): # checa quais bcps devem ir para a fila de prontos
                        if(0 == self.QueueBloq.sentinel[bcpindex].procResponseTime):
                            self.List_QRdy[0].queueOne(self.QueueBloq.sentinel[bcpindex])
                            print("\nprocesso ",self.QueueBloq.sentinel[bcpindex].procID, "saiu de bloqueado para pronto")
            
                #NC 1 Entrada de processos nao criados
                #if( len(self.QueueNCri.sentinel) > 0): # se a lista de nao criados nao terminou de ser percorrida
                    #confere se tem processos para serem criados
                #    if(self.Timestamp >= self.QueueNCri.sentinel[self.QueueNCri.indexQueue].procArrivalTime): # se sim, enfilera o novo processo criado
                #        self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri.sentinel[self.QueueNCri.indexQueue])
                #        print("\n",self.QueueNCri.sentinel[self.QueueNCri.indexQueue].procID, "criado")
                #        self.QueueNCri.sentinel.pop(self.QueueNCri.indexQueue) # apos criar o processo tira ele da fila de nao criados
                        # assim a cabeça da fila de nao criados ja fica em 0 com o segundo processo da fila

                self.criaListaProntos()
               
                #EXC 1 Consumo de processos na fila de prontos
                if(len(self.List_QRdy[self.indexQRdy].sentinel) > 0): # se tem processos na fila de prontos
                    # eh criada uma variavel para ser usada nas comparacoes, para melhor legibilidade do codigo
                    processo = self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()] # variavel com bcp do processo em execucao

                    # atualiza o tempo de espera de todos nas listas de prontos
                    # execeto do processo em execucao
                    self.List_QRdy[self.indexQRdy].update_WaitingTime()
                    RR.update_BCPQt(processo) # consome o quantum
                    terminado = self.List_QRdy[self.indexQRdy].check_Status(self.List_QRdy[self.indexQRdy].get_AIndex()) # checa o status do processo, se terminado é retirado da queue 
                    print("processo consumido", processo.procID, "\nqt ja consumido",processo.procQtCons,"\n proc state", processo.procState)
            
                    
                    if terminado != None: # se o processo terminou
                        finished.append(terminado) # vai pra lista de terminados
                        print("\n\nprocesso terminado ",terminado[0].procID)
                        #self.List_QRdy[self.indexQRdy].sentinel.pop(self.List_QRdy[self.indexQRdy].get_AIndex())


                    else:
                        if (processo.procCPUuse in processo.procIOTime): # se tempo de execucao do processo consta em sua lista de IO
                            processo.procState = -1
                            processo.procResponseTime = tms         # recebe o contador de tempo de espera
                            print("processo", processo.procID , " bloqueado")
                            self.QueueBloq.queueOne(processo)       # vai para a fila de bloqueados
                            self.List_QRdy[self.indexQRdy].sentinel.pop(self.List_QRdy[self.indexQRdy].get_AIndex()) # e eh retirado da fila de prontos


                        elif (processo.procQtCons == qt ):
                            processo.procQtCons = 0 # seu quantum consumido zera

                            print("passa a vez")
                    self.List_QRdy[self.indexQRdy].next_index()
                
                else: # se nao tiver mais o que consumir
                    print("Ocioso...") # quebra o loop  de execucao
                    if(len(finished) == qtdProcess):
                        print("Resultados")
                        return 1
   
                #BQ2 Atualizacao do tempo de espera dos processos na fila de bloq
                if(len(self.QueueBloq.sentinel) > 0): # se a fila de bloqueados nao for vazia
                    for bcpindex in range(len(self.QueueBloq.sentinel)): # checa quais bcps devem ir para a fila de prontos
                        self.QueueBloq.sentinel[bcpindex].procResponseTime -= 1

 
                
                self.Timestamp += 1
                print("fim ciclo: ",self.Timestamp)


        # Se Prioridade Dinamica 
        #if optscheduler == 'DNMC' or 'dnmc':
        #    DNMC = dnmc(confs[1])
            # print("Quantum: ", DNMC.getQuantum())
            
         #   while(not self.isTheEnd()): # enquanto houver algum processo para ser escalonado
         #       self.criaListaProntos() # caso algum processo tenha chegado para execução, insere ele na fila de prontos 
                

            #     # fluxo de execucao do DNMC 
            #     if(self.QueueNCri.indexQueue < len(self.QueueNCri.sentinel)): # se a lista de nao criados nao terminou de ser percorrida
            #         #confere se tem processos para serem criados
            #         if(self.Timestamp >= self.QueueNCri.get_actual.procArrivalTime): # se sim, enfilera o novo processo criado
            #             # definir qual criterio para selacao de fila
            #             #self.List_QRdy.queueOne(self.QueueNCri.get_proximo()) # processo inserido na fila de prontos
                        
            #             pass
            #        pass

            #pass

        
        if optscheduler == 'SJF' or 'sjf':
            pass
            self.Timestamp = 0
            SJF = sjf(confs[2])
            i = 0
            j = 0
            executingProc = None
            #print(self.QueueNCri.sentinel[2].procArrivalTime)
            while self.Timestamp < 7:
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
                    if (self.List_QRdy[0].sentinel): 
                        index, bt = SJF.selectProc(self.List_QRdy[0]) # retorna o index processo com o menor bt da lista de prontos

                    if (((len(self.List_QRdy[self.indexQRdy].sentinel) > 0) and (not executingProc)) or (executingProc.procBurstTime > bt) ): 
                    #compara se há algo na lista de prontos e não há processo executando, ou se o processo atual tiver um bt restante maior que o selecionado da lista de prontos
                        
                        if((executingProc) and (executingProc.procBurstTime > bt)):
                            self.List_QRdy[0].sentinel.append(executingProc)
                        # print ("entreiaqui")
                        if (self.List_QRdy[0].sentinel):
                            index, bt = SJF.selectProc(self.List_QRdy[0])
                        executingProc = self.List_QRdy[0].sentinel[index]
                        self.List_QRdy[0].sentinel.pop(index)

                    if (executingProc):
                            # print (executingProc)
                            print("ID: ", executingProc.procID, "\tFIO: ", executingProc.procIOTime, "\tSTATE: ",executingProc.procState, "\tBT: ",executingProc.procBurstTime)

                            if ((executingProc.procState == 0) or (executingProc.procState == 1)):
                                executingProc = SJF.executeSJF(executingProc, self.Timestamp)
                            
                            if (executingProc.procState == -1):
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
                            if (self.QueueBloq.sentinel != None ):
                                if (self.QueueBloq.sentinel[i].timeBlockRemain == 0):
                                    self.QueueBloq.sentinel[i].procState = 0
                                    self.List_QRdy[0].sentinel.append(self.QueueBloq.sentinel[i])
                                    print("\nTirei o processo " + str(self.QueueBloq.sentinel[i].procID) + " da fila de bloqueados, pelo tempo de bloqueio estar com " + str(self.QueueBloq.sentinel[i].timeBlockRemain) + " unidades de tempo")
                                    # print(self.List_QRdy[0].sentinel[0].procIOTime)
                                    self.QueueBloq.sentinel.pop(i)
                                    # print (self.QueueBloq.sentinel)
                                else:
                                    print ("Falta " + str(self.QueueBloq.sentinel[i].timeBlockRemain) + " unidades para desbloquear o processo " + str(self.QueueBloq.sentinel[i].procID))
                                    self.QueueBloq.sentinel[i].timeBlockRemain -= 1      

                else:
                    break
            
                self.Timestamp += 1
                

            # print(len(self.List_QRdy[0].sentinel))



    
 
    def criaListaProntos(self):         # gera lista de pronto por ordem de chegada
        i = 0

        while i < len(self.QueueNCri.sentinel):
            # print(i)
            if(self.Timestamp >= self.QueueNCri.sentinel[i].procArrivalTime): # se o timestamp atual for do momento de chegada do processo
                print("\nProcesso criado: ",self.QueueNCri.sentinel[i].procID)
                self.List_QRdy[0].queueOne(self.QueueNCri.sentinel[i]) # processo inserido na fila de prontos
                print("TimeStamp: ", self.Timestamp)
                self.QueueNCri.sentinel.pop(i)
                i -= 1
            
            i+=1

        # print (len(self.List_QRdy[0].sentinel))
        # for processo in self.List_QRdy[0].sentinel:
        #     print(processo.procID)

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
