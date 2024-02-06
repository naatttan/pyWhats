import socket
import os
import difflib

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
            sock_client, addr_client = self.echangeur.acceptConnexion()
            if self.server.DEBUG:
                print(f"[Connexion: {addr_client}]")
            conn = self.connexion(sock_client, addr_client)
            if conn in [5]:
                sock_client.close()
                break
            
    # fonction permettant de créer des sessions utilisateurs lorsqu'ils ont l'authorisation de se connecter, lance un thread contenant le programme de cette session   
    def connexion(self, sock_client, addr_client):
        message = self.echangeur.ecouter(sock_client)
        if message == None: return 3
        if not message['typeEchange'] == '1': return 3
        if not message['typeMessage'] == '0': return 3
        if not message['erreur'] == '0': return 3
        user = message['data'].split('\\')[0]
        passwd = message['data'].split('\\')[1]
        if user.lower() == 'kill' and self.server.DEBUG:
            return 5
        # verification user password
        with open(self.server.getUsersPath(), 'r', encoding="utf-8") as file:
            accept = False
            for line in file.readlines():
                if line.strip() == f"{user}\\{passwd.strip()}":
                    accept = True
                    break
            if not accept:
                self.echangeur.reponseConnexion(sock_client, 1, "Ce profil n'existe pas")
                return 1
        session = Session(user, sock_client, self.server, addr_client)
        self.server.addSession(session)
        self.server.lancerSession(session)
        self.echangeur.reponseConnexion(sock_client, 0, '')
        if self.server.DEBUG:
            print(f"[Session: {user}]")
        return 0
    
    # fonction permettant d'envoyer un message à tous les utilisateurs connectés appartenant à une conversation
    def synchroniser(self, conv: int, message):
        for user in self.server.listeConvUser.get(str(conv)):
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
    
    