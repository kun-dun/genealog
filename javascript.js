<script type="text/javascript">
    // Wait for the network to load
    document.addEventListener("DOMContentLoaded", function() {{
         // Récupérer tous les nœuds

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

        var searchContainer = document.createElement('div');
        searchContainer.style.position = 'absolute';
        searchContainer.style.top = '100px';
        searchContainer.style.left = '10px';
        searchContainer.style.zIndex = '1000';
        searchContainer.innerHTML =
            '<div style="display: flex; align-items: center;">' +
            '    <input type="text" id="node-search-input" placeholder="Rechercher un nom" ' +
            '        style="padding: 5px; width: 200px; margin-right: 10px;">' +
            '    <button id="node-search-button" style="padding: 5px 10px;">Rechercher</button>' +
            '</div>' +
            '<div id="search-results" style="margin-top: 10px; color: #666;"></div>';
        document.body.appendChild(searchContainer);

        // Store original node states
        var originalNodeStates = {{}};

        // Capture original node states when the network is first created
        var allNodes = data.nodes;
        allNodes.forEach(function(node) {{
            originalNodeStates[node.id] = {{
                color: node.color,
                borderWidth: 1,
                borderColor: '#000000'
            }};
        }});



      // Improved search function
        function searchNodes() {{
            var searchTerm = document.getElementById('node-search-input').value.toLowerCase();
            var searchResults = document.getElementById('search-results');
            searchResults.innerHTML = ''; // Clear previous results

            // Filter nodes matching the search term
            var matchingNodes = network.body.data.nodes.get().filter(function(node) {{
                return node.label.toLowerCase().includes(searchTerm);
            }});

            if (matchingNodes.length > 0) {{
                // Update matching nodes to red
                var nodesToUpdate = matchingNodes.map(function(node) {{
                    return {{
                        id: node.id,
                        color: "red", // Bright red
                        borderWidth: 3,
                        borderColor: '#000000'
                    }};
                }});

                // Update the nodes in the network
                network.body.data.nodes.update(nodesToUpdate);
            }}
        }}

        // Reset node styles function
        function resetNodeStyles() {{
            var nodesToReset = Object.keys(originalNodeStates).map(function(nodeId) {{
                var originalState = originalNodeStates[nodeId];
                return {{
                    id: nodeId,
                    color: originalState.color,
                    borderWidth: originalState.borderWidth,
                    borderColor: originalState.borderColor
                }};
            }});

            network.body.data.nodes.update(nodesToReset);
            document.getElementById('node-search-input').value = '';
        }}

        // Add event listener for search button
        document.getElementById('node-search-button').addEventListener('click', searchNodes);

        // Allow searching by pressing Enter key
        document.getElementById('node-search-input').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                searchNodes();
            }}
        }});

        // Store original colors
const originalColors = {{}};
const nodes = {nodes_js};
nodes.forEach(node => {{
    originalColors[node.id] = node.color;
}});

// Function to reset colors
function resetColors() {{
    const allNodes = network.body.data.nodes;
    allNodes.forEach(node => {{
        if (originalColors[node.id]) {{
            node.options.color = originalColors[node.id];
        }}
    }});
    network.redraw();
}}

// Add click event listener to network canvas
document.querySelector('.vis-network').addEventListener('click', function() {{
    resetColors();
}});






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

        // Fonction pour ouvrir Google Maps
        function openGoogleMaps(location) {{
            var query = encodeURIComponent(location);
            window.open('https://www.google.com/maps/search/?api=1&query=' + query, '_blank');
        }}

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

                // Ajouter l'icône de localisation cliquable
                var locationInfo = "";
                if (node.villenaiss) {{
                    var location = node.villenaiss;
                    if (node.paynaiss) {{
                        location += ', ' + node.paynaiss;
                    }}
                    locationInfo = location + " ";
                    locationInfo += "<span style='cursor:pointer; color:blue;' title='Voir sur Google Maps'><i class='fa fa-map-marker' aria-hidden='true'></i>📍</span>";
                }}
                infoContent += "<strong>à:</strong> " + locationInfo + "<br>";

                infoContent += "<strong>Profession :</strong> " + node.profession + "<br>";
                if (node.deces) {{
                    infoContent += "<strong>Décédé le :</strong> " + node.deces + "<br>";
                }}
                if (node.lieudeces) {{
                    infoContent += "<strong>à :</strong> " + node.lieudeces + "<br>";
                }}

                if (node.inhume) {{
                    infoContent += "<strong>Inhumé le :</strong> " + node.inhume + "<br>";
                }}
                if (node.villeinhum) {{
                    infoContent += "<strong>Ville Inhumation :</strong> " + node.villeinhum + "<br>";
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

                // Ajouter l'écouteur d'événements pour l'icône de localisation
                var mapMarker = infoBox.querySelector('.fa-map-marker');
                if (mapMarker) {{
                    mapMarker.addEventListener('click', function() {{
                        var location = node.villenaiss;
                        if (node.paynaiss) {{
                            location += ', ' + node.paynaiss;
                        }}
                        openGoogleMaps(location);
                    }});
                }}

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
                resetColors()


            }}
        }});
    }});
</script>