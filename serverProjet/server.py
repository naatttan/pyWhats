
import threading
import socket
import os

from session import Session
from conversation import Conversation, Message
from echange import Echange
from controlleurServer import ControlleurServer


class Server:
    
    
    def __init__(self):
        self.liste_session = {}
        self.adresse = 'localhost'
        self.port = 12345
        self.socket: socket.socket
        
        self.echangeur = Echange(self.adresse, self.port, self) # echangeur qui permet de gérer les échanges du serveur
        self.controlleur = ControlleurServer(self) # controlleur qui permet de gérer les fonctionnalités du serveur
        
        self.filePath = './stockage'
        self.listeConvUserPath = self.filePath + "/conv_user"
        self.usersPath = self.filePath + "/users"
        
        self.listeConvUser = {int: []} # listeConvUser -> {numConv: [users]} (contient les identifiants de conversations et les utilisateurs dans ces conversations)
        self.listeConversations = {int: Conversation} # dictionnaire associant les conversations à leurs identifiants
        
        self.lock = threading.Lock()
        self.listeThreads = []
        self.finThreads = False
        
        self.DEBUG = True
            
    
    # fonction principale du serveur
    def run(self):
        self.controlleur.verifierRepertoire()
        self.charger()
        
        self.controlleur.accepterConnexions()
            
        
        self.closeAllSession()
    
    
    def ecouterConnexion(self):
        pass
    
    # fonction permettant de synchroniser tous les utilisateurs d'une conversation et de leur partager les nouveaux messages
    def synchroniserAll(self, conv: int, message: Message):
        self.controlleur.synchroniser(conv, message)
        pass
    
    # fonction permettant d'ajouter une session dans la liste des sessions actives
    def addSession(self, session: Session):
        self.liste_session[session.user] = session
        
    # fonction permettant d'ajouter uneconversation dans la liste des conversations
    def addConversation(self, conv: Conversation):
        self.listeConversations[conv.idConversation] = conv
      
    
    def charger(self):
        self.chargerConversations()
        self.chargerListeConvUser()
        print(self.listeConvUser)
        print(self.listeConversations.keys())
        if self.DEBUG:
            print("[Serveur charge]")  
    
    # fonction permettant de remplir la liste de correspondance des utilisateurs dans les conversations en lisant le fichier qui les contient
    def chargerListeConvUser(self):
        with open(self.listeConvUserPath) as fichier:
            for line in fichier.readlines():
                if line.split("\\")[0] in self.listeConvUser.keys():
                    self.listeConvUser.get(line.split("\\")[0]).append(line.split("\\")[1].strip())
                else:
                    self.listeConvUser[line.split("\\")[0]] = []
                    self.listeConvUser.get(line.split("\\")[0]).append(line.split("\\")[1].strip())
                    
    
    def chargerConversations(self):
        for f in os.listdir(self.filePath):
            try:
                a = int(f)
                if os.path.isdir(self.filePath + "/" + f):
                    conv = Conversation(a, self.controlleur)
                    conv.chargerConversation()
                    self.listeConversations[f] = conv
            except Exception as e:
                print(f"[Erreur chargerConversation] {e}")
                
      
    # fonction permettant de lancer un thread d'une session lorsqu'un utilisateur se connecte
    def lancerSession(self, session: Session):
        threadSession = threading.Thread(target=session.run)
        threadSession.start()
        self.listeThreads.append(threadSession)         
    
    # fonction permettant de fermer tous les threads de sessions avant de finir le programme
    def closeAllSession(self):
        self.finThreads = True
        while len(self.listeThreads) > 0:
            for thread in self.listeThreads:
                thread.join()
                self.listeThreads.remove(thread)
        print("[Tous les threads terminés]")
        # for s in self.liste_session.values():
        #     s.socket.close()
        self.liste_session.clear()
        print("[Toutes les sessions fermées]")
        self.echangeur.fermerSocketServer()
        
        
    # getters
    def getUsersPath(self):
        return self.usersPath
        
        
if __name__ == "__main__":
    server = Server()
    server.run()