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
        


    def queueOne(self, procbcp):# recebe o bloco de controle de processo referente ao processo à ser infileirado
        if type(procbcp) == bcp:
            self.sentinel.append(procbcp)
        else:
            print("Inserir apenas itens do tipo bcp.")

    def get_prox(self): # retorna o indice do processo atual e ja muda para o proximo elemento da lista, retornando o indice para o controlador de processos alterar diretamente no bcp correto
        actual =  self.indexQueue
        if ((self.indexQueue + 1) < len(self.sentinel)):
            self.indexQueue = self.indexQueue + 1
            return actual
        else:
            self.indexQueue = 0
            return actual
        
    def isEmpty(self):
        if(len(self.sentinel) == 0):
            return True
        else:
            return False
 
   
