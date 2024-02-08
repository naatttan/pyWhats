import tkinter as tk
from tkinter import scrolledtext
import threading
from client import Client

class MessagerieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messagerie App")
        self.client = Client()
        
        self.listen_thread = threading.Thread(target=self.ecouterMessages)
        self.listen_thread.daemon = True 
        self.listen_thread.start()

        # Titre "Conversations"
        self.conversations_title = tk.Label(root, text="Conversations")
        self.conversations_title.grid(row=0, column=0, padx=0, pady=0, sticky=tk.W)

        # Création de la liste des conversations à gauche
        self.liste_conversations = tk.Listbox(root, width=20, height=18)
        self.liste_conversations.grid(row=1, column=0, padx=0, pady=0, rowspan=9)

        # Ajouter quelques conversations fictives
        conversations = ["Ami 1", "Ami 2", "Ami 3"]
        for conversation in conversations:
            self.liste_conversations.insert(tk.END, conversation)

        # Création de la zone de texte à droite
        self.message_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=24)
        self.message_history.grid(row=1, column=1, columnspan=10, padx=0, pady=0)

        # Création de l'étiquette pour afficher le nom de la conversation
        self.conversation_label = tk.Label(root, text="Conversation sélectionnée: ")
        self.conversation_label.grid(row=0, column=1, padx=0, pady=0, columnspan=2)

        # Création de la zone de saisie du message en bas de la zone de texte
        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.grid(row=11, column=1, padx=0, pady=0, columnspan=1)

        # Bouton d'envoi du message à droite
        send_button = tk.Button(root, text="Envoyer", command=self.envoyer_message)
        send_button.grid(row=11, column=2, padx=0, pady=0)

        # Liaison de la fonction à appeler lorsque la sélection de la liste change
        self.liste_conversations.bind('<<ListboxSelect>>', self.maj_conversation_label)

    def maj_conversation_label(self, event):
        # Mettre à jour l'étiquette avec le nom de la conversation sélectionnée
        selected_conversation_index = self.liste_conversations.curselection()
        if selected_conversation_index:
            selected_conversation = self.liste_conversations.get(selected_conversation_index)
            self.conversation_label.config(text=f"Conversation sélectionnée: {selected_conversation}")

    def envoyer_message(self):
        message = self.message_entry.get()
        self.client.envoyermsg(message)
    
    def afficherMessage(self, message):
        self.message_history.insert(tk.END, f"Vous: {message}\n")
        self.message_entry.delete(0, tk.END)

    #def afficherMessage(self, message):
            #self.message_history.insert(tk.END, f"Vous: {message}\n")
        #self.message_entry.delete(0, tk.END)
        
    def ecouterMessages(self):
        while True:
            message = self.client.recevoir_requete()  # Utiliser la méthode du client pour recevoir les messages
            self.afficherMessage(message)
    
    #def recevoir_requete(self):
        #response = self.client.s.recv(1024).decode("utf-8")
        #self.afficherMessage(response)

interface = MessagerieApp()  

if __name__ == "__main__":
    root = tk.Tk()
    app = MessagerieApp(root)
    root.mainloop() 
    

