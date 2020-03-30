# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 22:16:21 2020

@author: khalilchouchen modifié par Romaric 
"""

import threading
import socket
import select

class EnodeB(threading.Thread):
    """Station de Base"""
    def __init__(self,identifier,ip,port):
        threading.Thread.__init__(self)
        self.identifier=identifier
        self.port=port
        self.ip=ip
        print("La station de base {0} est crée \n".format(self.identifier))
    
    def getId(self):
        return self.identifier
    
    def getPort(self):
        return self.port
    
    def getIp(self):
        return self.ip
   
    def setConnectedbaseStation(self,EnodeB):
        self.connectedBaseStation=EnodeB
    
    def connectTobaseStation(self,EnodeB):
        self.setConnectedbaseStation(EnodeB)
        socket_between_servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_between_servers.bind((self.connectedBaseStation.getIp(),self.connectedBaseStation.getPort()))
        print("La station de base {0} est connectée à la station de base {1} \n".format(self.identifier,self.connectedBaseStation.getId()))
    
    def run(self):
        print("la station de base {0} est démarré \n".format(self.identifier))
        self.connexion_avec_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.connexion_avec_clients.bind(('',self.port))
        except socket.error :
            print("binding failed")
            
        
        self.connexion_avec_clients.listen(5)
        print("La station de base {0} écoute à présent sur le port {1}:{2} \n".format(self.identifier,self.ip,self.port))
        
        self.serveur_lance = True   
        self.mobiles_connectes=[]
        while (self.serveur_lance):
            # On va vérifier que de nouveaux clients ne demandent pas à se connecter
            # Pour cela, on écoute la connexion_principale en lecture
            # On attend maximum 50ms
            connexions_demandees, wlist, xlist = select.select([self.connextion_avec_clients],[], [], 0.05)
            for connexion in connexions_demandees:
                connexion_avec_mobile, infos_connexion = connexion.accept()
                # On ajoute le socket connecté à la liste des clients
                self.mobiles_connectes.append(connexion_avec_mobile)
            # Maintenant, on écoute la liste des clients connectés
            # Les clients renvoyés par select sont ceux devant être lus (recv)
            # On attend là encore 50ms maximum
            # On enferme l'appel à select.select dans un bloc try
            # En effet, si la liste de clients connectés est vide, une exception
            #Peut être levée        
            mobiles_a_lire = []
            try:
                mobiles_a_lire, wlist, xlist = select.select(self.mobiles_connectes,[], [], 0.05)
            except select.error:
                    pass
            else:
                self.reception(mobiles_a_lire)
                
#        print("Fermeture des connexions")
#        for mobile in self.mobiles_connectes:
#            mobile.close()
#        connexion_avec_client, infos_connexion = bs.accept()

        

    def reception(self,mobiles_a_lire):
        self.nb_mobile_ferme=0
        # On parcourt la liste des clients à lire
        for mobile in mobiles_a_lire:
            # Client est de type socket
            msg_recu_du_mobile = mobile.recv(1024)
            msg_recu_du_mobile = msg_recu_du_mobile.decode()
            if msg_recu_du_mobile!="":
                # Peut planter si le message contient des caractères spéciaux
                print("{0} a reçu {1} \n".format(self.identifier,msg_recu_du_mobile))
                mobile.send("msg recu".encode())
            if msg_recu_du_mobile=="fin":
                self.nb_mobile_ferme=+1
                mobile.close()
                        
            if(self.nb_mobile_ferme==2): #nombre de mobile connecte a la station de base
                print("closing")
                self.serveur_lance = False
  
            #ACK
#            self.emission(mobile,"msg reçu")
#            if msg_recu_du_mobile == "fin":
#                self.serveur_lance = False
   
    
    def emission(self,mobile_a_qui_envoyer,msg_a_envoyer):
        mobile_a_qui_envoyer.send(msg_a_envoyer.encode())
    
    def closeBaseStation(self):
        print("La station de base{0} est fermeé \n".format(self.identifier))
        self.connextion_avec_clients.close()
        
        
    

