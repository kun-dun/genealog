#-------------------------------------------------------------------------------
# Name:        VISGENEALOGLOC
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#              Usadso dashboard.render4.com para expor na WB
#              Vide video YOUTUBE : https://www.youtube.com/watch?v=H16dZMYmvqo
#              Usar com dados in github/genealog e RENDER DASHBOARD
#
# Author:      ylalo
# Version      1   Local
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pyvis.network import Network
import os
import webbrowser
import json


################################################################################
import tkinter as tk
from tkinter import messagebox

# Fonction pour centrer une fenêtre sur l'écran
def center_window(window, width, height):
    # Récupérer le mot de passe depuis une variable d'environnement

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Fonction pour afficher une boîte de dialogue centralisée
def show_centered_messagebox(title, message, type="info"):
    # Créer une fenêtre temporaire invisible pour centrer la boîte de dialogue
    temp_window = tk.Toplevel(root)
    temp_window.withdraw()  # Rendre la fenêtre invisible
    temp_window.attributes("-alpha", 0)  # La rendre complètement transparente
    center_window(temp_window, 300, 200)  # Centrer la fenêtre temporaire

    # Afficher la boîte de dialogue en fonction du type spécifié
    if type == "info":
        messagebox.showinfo(title, message, parent=temp_window)
    elif type == "error":
        messagebox.showerror(title, message, parent=temp_window)
    elif type == "warning":
        messagebox.showwarning(title, message, parent=temp_window)

    # Détruire la fenêtre temporaire après l'affichage de la boîte de dialogue
    temp_window.destroy()

# Fonction pour vérifier le login et le mot de passe
def verifier_login():
    username = entry_username.get()
    password = entry_password.get()
    mot_de_passe = os.getenv("MOTDEPASSE")
    print(mot_de_passe)
    # Remplacez ces valeurs par vos identifiants valides
    username_valide = "admin"
    password_valide = mot_de_passe

    if username == username_valide and password == password_valide:
        # Connexion réussie : afficher un message de succès
        #show_centered_messagebox("Succès", "Connexion réussie !", type="info")
        root.destroy()  # Fermer la fenêtre de login
        lancer_programme()  # Lancer le programme principal
    else:
        # Connexion échouée : afficher un message d'erreur
        show_centered_messagebox("Erreur", "Nom d'utilisateur ou mot de passe incorrect", type="error")
        entry_username.delete(0, tk.END)  # Effacer le champ du nom d'utilisateur
        entry_password.delete(0, tk.END)  # Effacer le champ du mot de passe

# Fonction pour gérer la fermeture de la fenêtre de login
def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        root.destroy()  # Fermer la fenêtre de login
        exit()  # Arrêter complètement le programme

# Fonction pour simuler le lancement du programme principal
def lancer_programme():
    print("Programme lancé avec succès !")
    # Ici, vous pouvez ajouter le code de votre programme principal

# Création de la fenêtre principale
root = tk.Tk()
root.title("Écran de Connexion")
center_window(root, 400, 300)  # Centrer la fenêtre principale

# Gestion de l'événement de fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Configuration du grid pour centrer les éléments
root.grid_rowconfigure(0, weight=1)  # Espace extensible en haut
root.grid_rowconfigure(6, weight=1)  # Espace extensible en bas
root.grid_columnconfigure(0, weight=1)  # Espace extensible à gauche
root.grid_columnconfigure(2, weight=1)  # Espace extensible à droite

# Étiquette et champ pour le nom d'utilisateur
label_username = tk.Label(root, text="Nom d'utilisateur:")
label_username.grid(row=1, column=1, pady=5, sticky="e")  # Aligné à droite
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=2, pady=5, sticky="w")  # Aligné à gauche

# Étiquette et champ pour le mot de passe
label_password = tk.Label(root, text="Mot de passe:")
label_password.grid(row=2, column=1, pady=5, sticky="e")  # Aligné à droite
entry_password = tk.Entry(root, show="*")  # Les caractères du mot de passe sont masqués
entry_password.grid(row=2, column=2, pady=5, sticky="w")  # Aligné à gauche

# Bouton de connexion
btn_login = tk.Button(root, text="Se connecter", command=verifier_login)
btn_login.grid(row=3, column=1, columnspan=2, pady=10)  # Centré sur deux colonnes

