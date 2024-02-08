
class Interface:
    def __init__(self):
        pass
    
    def apresConnexion(self):
        message = input("Que voulez-vous faire ? 1- Créer une conversation 2- Afficher mes conversations \n 3- Afficher mon profil \n 4- break")
        return message
        
    def affichageConversations(self):
        message = input("Quelle conversation voulez-vous ouvrir ?")
        return message
        
    def interieurConversation(self):
        message = input("Que voulez-vous faire ? 1- Envoyer un message \n 2- Envoyer un fichier 3- Télécharger un fichier")
        return message
    
    