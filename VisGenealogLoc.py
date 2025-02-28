from pyvis.network import Network
import os
import webbrowser
import json

html_file_path = "index.html"
# Step 1: Create a Pyvis Network object
net = Network(notebook=True, cdn_resources='remote', height="500px", width="100%")
# Configurando o zoom inicial
# Configure les options pour un zoom initial plus grand
scale = 0.7
jscale = json.dumps(scale)
options = """
{
  "physics": {
    "enabled": false
  },
  "interaction": {
    "zoomView": true,
    "dragView": true,
    "initialScale": 0.8,
    "hover": true
  },
  "manipulation": {
    "enabled": false
  },
  "edges": {
    "smooth": false
  },
  "layout": {
    "randomSeed": 42
  },
  "configure": {
    "enabled": false
  }
}
"""

net.set_options(options)

# Exibindo o gráfico
net.show(html_file_path)

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
net.show(html_file_path)

# Step 7: Populate dropdown options or direct link with files from a specific directory
def getfiles(pdir):
    directory_path = f"asset/{pdir}"  # Specify the directory containing the files
    file_options = []
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, file_name)):  # Ensure it's a file
                file_options.append(file_name)
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
                color: {{ // Default edge color (if not specified in JSON)
                    color: '#000000',
                    highlight: '#FF0000', // Color when edge is highlighted
                    hover: '#00FF00'      // Color when edge is hovered
                }},
                width: 2
            }}
        }};
        var network = new vis.Network(container, data, options);

        // Applique le zoom initial et se concentre sur un nœud spécifique au début
        var nodeIdToFocusOn = 75;  // ID du nœud sur lequel se concentrer
        var position = network.getPositions([nodeIdToFocusOn])[nodeIdToFocusOn];
        network.moveTo({{
            position: {{
                x: position.x,
                y: position.y
            }},
                scale: {jscale}  // Le niveau de zoom initial
        }});

        // Crée une boîte d'information
        var infoBox = document.createElement('div');
        infoBox.id = 'info-box';
        infoBox.style.position = 'absolute';
        infoBox.style.padding = '10px';
        infoBox.style.backgroundColor = '#f9f9f9';
        infoBox.style.border = '1px solid #ccc';
        infoBox.style.width = '250px';
        infoBox.style.zIndex = '1000';
        infoBox.style.display = 'none'; // Initialement caché
        document.body.appendChild(infoBox);

        // Ajoute un gestionnaire d'événements pour afficher les informations du nœud
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = data.nodes.find(function(n) {{ return n.id === nodeId; }});
                var imagePath = node.photo || 'photos/homme.jpg';
                var infoContent = "";
                infoContent += "<strong>Node ID:</strong> " + nodeId + "<br>";
                infoContent += "<strong>Nom:</strong> " + node.nom + "<br>";
                infoContent += "<strong>Prenom:</strong> " + node.prenoms + "<br>";
                infoContent += "<strong>Né le:</strong> " + node.naissance + "<br>";
                infoContent += "<strong>à:</strong> " + node.villenaiss + '-' + node.paynaiss + "<br>";
                infoContent += "<strong>Profession :</strong> " + node.profession + "<br>";
                if (node.deces) {{
                    infoContent += "<strong>Décédé le :</strong> " + node.deces + "<br>";
                }}
                if (node.inhume) {{
                    infoContent += "<strong>Inhumé le :</strong> " + node.inhume + "<br>";
                }}
                if (node.lieudeces) {{
                    infoContent += "<strong>à :</strong> " + node.lieudeces + "<br>";
                }}
                infoContent += "<img id='node-image' src='" + imagePath + "' alt='Image of " + node.nom + "' style='width:100px; margin-top:10px;'>";
                infoContent += "<hr><strong>Choisir un Document:</strong><br>";
                var files = nodeFileOptions[nodeId];
                if (files && files.length > 0) {{
                    if (files.length === 1) {{
                        infoContent += "<a href='asset/" + nodeId + "/" + files[0] + "' target='_blank'>" + files[0] + "</a>";
                    }} else {{
                        infoContent += "<select id='file-dropdown' style='margin-bottom: 10px;'>";
                        files.forEach(function(file) {{
                            infoContent += "<option value='" + file + "'>" + file + "</option>";
                        }});
                        infoContent += "</select>";
                    }}
                }} else {{
                    infoContent += "<span>No files available</span>";
                }}
                infoBox.innerHTML = infoContent;
                var dropdown = document.getElementById('file-dropdown');
                if (dropdown) {{
                    dropdown.addEventListener('change', function() {{
                        var selectedFile = this.value;
                        if (selectedFile) {{
                            var filePath = 'asset/' + nodeId + '/' + selectedFile;
                            window.open(filePath, '_blank');
                        }}
                    }});
                }}
                var position = network.getPositions([nodeId])[nodeId];
                var canvasPosition = network.canvasToDOM({{x: position.x, y: position.y}});
                infoBox.style.top = (canvasPosition.y + 50) + 'px';
                infoBox.style.left = (canvasPosition.x + 50) + 'px';
                infoBox.style.display = 'block';
            }} else {{
                infoBox.style.display = 'none';
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
        '>Arbre Généalogique Laloë(1.2)</h1>

        <h1 style='
            text-align: center;
            margin-top: 20px;
            font-family: Arial, sans-serif;
            color: #4CAF50;
            font-size: 16px;
        '>(Zoom: Rouler la souris)</h1>
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
