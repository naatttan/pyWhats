import socket
import os

# from server import Server
# from echange import Echange
from session import Session

class ControlleurServer:
    
    def __init__(self, server):
        self.server = server
        self.echangeur = server.echangeur
        
    # fonction permettant de gérer les connexion des différents utilisateurs
    def accepterConnexions(self):
        self.echangeur.attendreConnexion()
        if self.server.DEBUG:
            print("[Serveur en attente de connexion...]")
        while True:
            conn = self.connexion()
            if conn == 1:
                break
            
    # fonction permettant de créer des sessions utilisateurs lorsqu'ils ont l'authorisation de se connecter, lance un thread contenant le programme de cette session   
    def connexion(self):
        sock_client, addr_client = self.echangeur.acceptConnexion()
        if self.server.DEBUG:
            print(f"[Connexion: {addr_client}]")
        message = self.echangeur.ecouter(sock_client)
        if not message['typeEchange'] == '1': return 3
        if not message['typeMessage'] == '00': return 3
        if not message['erreur'] == '0': return 3
        user = message['data'].split('\\')[0]
        passwd = message['data'].split('\\')[1]
        if user.lower() == 'kill' and self.server.DEBUG:
            return 1
        #### VERIF FICHIER ####
        session = Session(user, sock_client, self.server, addr_client)
        self.server.addSession(session)
        self.server.lancerSession(session)
        self.echangeur.reponseConnexion(sock_client, 0, '')
        if self.server.DEBUG:
            print(f"[Session: {user}]")
        return 0
    
    # fonction permettant d'envoyer un message à tous les utilisateurs connectés appartenant à une conversation
    def synchroniser(self, conv: int, message):
        for user in self.server.listeConvUser.get(conv):
            self.server.liste_session.get(user).synchroniserMessage(message=message)
            
    # fonctin permettant de vérifier l'existence des répertoires de stockage du serveur ou de les créer
    def verifierRepertoire(self) -> bool:
        if not os.path.exists(self.server.filePath):
            os.makedirs(self.server.filePath)
            with open(self.server.listeConvUserPath, 'a+') as fichier:
                pass
            with open(self.server.usersPath, 'a+') as fichier:
                pass
        return True
    
    