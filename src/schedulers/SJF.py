# ESCALONADOR SHORTEST JOB FIRST

from src.models.bcp import BCP
from random import randrange

class SJF: 
  def __init__(self, confs):
    self.minIOTime = confs[0]
    self.maxIOTime = confs[1]
    self.IOTime = self.randomIOTime()
  
    
  def executeSJF(self, bcp, timestamp): 

    for i in range (len(bcp.procIOTime)):
      if (bcp.procIOTime[i] == timestamp):
        print("Bloqueado para IO, durante " + str(self.IOTime) + " unidades de tempo")
        bcp.timeBlockRemain = self.IOTime - 1
        bcp.procState = -1

    if (bcp.procState == 0 or bcp.procState == 1):
      if (bcp.procBurstTime > 0 ):
        print ("entrei")
        bcp.procState = 1
        bcp.procBurstTime -= 1
        bcp.procCompletionTime = timestamp
        bcp.procCPUuse += 1
      else: 
        bcp.procState = 2

    return bcp

  def selectProc (self, ReadyQueue):
    selectedIndex = 0
    burstTest = ReadyQueue.sentinel[0].procBurstTime
    
    for i in range(len(ReadyQueue.sentinel)):
      if (ReadyQueue.sentinel[i].procBurstTime < burstTest):
        burstTest = ReadyQueue.sentinel[i].procBurstTime
        selectedIndex = i
        
    return selectedIndex
  
  def randomIOTime(self):
    value = randrange(self.minIOTime, self.maxIOTime)
    return value