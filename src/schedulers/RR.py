# ESCALONADOR ROUND ROBIN ###############
## CLASS RR                     #########
### METODOS PARA ATUALIZAR BCP  #########


class RR: 
    def __init__(self, Qt):
        self.Quantum = Qt 

    ## UPDATE BCP DO PROCESSO #################################################################################
    # metodo chamado uma vez para cada quantum de cada processo na fila de prontos                            #
    # o metodo invocador deve checar o procState a cada execucao                                              #
    # quando o status muda, o metodo invocador deve mudar o processo de fila ou posicao na fila               #
    def update_BCPQt(self, bcp): # em cada quantum atualiza as informações do bcp do processo em execucao     #
        if ((bcp.procQT_act < self.Quantum) and (bcp.procCPUuse < bcp.proc_Coust )):
            if (bcp.procQT_act == (self.Quantum -1)):
                bcp.procQT_act = bcp.procQT_act + 1
                bcp.procCPUuse = bcp.procCPUuse + 1
                bcp.procState = 'pronto'
            else:
                bcp.procQT_act = bcp.procQT_act + 1
                bcp.procCPUuse = bcp.procCPUuse + 1
                bcp.procState = 'executando'
        
        elif(bcp.procCPUuse == bcp.proc_Coust ): # se ja usou tudo q precisava
            bcp.procState = 'terminado'

             
