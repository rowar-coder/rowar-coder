# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:04:23 2020

@author: rom_w
"""

import socket
import threading

class UE(threading.Thread): 
    
    def __init__(self,identifier):
        threading.Thread.__init__(self)
        self.identifier=identifier
        print("Mobile {0} est crée \n".format(self.identifier))
        
    def getId(self):
        return self.identifier

    def setConnectedbaseStation(self,baseStation):
        self.connectedBaseStation=baseStation
    
    def run(self):
        print("mobile {0} est démarré \n".format(self.identifier))
        self.connexion_avec_bs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_avec_bs.connect((self.connectedBaseStation.getIp(),self.connectedBaseStation.getPort()))
        print("mobile {0} est connecté à la station de base {1} \n".format(self.identifier,self.connectedBaseStation.getId()))
        self.emission()
#        self.emission("hello i am mobile {0} \n".format(self.identifier))
#        self.reception()
        
#        msg_recu = connexion_avec_bs.recv(1024)
#        print("{0} recieved: {1} \n".format(self.identifier,msg_recu.decode()))
#        while msg_a_envoyer != "fin":
#            msg_a_envoyer = input("{0} > ".format(self.identifier))
#            # Peut planter si vous tapez des caractères spéciaux
#            msg_a_envoyer = msg_a_envoyer.encode()
#            # On envoie le message
#            connexion_avec_bs.send(msg_a_envoyer)
#            msg_recu = connexion_avec_bs.recv(1024)
#            print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents

    def emission(self):
        msgs_a_envoyer=["hello from {0} \n".format(self.identifier),"im mobile {0} \n".format(self.identifier),"this is a test from {0} \n".format(self.identifier),"fin"]
        i=0;
        while i<len(msgs_a_envoyer):
            msg_a_envoyer = msgs_a_envoyer[i]
            # Peut planter si vous tapez des caractères spéciaux
            msg_a_envoyer = msg_a_envoyer.encode()
            # On envoie le message
            self.connexion_avec_bs.send(msg_a_envoyer)
            self.reception()
            i=i+1;
#           msg_a_envoyer = msg_a_envoyer.encode()
#           self.connexion_avec_bs.send(msg_a_envoyer)
    
    def reception(self):
        msg_recu = self.connexion_avec_bs.recv(1024)
        print("{0} recieved: {1} \n".format(self.identifier,msg_recu.decode()))
        
    def close(self):  
       print("Le mobile {0} est fermeé \n".format(self.identifier))
       self.connexion_avec_bs.close()      
        