# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt
#import numpy as np
class Gantt:
    def __init__(self, processNames ):
        self.fig, self.gnt = plt.subplots() 
 
        self.list_consun = []

    def construc_graph(self, processNames):
        base = 10
        jumpbase = 10
        spec = 9
        self.gnt.set_ylim(0, 50) 
        self.gnt.set_xlim(0, 160) 

        # Setting labels for x-axis and y-axis 
        self.gnt.set_xlabel('seconds since start') 
        self.gnt.set_ylabel('Processo') 



        # Declaring a bar in schedule
        acumulado = []
        anterior = 'name'
        contador = 0
        setnome = []
        for nome in processNames:
            setnome.append(nome[0])

        setnome = list(set(setnome))
        ytickss = []
        initn = 15
        for name in setnome:
            ytickss.append(name)
        # Setting ticks on y-axis 
        self.gnt.set_yticks(ytickss) 



        # Labelling tickes of y-axis 
        self.gnt.set_yticklabels(setnome) 
        # Setting graph attribute 
        self.gnt.grid(True) 
        for name in setnome:
            multiplus = []
            for proc in processNames:
                if(proc[0] == name):
            
                    multiplus.append(proc)
            acumulado.append(multiplus)

        print(acumulado) 
        print(setnome)

        #for nome in nomes:
        #    print(nome)

        #    contador += 1


        # for TESTE
        # Declaring a bar in schedule 
        self.gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange')) 
  
        # Declaring multiple bars in at same level and same width 
        self.gnt.broken_barh([(110, 10), (150, 10)], (10, 9), 
                         facecolors ='tab:blue') 
  
        self.gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9), 
                                  facecolors =('tab:red')) 

        self.gnt.broken_barh([(130, 150)], (40, 9), 
                                  facecolors =('tab:red')) 
        ####################################  
           



        print(self.list_consun)
                
        #for process in self.list_consun:
        #    print(process)
        #    self.gnt.broken_barh(process, (base+jumpbase, spec), facecolors =('tab:red')) 
        #    base = base+jumpbase
       
            
        plt.savefig("gantt1.png") 
