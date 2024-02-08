import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog

class MessagerieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messagerie App")

        # Création des boutons pour sélectionner entre créer une conversation ou voir le profil
        self.create_conversation_button = ttk.Button(root, text="Créer une conversation", command=self.create_conversation)
        self.create_conversation_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.view_profile_button = ttk.Button(root, text="Voir le profil", command=self.view_profile)
        self.view_profile_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Bouton pour se déconnecter
        self.disconnect_button = ttk.Button(root, text="Se déconnecter", command=self.disconnect)
        self.disconnect_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Création de la liste des conversations à gauche
        self.liste_conversations = tk.Listbox(root, width=20, height=15)
        self.liste_conversations.grid(row=4, column=0, padx=5, pady=5, sticky="nsew") # Utilisation de "nsew" pour étirer la liste

        # Ajouter quelques conversations fictives
        conversations = ["Ami 1", "Ami 2", "Ami 3"]
        for conversation in conversations:
            self.liste_conversations.insert(tk.END, conversation)

        # Création de la zone de texte à droite
        self.message_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=24)
        self.message_history.grid(row=1, column=1, rowspan=5, padx=5, pady=5, sticky="nsew") # Utilisation de "nsew" pour étirer la zone de texte

        # Configuration des poids des colonnes et rangées pour qu'elles s'étirent de manière égale
        root.columnconfigure(1, weight=1)
        root.rowconfigure(4, weight=1)

        # Création de l'étiquette pour afficher le nom de la conversation
        self.conversation_label = ttk.Label(root, text="Conversation sélectionnée: ", style="Custom.TLabel")
        self.conversation_label.grid(row=0, column=1, padx=1, pady=1, columnspan=1)

        # Création de la zone de saisie du message en bas de la zone de texte
        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.grid(row=6, column=1, padx=5, pady=(0, 5), columnspan=1, sticky="ew")

        # Bouton d'envoi du message à droite
        send_button = ttk.Button(root, text="Envoyer", command=self.envoyer_message)
        send_button.grid(row=6, column=2, padx=5, pady=(0, 5), sticky="ew")

        # Bouton pour choisir un fichier
        choose_file_button = ttk.Button(root, text="Choisir un fichier", command=self.choisir_fichier)
        choose_file_button.grid(row=7, column=2, padx=5, pady=(0, 5), sticky="ew")

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
        if message:
            self.message_history.insert(tk.END, f"Vous: {message}\n")
            self.message_entry.delete(0, tk.END)

    def create_conversation(self):
        # Crée une nouvelle fenêtre contextuelle (popup) pour créer une nouvelle conversation
        conversation_window = tk.Toplevel(self.root)
        conversation_window.title("Nouvelle Conversation")

        # Zone de saisie de texte pour le nom de la nouvelle conversation
        ttk.Label(conversation_window, text="Nom de la conversation").grid(row=0, column=0, padx=10, pady=10)
        self.new_conversation_entry = ttk.Entry(conversation_window, width=40)
        self.new_conversation_entry.grid(row=0, column=1, padx=10, pady=10)

        # Zone de saisie de texte pour les membres de la nouvelle conversation
        ttk.Label(conversation_window, text="Membre(s)").grid(row=1, column=0, padx=10, pady=10)
        self.new_conversation_members_entry = ttk.Entry(conversation_window, width=40)
        self.new_conversation_members_entry.grid(row=1, column=1, padx=10, pady=10)

        # Bouton pour créer la conversation
        create_button = ttk.Button(conversation_window, text="Créer", command=self.create_new_conversation)
        create_button.grid(row=2, column=1, padx=10, pady=10)

    def create_new_conversation(self):
        # Récupère le contenu des zones de saisie et effectue les actions nécessaires pour créer la conversation
        new_conversation_name = self.new_conversation_entry.get()
        new_conversation_members = self.new_conversation_members_entry.get()
        if new_conversation_name:
            print(f"Création de la conversation avec le nom : {new_conversation_name}")
            print(f"Membres de la conversation : {new_conversation_members}")

    def view_profile(self):
        # Ouvre une nouvelle fenêtre contextuelle (popup) pour afficher le profil de l'utilisateur
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Profil Utilisateur")
        profile_label = ttk.Label(profile_window, text="Contenu du Profil de l'Utilisateur")
        profile_label.pack(padx=10, pady=10)

    def choisir_fichier(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print("Chemin du fichier choisi :", file_path)

    def disconnect(self):
        # Ajoutez ici le code pour se déconnecter de l'application
        print("Déconnexion de l'application")

if __name__ == "__main__":
    root = tk.Tk()
    app = MessagerieApp(root)
    root.mainloop()