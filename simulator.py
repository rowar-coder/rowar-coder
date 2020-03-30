# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:09:08 2020

@author: rom_w
"""

from EnodeB import *
from UE import *
import socket
import time


class simulator:
    def __init__(self):
        print("creating DataBase")
        self.mobiles=[]
        self.baseStations=[]
        
    def addMobile(self,mobile):
        self.mobiles.append(mobile)
    
    def addBaseStation(self,baseStation):
        self.baseStations.append(baseStation)
    def createNetwork(self):
#        démarer les stations de base
        self.network= {'M1':'BS1','M2':'BS1','M3':'BS2','M4':'BS2'}
#        ,'M3':'BS2','M4':'BS2','BS1':'BS2'} 
        for b in self.baseStations:
            b.start()
            time.sleep(1)
#         démarer et connecter les mobiles aux stations de base
        for key, value in self.network.items():
            if(key.startswith('M')):
                mobileIndex=self.findMobilebyId(key)
                self.mobiles[mobileIndex].setConnectedbaseStation(self.baseStations[self.findBaseStationbyId(value)])
                self.mobiles[mobileIndex].start()
            else:
                baseStationIndex=self.findBaseStationbyId(key) 
                self.baseStations[baseStationIndex].connectToBaseStation(self.baseStations[self.findBaseStationbyId(value)])                
              
    