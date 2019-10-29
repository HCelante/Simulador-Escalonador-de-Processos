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
        self.procPriority = context[2]      # prioridade do processo
        self.procIOTime = context[4 :]      # eventos de IO
        self.procQtCons = 0                 # quantum consumido
        self.procState = 0                  # estado do processo 0 para pronto 1 para executando -1 para bloqueado 2 para terminado
        self.procBurstTime = context[1]     # duracao do processo
        self.totalBt = context[1]           # duracao total do burst time
        self.procArrivalTime = context[3]   # momento que o processo foi iniciado
        self.procCompletionTime = 0         # momento que o processo foi finalizado
        self.procResponseTime = 0           # tempo de resposta do processo
        self.procTurnaroundTime = 0         # tempo total de execução do processo
        self.procWaitingTime = 0            # tempo de espera do processo na fila de pronto
        self.procCPUuse = 0                 # tempo gasto da cpu
        self.timeBlockRemain = 0            # tempo restante de bloqueio
        self.tempoRespMedio = 0
    
    def calculate_Turnaround(self):
        self.procTurnaroundTime = self.procCompletionTime - self.procArrivalTime
        
    def calculate_Waiting(self):
        self.procWaitingTime = self.procTurnaroundTime - self.totalBt
        