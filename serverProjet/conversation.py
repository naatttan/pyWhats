import os
# from controlleurServer import ControlleurServer

class Conversation:
    
    def __init__(self, id, controlleur):
        self.server = controlleur.server
        self.idConversation: int = id
        self.messages = []
       
       
    # fonction permettant de créer une conversation et de créer son répertoire de stockage 
    def creer(self, conv: int, users: []):
        self.idConversation = conv
        os.makedirs(self.server.filePath + "/" + str(conv) + "/fichiers")
        with open(self.server.filePath + "/" + str(conv) + '/messages', 'a+') as fichier:
            pass
        with open(self.server.listeConvUserPath) as fichier:
            for user in users:
                fichier.write(str(self.idConversation) + "\\" + user)
        self.server.addConversation(self)
            
     
    # fonction permettant d'ajouter un message à une conversation et de l'enregistrer dans les fichiers de la conversation   
    def addMessage(self, user: str, timer: float, texte: str):
        self.messages.append(Message(self.idConversation ,user, timer, texte))
        with open(self.server.filePath + "/" + str(self.idConversation) + '/messages', 'a+') as fichier:
            fichier.write(f"{timer}\\{user}\\{texte}\n")
                
    
    # fonction permettant de charger les messages d'une conversation en lisant les fichiers de la conversation
    def chargerConversation(self):
        with open(self.server.filePath + "/" + str(self.idConversation) + '/messages', 'r') as fichier:
            for line in fichier.readlines():
                self.messages.append(Message(self.idConversation ,line.split("\\")[1], float(line.split("\\")[0]), line.split("\\")[2].strip()))
                
                
            
    

   
class Message:
    
    def __init__(self, conv: int, user: str, timer: float, texte: str):
        self.conv = conv
        self.user = user
        self.timer = timer
        self.texte = texte
        
    def getUser(self):
        return self.user
    
    def getTimer(self):
        return self.timer