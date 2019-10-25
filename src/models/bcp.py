# BLOCO DE CONTROLE DE PROCESSOS ##############
## CLASS BCP                     ##############
### METODOS CONSTRUTORES         ##############
### METODOS UPDATE               ##############
### METODOS FEEDBACK             ##############
###############################################

class BCP: # Bloco de Controle de processos
    def __init__(self, context):

        # INFORMACOES DE PROCESSO
        self.procID = context[0]
        self.procDuration = context[1]     # duracao do processo
        self.procPriority = context[2]  # prioridade do processo
        self.procIniHr = context[3]     # momento que o processo foi iniciado
        self.procIOTime = context[4 :]
        
        # self.procQt_act = context[1]     # quantum consumido parcialmente
        # self.schedParam = context[2]    # parametros do schelude
        # self.procParent = context[3]    # id do processo pai
        # self.procCPUuse = context[4]    # tempo usado da cpu
        # self.procGroup = context[5]     # grupo do processo
        # self.procState = context[7]     # estado do processo
        
 
    def set_procCPUuse(self, use):
        if type(use) == int:
            #self.procCPUuse +=  use
            pass
        else:
            print("Inserir apenas valores inteiros!!!")

    def set_procPriority(self, priority):
        if type(priority) == int:
            self.procPriority = priority
        else:
            print("Inserir apenas valores inteiros!!!")
    