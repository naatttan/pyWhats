import os

# from session import Session
# from conversation import Conversation, Message


class ControlleurSession:
    
    
    def __init__(self, session):
        self.session = session
        self.echangeur = self.session.echangeur
    
    def enregistrerMessage(self, conv: int, message):
        if not message.getUser() in self.session.server.listeConvUser.get(str(conv)): return (1, "Vous n'avez pas accès à cette conversation.")
        if message.user != self.session.user: return (1, f"Vous n'etes pas connecté en tant que {message.user}")
        self.session.server.listeConversations.get(str(conv)).addMessage(user=message.user, timer=message.timer, texte=message.texte)
        self.session.server.synchroniserAll(conv, message)
        self.echangeur.reponseMessage(self.session.socket, 0, "")
        return (0, "")
    
    def verifierConnexion(self, user: str, password: str):
        pass
    
    def enregistrerFichier(self, conv: int, fichier):
        pass
    
    def telechargementFichier(self, conv: int, nomFichier: str):
        if not os.path.isdir(self.session.server.filePath + "/" + str(conv)): return (2, f"La conversation {conv} n'existe pas.")
        if not os.path.isfile(self.session.server.filePath + "/" + str(conv) + "/fichiers/" + nomFichier): return (2, f"La conversation {conv} n'a pas de fichier {nomFichier}.")
        try:
            self.echangeur.telechargementFichier(self.session.socket, self.session.server.filePath + "/" + str(conv) + "/fichiers/" + nomFichier)
            return (0, "")
        except Exception as e:
            return (3, "Erreur lors de l'envoie du fichier")
    
    def verifierConversationExistante(self, conv: int) -> bool:
        return os.path.exists(self.session.server.filePath + "/" + conv)
    
    def synchroniserMessage(self, message):
        self.echangeur.envoieMessageSynchro(self.session.socket, message)
    