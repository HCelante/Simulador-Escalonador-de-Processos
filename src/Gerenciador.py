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
from src.models.plotting import Gantt

# GERENCIADOR DE PROCESSOS #######################################################
class Manager:                                          # Gerenciador de processos
    def __init__(self, nfilas):                         # metodo inicializador
        self.Timestamp      = 0                         # tempo da cpu
        self.QueueBloq      = Q(True)                   # fila de bloqueados
        self.List_QRdy      = self.construc_listQ(nfilas) # lista de fila de prontos
        self.QueueNCri      = Q(False)                  # fila de processos nao criados
        self.indexQRdy      = 0                         # 0 = Fila A, 1 = Fila B
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

    def isTheEnd(self, procDaVez): # True se não há mais processos para serem escalonados, False caso contrário
        cond = True
        if(procDaVez != None):
            cond = False
        for i in range(len(self.List_QRdy)):
            cond = cond and self.List_QRdy[i].isEmpty()
        cond = cond and self.QueueBloq.isEmpty()
        cond = cond and self.QueueNCri.isEmpty()
        if(cond): 
            print("Todas as filas estão vazias")
        return cond

    def isIO(self, proc):
        print("proc: ", proc.procID)
        IO = False
        for i in range(len(proc.procIOTime)):           # percorre todo o vetor de IO
            if(proc.procIOTime[i] == self.Timestamp):                # caso tenha que realizar IO
                print("processo ", proc.procID, "saiu para realizar IO no tempo ", self.Timestamp)
                IO = True
        return IO

    def bloqUpdate(self, quantum):
        if(not self.QueueBloq.isEmpty()):
            for i in range (len(self.QueueBloq.sentinel)):                  # percorre toda a lista de bloqueados
                print("Processo: ", self.QueueBloq.sentinel[i].procID, "Bloqueado, timeBlockRemain:", self.QueueBloq.sentinel[i].timeBlockRemain)
                self.QueueBloq.sentinel[i].timeBlockRemain -= 1             # decrementa 1 no tempo de bloqueio restante do processo
                if(self.QueueBloq.sentinel[i].timeBlockRemain <= 0):        # caso algum processo tenha seu tempo restante de bloqueio zerado:
                    print("entrou")
                    self.QueueBloq.sentinel[i].procState = 0                # atualiza o estado do processo
                    if(self.QueueBloq.sentinel[i].procBurstTime != 0):      # só insere novamente nas filas se o processo ainda tiver que ser processado
                        print("entrou2")                        
                        self.QueueBloq.sentinel[i].procQtCons = 0               # zera a quantidade do Quantum consumido
                        if(self.QueueBloq.sentinel[i].procQtCons < quantum):
                            self.List_QRdy[0].queueOne(self.QueueBloq.pop(i))  # processo vai para a lista A
                            i -= 1 
                        elif(self.QueueBloq.sentinel[i].procQtCons == quantum):
                            self.List_QRdy[1].queueOne(self.QueueBloq.pop(i))  # processo vai para a lista B
                            i -= 1 
                            
                    else:
                        print("entrou 3")
                        self.QueueBloq.sentinel[i].procState = 2            # processo finalizado
                        self.QueueBloq.sentinel[i].calculate_Turnaround()
                        self.QueueFinished.append(self.QueueBloq.pop(i))  # insere na lista de finalizados 

                    # self.QueueBloq.pop(i)                                   # Retira o processo da lista de bloqueados
                    # self.QueueBloq.sentinel = self.QueueBloq.sentinel[: i-1] + self.QueueBloq.sentinel[i+1 :]
                    # print("Processo ", self.QueueBloq.pop(i).procID, "saiu da fila de bloqueados")


    def exec_loop(self, optscheduler, confs): # fluxo de execucao para os escalonadores
       #optscheduler = tipo do schedule  confs = configuraçoes do escalonadores
        finished = []
        
        # Se Round Robin escolhido
        #######################
        # ROUND ROBIN  ########
        #######################
        if optscheduler == ('RR' or 'rr'):
            tms = 2
            self.Timestamp = 0
            qt = confs[0][0]
            RR = rr(qt)
            qtdProcess = self.numberOfProc
            executionlog = []
            while True: 
                # fluxo de execucao do RR

                #BQ1 Entrada de processos bloqueados
                #print("\n\nainda nao criados",len(self.QueueNCri.sentinel)  )
                print("\nTimeStamp: ", self.Timestamp)
                if(len(self.QueueBloq.sentinel) > 0): # se a fila de bloqueados nao for vazia
                    for bcpindex in range(len(self.QueueBloq.sentinel)): # checa quais bcps devem ir para a fila de prontos
                        if(0 == self.QueueBloq.sentinel[bcpindex].timeBlockRemain):
                            self.QueueBloq.sentinel[bcpindex].procState = 0
                            self.List_QRdy[0].queueOne(self.QueueBloq.sentinel[bcpindex])
                            
                            print("Processo: ",self.QueueBloq.sentinel[bcpindex].procID, "saiu de bloqueado para pronto")
                            self.QueueBloq.sentinel.pop(bcpindex)
                self.criaListaProntos()
               
                #EXC 1 Consumo de processos na fila de prontos
                if(len(self.List_QRdy[self.indexQRdy].sentinel) > 0): # se tem processos na fila de prontos
                    # eh criada uma variavel para ser usada nas comparacoes, para melhor legibilidade do codigo
                    processo = self.List_QRdy[self.indexQRdy].sentinel[self.List_QRdy[self.indexQRdy].get_AIndex()] # variavel com bcp do processo em execucao
                    print("ID: ", processo.procID, "\tFIO: ", processo.procIOTime, "\tSTATE: ",processo.procState, "\tBT: ",processo.procBurstTime, "\tUSED: ", processo.procCPUuse)

                    # atualiza o tempo de espera de todos nas listas de prontos
                    # execeto do processo em execucao
                    self.List_QRdy[self.indexQRdy].update_WaitingTime()
                    RR.update_BCPQt(processo) # consome o quantum
                    terminado = self.List_QRdy[self.indexQRdy].check_Status(self.List_QRdy[self.indexQRdy].indexQueue) # checa o status do processo, se terminado é retirado da queue 
                    #print("processo consumido", processo.procID, "\nqt ja consumido",processo.procQtCons,"\n proc state", processo.procState)
                    executionlog.append([processo.procID, self.Timestamp])
                    
                    if terminado != None: # se o processo terminou
                        finished.append(terminado) # vai pra lista de terminados
                        print("\nProcesso terminado: ",terminado[0].procID)
                        #self.List_QRdy[self.indexQRdy].sentinel.pop(self.List_QRdy[self.indexQRdy].get_AIndex())


                    else:
                        if (int(processo.procCPUuse) in processo.procIOTime): # se tempo de execucao do processo consta em sua lista de IO
                            processo.procState = -1
                            processo.timeBlockRemain = tms         # recebe o contador de tempo de espera
                            print("Processo "+ str(processo.procID) +" bloqueado para IO, durante " + str(tms) + " unidades de tempo\n")
                            if (processo.procQtCons == qt):
                                processo.procQtCons = 0 
                            self.QueueBloq.queueOne(processo)       # vai para a fila de bloqueados
                            self.List_QRdy[self.indexQRdy].sentinel.pop(self.List_QRdy[self.indexQRdy].get_AIndex()) # e eh retirado da fila de prontos


                        elif (processo.procQtCons == qt ):
                            processo.procQtCons = 0 # seu quantum consumido zera
                            processo.procState = 0
                            print("\nPassa a vez para o proximo.")
                    
                            self.List_QRdy[self.indexQRdy].next_index()
                
                else: # se nao tiver mais o que consumir
                    print("Ocioso...") # quebra o loop  de execucao
                    #print("terminados",len(finished),"total", qtdProcess)
                    if(len(finished) == qtdProcess):
                        print(executionlog)
                        gantt = Gantt(executionlog)
                        gantt.construc_graph(executionlog)
                        print("Resultados")
                        return 1
   
                #BQ2 Atualizacao do tempo de espera dos processos na fila de bloq
                if(len(self.QueueBloq.sentinel) > 0): # se a fila de bloqueados nao for vazia
                    for bcpindex in range(len(self.QueueBloq.sentinel)): # checa quais bcps devem ir para a fila de prontos
                        print ("Falta " + str(self.QueueBloq.sentinel[bcpindex].timeBlockRemain) + " unidades para desbloquear o processo " + str(self.QueueBloq.sentinel[bcpindex].procID) + "\n")
                        self.QueueBloq.sentinel[bcpindex].timeBlockRemain -= 1

 

                self.Timestamp += 1
                # print(">>> Fim Time Stamp: ",self.Timestamp,"\n\n")
                if(self.Timestamp >= 40):
                    break
                #print(len(finished), qtdProcess, len(self.List_QRdy[0].sentinel), "bloeq: ", len(self.QueueBloq.sentinel))
                if(len(finished) == qtdProcess):
                    print(executionlog)
                    gantt = Gantt(executionlog)
                    gantt.construc_graph(executionlog)
                    print("Resultados")
                    return 1







            
        # Se Prioridade Dinamica 
        if optscheduler == ('DNMC' or 'dnmc'):
            DNMC = dnmc(confs[1])
            quantum = DNMC.getQuantum()
            procDaVez = None
            bloqOut = 0
            queue = 'A'
            dnmcplot = []
            # print("Quantum: ", DNMC.getQuantum())
            
            while(not self.isTheEnd(procDaVez)):    # enquanto houver algum processo para ser escalonado
                # print("-------------------------------------------------------------------------")
            # while(self.Timestamp < 35):
                print("TimeStamp: ", self.Timestamp)

                A_size = len(self.List_QRdy[0].sentinel)
                self.criaListaProntos()                             # caso algum processo novo tenha chegado, insere ele na fila de prontos 
                if(A_size < len(self.List_QRdy[0].sentinel)):       # caso algum processo tenha sido inserido a fila de prontos 
                    A_size = len(self.List_QRdy[0].sentinel)
                    self.ordByPriority()                            # reordena a Fila A pela prioridade dos processos 

                bloq_size = len(self.QueueBloq.sentinel)
                self.bloqUpdate(quantum)                            # atualiza as informações dos processos da lista de bloqueados
                bloqOut = 0                                         # variável que informa quando um processo saiu da fila de bloqueados
                if(bloq_size > len(self.QueueBloq.sentinel)):       # caso algum processo tenha saído da fila de bloqueados
                    bloqOut = 1
                
                if(procDaVez == None):                              # caso nenhum processo esteja executando,
                    # print("procDaVez None")
                    quantum = DNMC.getQuantum()
                    if(A_size != 0):                                # caso haja processo em A, ele é o escolhido para o procesamento
                        procDaVez = self.List_QRdy[0].pop(0)
                        self.calc_RT(procDaVez)
                        # print("A_size: ",A_size)
                        # print("procDaVez:", procDaVez.procID)
                        queue = 'A'

                    elif(len(self.List_QRdy[1].sentinel) > 0):      # se não, caso haja processos na fila B, ele é o escolhido
                        procDaVez = self.List_QRdy[1].pop(0)
                        if(procDaVez.procState == 0):
                            self.calc_RT(procDaVez)
                        queue = 'B' 
                    else:
                        print("Todos os processos estão bloqueados ou ainda não chegaram para o Processamento: ")
                 
                if(procDaVez):
                    if(bloqOut and (queue == 'A')):                           # caso um processo tenha saído agora da fila de bloqueados
                        if(not self.List_QRdy[0].isEmpty()):                # caso o processo que saiu de bloqueados tenha ido pra fila A
                            self.ordByPriority()                            # reordena a Fila A pela prioridade dos processos 
                            # procDaVez = self.List_QRdy[0].pop(0)
                            if(procDaVez.procID != self.List_QRdy[0].get_actual().procID):# caso o processo que chegou da fila de bloqueados seja de maior prioridade
                                aux = procDaVez
                                procDaVez = self.List_QRdy[0].pop(0)
                                aux.procQtCons = 0
                                procDaVez.procState = 0             
                                self.calc_RT(procDaVez)
                                self.List_QRdy[0].queueOne(aux)

                    if(quantum > 0 and procDaVez != None):                      # caso ja tenha um processo em execução 
                        dnmcplot.append([procDaVez.procID,self.Timestamp])
                        print("ID: ", procDaVez.procID, "\tFIO: ", procDaVez.procIOTime, "\tSTATE: ",procDaVez.procState, "\tBT: ",procDaVez.procBurstTime, "\tUSED: ", procDaVez.procCPUuse)

                        if(self.isIO(procDaVez)):                               # Caso haja IO
                            procDaVez.procState = -1                             # Atualiza status -> Bloqueado      
                            procDaVez.timeBlockRemain += DNMC.getIOtime()
                            DNMC.changePriority(procDaVez)                      # atualiza a prioridade do processo
                            self.QueueBloq.queueOne(procDaVez)
                            # print("processo ", procDaVez.procID, "saiu para IO no TimeStamp:", self.Timestamp)
                            procDaVez.procCompletionTime = self.Timestamp
                            procDaVez = None
                        
                        else:                                   # Se não houver IO, executa
                            procDaVez.procState = 1             # estado -> Executando
                            procDaVez.procQtCons += 1           # quantum consumido += 1
                            procDaVez.procBurstTime -= 1        # diminui 1 no tempo que o processo precisa executar
                            DNMC.changePriority(procDaVez)      # Atualiza a prioridade
                            # print("proc: ", procDaVez.procID, " executando, faltam ", procDaVez.procBurstTime, "ciclos a serem executados" )                        
                            if(procDaVez.procBurstTime == 0):   # Caso o Processo termine -----------------------------
                                procDaVez.procState = 2         #   estado -> Finalizado
                                procDaVez.calculate_Turnaround()
                                self.QueueFinished.append(procDaVez)  #   procDaVez -> finalizados
                                procDaVez.procCompletionTime = self.Timestamp
                                procDaVez = None
                                quantum = 0

                        quantum -= 1
                
                if((quantum == 0) and (procDaVez != None) and (procDaVez.procBurstTime > 0)):             # caso o processo em execução ja tenha excedido o quantum
                    self.List_QRdy[1].queueOne(procDaVez)           # procDaVez -> B[]
                    procDaVez.procState = 0                         # estado -> Pronto
                    procDaVez.procCompletionTime = self.Timestamp
                    procDaVez = None

                # if(procDaVez != None):
                #     print("BurstTime: ", procDaVez.procBurstTime)
                # print("A: ") 
                # for i in range(len(self.List_QRdy[0].sentinel)):
                #     # A.append(self.List_QRdy[0].sentinel[i])
                #     print(self.List_QRdy[0].sentinel[i].procID)
                # print("--------")
                # print("B: ")
                # for i in range(len(self.List_QRdy[1].sentinel)):
                #     print(self.List_QRdy[1].sentinel[i].procID)

                # print("--------")
                # print("Bloq: ")
                # for i in range(len(self.QueueBloq.sentinel)):
                #     print(self.QueueBloq.sentinel[i].procID)

                # print("Timestamp: ", self.Timestamp)
                self.Timestamp += 1
                # print("-------------------------------------------------------------------------")

            # for proc in self.QueueFinished:
            #     print("processo: ", proc.procID ,"Response Time: ", proc.procResponseTime)

            for process in (self.QueueFinished):
                process.calculate_Waiting()
            gantt = Gantt(dnmcplot)
            gantt.construc_graph(dnmcplot)
            self.calc_TRM(self.QueueFinished)
            self.calc_TTE(self.QueueFinished)

        if optscheduler == ('SJF' or 'sjf'):
            self.Timestamp = 0
            SJF = sjf(confs[2])
            blockIndex = 0
            executingProc = None
            outplot = []
            # fluxo de execucao do SJF
            while True:    
                # Percorre a lista de não criados, preenchendo a lista de prontos
                self.criaListaProntos()
                
                #Verifica se há um processo na lista de prontos para a execuçao
                if (self.List_QRdy[0].sentinel):
                    index, bt = SJF.selectProc(self.List_QRdy[0])   # Faz a seleção do processo com menor burstime na fila de prontos, para ser executado, retornando o index dele e o bt

                    if (executingProc):
                        
                        if (executingProc.procState == 1):
                            if (executingProc.procBurstTime > bt):  # caso haja um processo em execução, o processo selecionado na fila só iniciará se ele possuir um bt menor
                                
                                executingProc.procState = 0
                                
                                self.List_QRdy[0].sentinel.append(executingProc)    # retorna o processo em execução para a lista de prontos
                                executingProc = self.List_QRdy[0].sentinel[index]   # atribui o novo processo
                                self.List_QRdy[0].sentinel.pop(index)               # remove da lista
                    
                    else:                                           # caso não haja um processo em execução, iniciar o mais apto
                        executingProc = self.List_QRdy[0].sentinel[index]
                        self.List_QRdy[0].sentinel.pop(index)

                # execução principal
                if((len(self.QueueFinished) != self.numberOfProc) ): # Se o numero de processos terminados for diferente do numero de processos
                    print("TimeStamp: ", self.Timestamp)

                    if (executingProc):
                            outplot.append([executingProc.procID,self.Timestamp])
                            print("ID: ", executingProc.procID, "\tFIO: ", executingProc.procIOTime, "\tSTATE: ",executingProc.procState, "\tBT: ",executingProc.procBurstTime, "\tUSED: ", executingProc.procCPUuse)

                            if ((executingProc.procState == 0) or (executingProc.procState == 1)):
                                self.calc_RT(executingProc)
                                executingProc = SJF.executeSJF(executingProc, self.Timestamp)       # executa um novo processo ou um que está executando
                            
                            if (executingProc.procState == -1):
                                self.QueueBloq.sentinel.append(executingProc)   # caso retorne da execução com o estado -1, o processo será inserido na fila de bloqueados
                                executingProc = None

                            elif(executingProc.procState == 2):
                                self.QueueFinished.append(executingProc)        # caso retorne da execução com o estado 2, o processo será inserido na fila de finalizados
                                executingProc = None

                    if (len(self.QueueBloq.sentinel) > 0):                      # caso haja alguém na fila de bloqueados
                        while blockIndex < (len(self.QueueBloq.sentinel)):

                            if (self.QueueBloq.sentinel[blockIndex].timeBlockRemain == 0):  # Remove da fila de bloqueados caso o tempo de bloqueio esteja zerado
                                self.QueueBloq.sentinel[blockIndex].procState = 0
                                self.List_QRdy[0].sentinel.append(self.QueueBloq.sentinel[blockIndex])  # E insire na lista de prontos 
                                print("\nTirei o processo " + str(self.QueueBloq.sentinel[blockIndex].procID) + " da fila de bloqueados, pelo tempo de bloqueio estar com " + str(self.QueueBloq.sentinel[blockIndex].timeBlockRemain) + " unidades de tempo")
                                self.QueueBloq.sentinel.pop(blockIndex)
                                blockIndex -= 1

                            else:   # decrementa o tempo restante do bloqueio
                                print ("Falta " + str(self.QueueBloq.sentinel[blockIndex].timeBlockRemain) + " unidades para desbloquear o processo " + str(self.QueueBloq.sentinel[blockIndex].procID))
                                self.QueueBloq.sentinel[blockIndex].timeBlockRemain -= 1   
                            
                            blockIndex += 1
                        blockIndex = 0

                else:
                    for process in (self.QueueFinished):
                        process.calculate_Waiting()
                    print(outplot)
                    gantt = Gantt(outplot)
                    gantt.construc_graph(outplot)
                    self.calc_TRM(self.QueueFinished)
                    self.calc_TTE(self.QueueFinished)
                    break
            
                self.Timestamp += 1


    def criaListaProntos(self):         # gera lista de pronto por ordem de chegada
        i = 0

        while i < len(self.QueueNCri.sentinel):
    
            if(self.Timestamp >= self.QueueNCri.sentinel[i].procArrivalTime):       # se o timestamp atual for do momento de chegada do processo
                self.List_QRdy[self.indexQRdy].queueOne(self.QueueNCri.sentinel[i]) # processo inserido na fila de prontos
                # print("Processo ", self.QueueNCri.sentinel[i].procID ," criado no tempo",self.Timestamp)
                self.QueueNCri.sentinel.pop(i)
                i -= 1
            
            i+=1

    def func(self, proc):
        return proc.procPriority

    def ordByPriority(self):
        ordList = []
        size = len(self.List_QRdy[0].sentinel)
        ordList = sorted(self.List_QRdy[0].sentinel, key = self.func, reverse = True)

        for i in range(size):    # esvazia a Lista A para receber os novos valores ordenados
            self.List_QRdy[0].sentinel.pop()
         
        for proc in ordList:     # insere os valores já ordenados na lista A
            self.List_QRdy[0].queueOne(proc)


    # METODOS DE FEEDBACK ########################################################
    def calc_RT(self, bcp):
        if (bcp.procCPUuse == 0):
            bcp.procResponseTime += self.Timestamp - bcp.procArrivalTime
        else:
            bcp.procResponseTime += self.Timestamp - bcp.procCompletionTime

    def calc_TME(self, tte):                   # calculo do tempo medio de espera
        tme = tte/self.numberOfProc
        print("Tempo médio de resposta: ", tme)
        return tme

    def calc_TTE(self, procs):                   # calculo tempo total de espera
        tte = 0
        for process in procs:
            tte += process.procWaitingTime
        print("Tempo total de resposta: ", tte)
        self.calc_TME(tte)
        return tte
    
    def calc_Thrgpt(self):                # calculo throughput do sistema
        pass

    def calc_TMTMF(self):                 # calculo tamanho maximo e medio das filas
        pass

    def calc_TRM(self, procs):                   # calculo tempo de resposta medio
        trt = 0
        print('\n')
        for process in procs:
            trt += process.procResponseTime
        for process in procs:
            process.tempoRespMedio = (process.procResponseTime/(trt/self.numberOfProc))
            print("Tempo de resposta médio: ", process.tempoRespMedio, " do processo ", process.procID)
        
