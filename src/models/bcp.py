# BLOCO DE CONTROLE DE PROCESSOS ##############
## CLASS BCP                     ##############
### METODOS CONSTRUTORES         ##############
### METODOS UPDATE               ##############
### METODOS FEEDBACK             ##############
###############################################

class BCP: # Bloco de Controle de processos
    def __init__(self, context):

        # INFORMACOES DE PROCESSO
        self.proc_Coust = context[0]     # custo total do processo
        self.procQt_act = context[1]     # quantum consumido parcialmente
        self.schedParam = context[2]    # parametros do schelude
        self.procParent = context[3]    # id do processo pai
        self.procCPUuse = context[4]    # tempo usado da cpu
        self.procGroup = context[5]     # grupo do processo
        self.procIniHr = context[6]     # momento que o processo foi iniciado
        self.procState = context[7]     # estado do processo
        self.procPriority = context[8]  # prioridade do processo
        self.procID = context[9]        # id do processo
 
    def set_procCPUuse(self, use):
        if type(use) == int:
            self.procCPUuse +=  use
        else:
            print("Inserir apenas valores inteiros!!!")

    def set_procPriority(self, priority):
        if type(priority) == int:
            self.procPriority = priority
        else:
            print("Inserir apenas valores inteiros!!!")
    