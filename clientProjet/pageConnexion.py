import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importer les modules de Pillow pour manipuler les images

class ConnexionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")

        # Charger l'image
        image_path = "logopyt.jpg"
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.ANTIALIAS)  # Redimensionner l'image si nécessaire
        self.logo = ImageTk.PhotoImage(image)

        # Afficher l'image dans un Label
        self.logo_label = ttk.Label(root, image=self.logo)
        self.logo_label.grid(row=0, columnspan=2, padx=5, pady=5)

        self.label_pseudo = ttk.Label(root, text="Pseudo:")
        self.label_pseudo.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.pseudo_entry = ttk.Entry(root)
        self.pseudo_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_password = ttk.Label(root, text="Mot de passe:")
        self.label_password.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.connexion_button = ttk.Button(root, text="Connexion", command=self.connexion)
        self.connexion_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def connexion(self):
        pseudo = self.pseudo_entry.get()
        password = self.password_entry.get()

        # Ici vous pouvez mettre la logique de vérification du pseudo et du mot de passe
        # Pour cet exemple, je vérifie si les champs ne sont pas vides
        if pseudo and password:
            messagebox.showinfo("Connexion réussie", f"Bienvenue, {pseudo} !")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo et un mot de passe.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnexionApp(root)
    root.mainloop()