# Lancement de la boucle principale Tkinter
root.mainloop()
################################################################################

# Step 1: Create a Pyvis Network object
net = Network(notebook=True, cdn_resources='remote', height="500px", width="100%")

# Step 2: Read data from the external JSON file for nodes
with open('js.txt', 'r', encoding='utf-8') as file:
    nodes = json.load(file)

# Step 3: Add nodes from the JSON data
for node in nodes:
    net.add_node(
        node['id'],
        nom=node['nom'],
        prenoms=node['prenoms'],
        sexe=node['sexe'],
        label=node['label'],
        naissance=node['naissance'],
        villenaiss=node['villenaiss'],
        paynaiss=node['paysnaiss'],
        baptise=node['baptise'],
        marie=node['marie'],
        conjoint=node['conjoint'],
        inhume=node['inhume'],
        deces=node['deces'],
        pere=node['pere'],
        profession=node['profession'],
        photo=node['photo'],
        physics=False,
        color=node['color'],
        x=node['x'],  # Pass x coordinate
        y=node['y']   # Pass y coordinate
    )

# Step 4: Read data from the external JSON file for edges
with open('jsedges.txt', 'r', encoding='utf-8') as file:
    edges = json.load(file)

# Step 5: Add edges between nodes
for edge in edges:
    net.add_edge(edge['from'], edge['to'])

# Step 6: Export the network graph to an HTML file
html_file_path = "index.html"
net.show(html_file_path)

# Step 7: Populate dropdown options with files from a specific directory
def getfiles(pdir):
    directory_path = f"asset/{pdir}"  # Specify the directory containing the files
    file_options = ""
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, file_name)):  # Ensure it's a file
                file_options += f"<option value='{file_name}'>{file_name}</option>"
    return file_options

# Precompute file options for each node
node_file_options = {}
for node in nodes:
    node_id = str(node['id'])  # Ensure node ID is a string
    node_file_options[node_id] = getfiles(node_id)

# Step 8: Inject custom JavaScript into the generated HTML file
nodes_js = json.dumps(nodes)  # Convert nodes to JSON string
edges_js = json.dumps(edges)  # Convert edges to JSON string
node_file_options_js = json.dumps(node_file_options)  # Convert file options to JSON string

