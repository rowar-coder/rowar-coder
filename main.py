#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:37:45 2019

@author: khalilchouchen modifié par Romaric 
"""

from simulator import *
from UE import *
from EnodeB import *

import time


#some function that will be used later in the script
def findBaseStationbyId(baseStationId):    
   for x in range(0, len(baseStations)):
      if baseStations[x].getId()==baseStationId:
          break
   return x
    
def findMobilebyId(mobileId):
   for x in range(0, len(mobiles)):
     if mobiles[x].getId()==mobileId:
         break
   return x


#create DataBase
Simulateur= simulator()

#create mobiles and baseStations
mobiles=[]
M1 = UE('M1')
M2 = UE('M2')
M3 = UE('M3')
M4 = UE('M4')
mobiles.append(M1)
mobiles.append(M2)
mobiles.append(M3)
mobiles.append(M4)


baseStations=[]
BS1=EnodeB('BS1','127.0.0.1',8000)
BS2=EnodeB('BS2','127.0.0.1',8001)


baseStations.append(BS1)
baseStations.append(BS2)

#update 
Simulateur.addMobile(M1)
Simulateur.addMobile(M2)
Simulateur.addMobile(M3)
Simulateur.addMobile(M4)

#start the baseStations
for b in baseStations:
    b.start()
    time.sleep(1)

#create Network and start mobiles
network= {'M1':'BS1','M2':'BS1','M3':'BS2','M4':'BS2'}
for key, value in network.items():
    if(key.startswith('M')):
        mobileIndex=findMobilebyId(key)
        mobiles[mobileIndex].setConnectedbaseStation(baseStations[findBaseStationbyId(value)])
        mobiles[mobileIndex].start()
    else:
        baseStationIndex=findBaseStationbyId(key) 
        baseStations[baseStationIndex].connectToBaseStation(baseStations[findBaseStationbyId(value)])                



