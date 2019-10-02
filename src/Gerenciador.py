import bcp
import filaGC as fila


# GERENCIADOR DE PROCESSOS #######################################################
class Gerenciador:                              # Gerenciador de processos
    def __init__(self):                         # metodo inicializador
        self.Timestamp      = 0                 # tempo da cpu
        self.filadeBloq     = fila.Queue(True)  # fila de bloqueados
        self.filadePron     = fila.Queue(False) # fila de prontos
        self.filadeNCri     = fila.Queue(False) # fila de processos nao criados

    # METODOS DE GERENCIA ########################################################
    def consome(self):                      # consome os processos
        pass
    

    # METODOS DE FEEDBACK ########################################################
    def calculaTME(self):                   # calcula tempos medio de espera
        pass

    def calculaTTE(self):                   # calcula tempo total de espera
        pass
    
    def calculaThrgpt(self):                # calcula throughput do sistema
        pass

    def calculaTMTMF(self):                 # calcula tamanho maximo e medio das filas
        pass

    def calculaTRM(self):                   # calcula tempo de resposta medio
        pass
