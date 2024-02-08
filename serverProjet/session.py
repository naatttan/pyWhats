import socket
import time
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
        self.connecte = False
        
    # fonction d'une session utilisateur en cours
    def run(self):
        self.connecte = True
        time.sleep(0.01)
        self.synchronisation()
        while not self.server.finThreads and self.connecte:
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
                print(f"[Erreur run session] {erreur}")
                break
    
    # fonction permettant de gérer les echanges de connexion
    def echange_connexion(self, rcv):
        match rcv['typeMessage']:
            case '0':
                self.echangeur.reponseConnexion(self.socket, 3, "Vous etes deja connecte.")
            case '1':
                pass
            case '2':
                pass
            case '3':
                self.connecte = False
                self.echangeur.reponseDeconnexion(self.socket, 0, "")
    
    # fonction permettant de gérer les echanges de messages
    def echange_msg(self, rcv):
        match rcv['typeMessage']:
            case '0':
                msg = rcv['data'].split('\\')
                enregistrementMsg = self.controlleur.enregistrerMessage(int(msg[0]), Message(int(msg[0]), msg[1], float(msg[2]), msg[3]))
                self.echangeur.reponseMessage(self.socket, enregistrementMsg[0], enregistrementMsg[1])
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
                #### le nom du fichier et le timer sont passé lors de la demande de token
                #### le fichier doit etre enregistré comme un message ???
                msg = rcv['data'].split('\\')
                repEnvoieFichier = self.controlleur.enregistrerFichier(int(msg[0]), Message(int(msg[0]), msg[1], float(msg[2]), f"~&~{msg[3]}"))
                self.echangeur.reponseEnregistrementFichier(self.socket, repEnvoieFichier[0], repEnvoieFichier[1])
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
                msg = rcv['data'].split('\\')
                telechargement = self.controlleur.telechargementFichier(msg[0], msg[1], msg[2])
                if telechargement[0] == 0 :
                    self.echangeur.telechargementFichierOk(self.socket)
                else:
                    self.echangeur.telechargementFichierErreur(self.socket, telechargement[0], telechargement[1])
            case '2':
                pass
            case '3':
                pass
    
    # fonction permettant de gérer la synchronisation du client
    def synchronisation(self):
        if self.server.DEBUG:
            print(f"[{self.user} synchronisation...]")
        for conv in self.server.listeConvUser.keys():
            if self.user in self.server.listeConvUser.get(conv):
                self.synchroniserConv(self.server.listeConversations.get(conv))
        if self.server.DEBUG:
            print(f"[{self.user} synchronise.]")
    
    def synchroniserConv(self, conv: Conversation):
        self.echangeur.demandeSynchro(self.socket, conv.idConversation)
        rep = self.echangeur.ecouter(self.socket)
        messages = []
        for msg in conv.messages:
            print(msg)
            if msg.getTimer() >= float(rep['data'].split("\\")[2]):
                messages.append(msg)
        self.echangeur.envoieListeMessageSynchro(self.socket, messages)
    
    def synchroniserMessage(self, message: Message):
        self.controlleur.synchroniserMessage(message)
    
    def envoie_message(self):
        pass
    
    def getUser(self):
        return self.user
        