custom_js = f"""
<script type="text/javascript">
    // Wait for the network to load
    document.addEventListener("DOMContentLoaded", function() {{
        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: {nodes_js},
            edges: {edges_js}
        }};
        // Precomputed file options for each node
        var nodeFileOptions = {node_file_options_js};
        // Add fixed positions to nodes
        data.nodes.forEach(function(node) {{
            node.x = node.x || 0; // Ensure x is defined
            node.y = node.y || 0; // Ensure y is defined
            node.fixed = {{ x: true, y: true }}; // Fix the position
        }});
        var options = {{
            physics: false, // Disable physics to keep nodes at fixed positions
            nodes: {{
                font: {{
                    size: 12, // Adjust font size for labels
                    face: 'Arial', // Use a consistent font
                    color: '#000000', // Text color
                    align: 'center', // Center-align text inside the box
                    multi: false // Prevent multi-line text
                }},
                shape: 'box', // Use a box shape for nodes
                widthConstraint: {{
                    minimum: 80, // Minimum width for all nodes
                    maximum: 80  // Maximum width for all nodes
                }},
                heightConstraint: {{
                    minimum: 20, // Minimum height for all nodes
                    valign: 'middle' // Vertically center-align the content
                }},
                margin: {{
                    top: 10, // Top margin
                    bottom: 10, // Bottom margin
                    left: 10, // Left margin
                    right: 10 // Right margin
                }},
                borderWidth: 1, // Border thickness
                color: {{
                    border: '#000000', // Border color
                    background: '#ffffff', // Background color
                    highlight: {{
                        border: '#FF0000', // Highlighted border color
                        background: '#FFFF00' // Highlighted background color
                    }}
                }}
            }},
            edges: {{
                color: {{
                    color: '#000000', // Default edge color
                    highlight: '#FF0000', // Color when edge is highlighted
                    hover: '#00FF00' // Color when edge is hovered
                }},
                width: 2 // Edge thickness
            }}
        }};
        var network = new vis.Network(container, data, options);
        // Create a div for displaying node details
        var infoBox = document.createElement('div');
        infoBox.id = 'info-box';
        infoBox.style.position = 'absolute';
        infoBox.style.padding = '10px';
        infoBox.style.backgroundColor = '#f9f9f9';
        infoBox.style.border = '1px solid #ccc';
        infoBox.style.width = '250px';
        infoBox.style.zIndex = '1000';
        infoBox.style.display = 'none'; // Initially hidden
        document.body.appendChild(infoBox);
        // Add event listener for node click
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = data.nodes.find(function(n) {{ return n.id === nodeId; }});
                // Handle missing images with a fallback
                var imagePath = node.photo || 'photos/homme.jpg';
                // Build the info box content dynamically
                var infoContent = "";
                infoContent += "<strong>Node ID:</strong> " + nodeId + "<br>";
                infoContent += "<strong>Nom:</strong> " + node.nom + "<br>";
                infoContent += "<strong>Prenom:</strong> " + node.prenoms + "<br>";
                infoContent += "<strong>Né le:</strong> " + node.naissance + "<br>";
                infoContent += "<strong>à:</strong> " + node.villenaiss + '-' + node.paynaiss + "<br>";
                infoContent += "<strong>Profession :</strong> " + node.profession + "<br>";
                // Conditionally add "Décédé le" only if node.deces exists
                if (node.deces) {{
                    infoContent += "<strong>Décédé le :</strong> " + node.deces + "<br>";
                }}
                // Conditionally add "Inhumé le" only if node.inhume exists
                if (node.inhume) {{
                    infoContent += "<strong>Inhumé le :</strong> " + node.inhume + "<br>";
                }}
                // Conditionally add "à" only if node.lieudeces exists
                if (node.lieudeces) {{
                    infoContent += "<strong>à :</strong> " + node.lieudeces + "<br>";
                }}
                // Add the image tag
                infoContent += "<img id='node-image' src='" + imagePath + "' alt='Image of " + node.nom + "' style='width:100px; margin-top:10px;'>";
                // Add dropdown menus populated with files from the directory
                infoContent += "<hr><strong>Choisir un Document:</strong><br>";
                infoContent += "<select id='file-dropdown' style='margin-bottom: 10px;'>";
                infoContent += nodeFileOptions[nodeId] || "<option>No files available</option>";
                infoContent += "</select>";
                // Update the info box content
                infoBox.innerHTML = infoContent;
                // Add event listener to open the selected file
                var dropdown = document.getElementById('file-dropdown');
                dropdown.addEventListener('change', function() {{
                    var selectedFile = this.value;
                    if (selectedFile) {{
                        var filePath = 'asset/' + nodeId + '/' + selectedFile; // Construct the file path
                        window.open(filePath, '_blank'); // Open the file in a new tab
                    }}
                }});
                // Position the info box near the clicked node
                var position = network.getPositions([nodeId])[nodeId];
                var canvasPosition = network.canvasToDOM({{x: position.x, y: position.y}});
                infoBox.style.top = (canvasPosition.y - 50) + 'px'; // Offset below the node
                infoBox.style.left = (canvasPosition.x + 50) + 'px'; // Offset to the right of the node
                infoBox.style.display = 'block'; // Show the info box
            }} else {{
                infoBox.style.display = 'none'; // Hide the info box if no node is clicked
            }}
        }});
    }});
</script>
"""

# Step 9: Modify the HTML file to include the custom JavaScript
with open(html_file_path, "r") as file:
    html_content = file.read()


# Add a styled title to the page (visible on the page itself)
html_content = html_content.replace(
    "<body>",
    """
    <body>
        <h1 style='
            text-align: center;
            margin-top: 20px;
            font-family: Arial, sans-serif;
            color: #4CAF50;
            font-size: 36px;
        '>Arbre Généalogique Laloë(1.0)</h1>

        <h1 style='
            text-align: center;
            margin-top: 20px;
            font-family: Arial, sans-serif;
            color: #4CAF50;
            font-size: 16px;
        '>(Zoom: Roule la souris)</h1>
    """
)

# Inject the custom JavaScript before the closing </body> tag
html_content = html_content.replace("</body>", custom_js + "</body>")

# Write the modified HTML content back to the file
with open(html_file_path, "w") as file:
    file.write(html_content)

#print(f"Custom JavaScript injected into {html_file_path}")

# Open the HTML file in the default web browser
webbrowser.open(html_file_path)