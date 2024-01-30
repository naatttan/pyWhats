import socket
# from server import Server
from controlleurSession import ControlleurSession
from conversation import Conversation, Message

class Session:
   
    def __init__(self, user_name : str, socket_client: socket, server, addr_client):
        self.user = user_name
        self.socket = socket_client
        self.server = server
        self.echangeur = server.echangeur 
        self.addr_client = addr_client
        self.synchronise = False
        self.controlleur = ControlleurSession(self) # controlleur gérant les fonctionnalités de la session client
        
    # fonction d'une session utilisateur en cours
    def run(self):
        # self.synchronisation()
        while True and not self.server.finThreads:
            try:
                rcv = self.echangeur.ecouter(self.socket)
                match rcv['typeEchange']:
                    case '1':
                        self.echange_connexion(rcv)
                    case '2':
                        self.echange_msg(rcv)
                    case '3':
                        self.echange_envoie_fichier(rcv)
                    case '4':
                        self.echange_telechargement_fichier(rcv)
                    case '5':
                        pass
                    case other:
                        pass
            except Exception as erreur:
                print([f"Erreur: {erreur}"])
                break
    
    # fonction permettant de gérer les echanges de connexion
    def echange_connexion(self, rcv):
        match rcv['typeMessage']:
            case '0':
                pass
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
    
    # fonction permettant de gérer les echanges de messages
    def echange_msg(self, rcv):
        match rcv['typeMessage']:
            case '0':
                msg = rcv['data'].split('//')
                self.controlleur.enregistrerMessage(msg[0], Message(msg[0], msg[1], msg[2], msg[3]))
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
    
    # fonction permettant de gérer les echanges d'envoie de fichiers
    def echange_envoie_fichier(self, rcv):
        match rcv['typeMessage']:
            case '0':
                pass
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
    
    
    # fonction permettant de gérer les echanges de téléchargments de fichiers
    def echange_telechargement_fichier(self, rcv):
        match rcv['typeMessage']:
            case '0':
                pass
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
    
    # fonction permettant de gérer la synchronisation du client
    def synchronisation(self, rcv):
        
        pass
    
    def synchroniserMessage(self, message: Message):
        self.controlleur.synchroniserMessage(message)
    
    def envoie_message(self):
        pass
    
    def getUser(self):
        return self.user
        