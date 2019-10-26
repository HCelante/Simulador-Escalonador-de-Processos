# ESCALONADOR ROUND ROBIN ###############
## CLASS RR                     #########
### METODOS PARA ATUALIZAR BCP  #########
import src.models.bcp as bcp

class RR: 
    def __init__(self, Qt):
        self.Quantum = Qt 

    ## UPDATE BCP DO PROCESSO #################################################################################
    # metodo chamado uma vez para cada quantum de cada processo na fila de prontos                            #
    # o metodo invocador deve checar o procState a cada execucao                                              #
    # quando o status muda, o metodo invocador deve mudar o processo de fila ou posicao na fila               #
    def update_BCPQt(self, bcp): # em cada quantum atualiza as informações do bcp do processo em execucao     #
        if ((bcp.procQTCons < self.Quantum) and (bcp.procCPUuse < bcp.procBurstTime )): # se tem quantum pra consumir 
            if (bcp.procQTCons == (self.Quantum -1)):      # se esta para consumir seu ultimo quantum dessa execucao
                bcp.procQTCons = bcp.procQTCons + 1        
                bcp.procCPUuse = bcp.procCPUuse + 1
                bcp.procState = 0                   # fica pronto
            else:                                          # se nao
                bcp.procQTCons = bcp.procQTCons + 1
                bcp.procCPUuse = bcp.procCPUuse + 1
                bcp.procState = 1               # continua executando
        
        elif(bcp.procCPUuse == bcp.procBurstTime ):           # se ja usou tudo q precisava
            bcp.procState = 2                    # termina o processo
        
        else:
            print("Nao consumido, conferir o codigo!")

             
