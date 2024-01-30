import os

# from session import Session
# from conversation import Conversation, Message


class ControlleurSession:
    
    
    def __init__(self, session):
        self.session = session
        self.echangeur = self.session.echangeur
    
    def enregistrerMessage(self, conv: int, message):
        self.session.server.listeConversations.get(conv).addMessage(user=message.user, timer=message.timer, texte=message.texte)
        self.session.server.synchroniserAll(conv)
        pass
    
    def verifierConnexion(self, user: str, password: str):
        pass
    
    def enregistrerFichier(self, conv: int, fichier):
        pass
    
    def verifierConversationExistante(self, conv: int) -> bool:
        return os.path.exists(self.session.server.filePath + "/" + conv)
    
    def synchroniserMessage(self, message):
        self.echangeur.envoieMessageSynchro(self.session.socket, message)
    