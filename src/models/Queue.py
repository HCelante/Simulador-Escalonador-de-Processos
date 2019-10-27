# FILA CIRCULAR ######################
## CLASS QUEUE                ########
### METODOS DE ENFILEIRAMENTO ########
### METODOS DE RETORNO        ######## 
######################################

from src.models.bcp import BCP as bcp 

 
class Queue: # fila circular
    def __init__(self, bloqd):
        self.indexQueue = 0 # indice da fila de processos
        self.sentinel = [] # ponteiro/lista para armazenar e percorrer os valores da fila
        
        if bloqd == True : # se for uma fila de bloqueados
            self.totalTime = 0 # tempo total de espera para os processos nessa fila
        
    def check_Status_All(self): # cehca o status dos processos e da pop nos terminados e retorna uma lista de terminados
        terminated = []
        for bcpindex in range(len(self.sentinel)):
            if(self.sentinel[bcpindex].procState == 2): # se processo terminado~
                terminated.append(self.sentinel[bcpindex])
                self.sentinel.pop(bcpindex)

        return terminated # retorna a lista de processos terminados para que possam ser enfileirados na de terminados

    def check_Status(self, index):
        terminated = []
        if(self.sentinel[index].procState == 2): # se processo terminado~
            terminated.append(self.sentinel[index])
            self.sentinel.pop(index)
            return terminated
        else:
            return None


    def queueOne(self, procbcp): # recebe o bloco de controle de processo referente ao processo à ser infileirado
        self.sentinel.append(procbcp)

    def get_actual(self): # retorna o atual processos da fila sem incrementar o index
        return self.sentinel[self.indexQueue]

    def get_AIndex(self):
        return self.indexQueue

    def next_index(self):
        self.indexQueue = self.indexQueue + 1
    #def get_prox(self): # retorna o indice do processo atual e ja muda para o proximo elemento da lista, 
    #                    # retornando o indice para o controlador de processos alterar diretamente no bcp correto
    #    actual =  self.indexQueue
    #    if ((self.indexQueue + 1) < len(self.sentinel)):
    #        self.indexQueue = self.indexQueue + 1
    #        return actual
    #    else:
    #        self.indexQueue = 0
    #        return actual
        
    def isEmpty(self):
        if(len(self.sentinel) == 0):
            return True
        else:
            return False
 
   
    def update_WaitingTime(self): #atualiza o tempo de espera de todos
    # recebe por parametro o indice do processo em execucao
        for bcp in range(len(self.sentinel)):
            if(bcp != self.indexQueue):
                self.sentinel[bcp].procWaitingTime += 1

