#-------------------------------------------------------------------------------
# Name:        GEN
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#              Usadso dashboard.render4.com para expor na WB
#              Vide video YOUTUBE : https://www.youtube.com/watch?v=H16dZMYmvqo
#              Usar com dados in github/genealog e RENDER DASHBOARD
#
# Author:      ylalo
# Version      1.9   (sem GITHUB)
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import dash
from dash import Dash, html, Input, Output, callback, dash_table,dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import os
import json
import requests
import webbrowser
from docx2txt import process  # For extracting text from DOCX files
#from github import Github
#from dotenv import load_dotenv

global fileid
fileid=''
#adir = os.getcwd()
#local_path = 'C:/Users/Public/Downloads'


def download_github_file(pdir,pfile):
    # Construct the raw GitHub URL
    raw_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pdir+'/'+pfile

    # Send a GET request to fetch the file content
    response = requests.get(raw_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the file locally
        with open(pfile, 'wb') as file:
            file.write(response.content)
        #print(f"File downloaded successfully and saved to {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

def getfilegithub(pdir,pfile):     #informar /75/xxxx.xx  devolve o nome do arquvo
    if pdir =='':
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pfile
    else:
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pdir+'/'+pfile
    response = requests.get(file_url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
       with open(pfile, 'wb') as file:
            file.write(response.content)
       return file_url #file_path
    else:
        return ''

def gettree(pdir,pfile):     #informar /75/xxxx.xx  devolve o conteudo do arquivo
    if pdir =='':
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pfile
    else:
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pdir+'/'+pfile
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text  # Retourne le contenu du fichier en tant que texte
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")
        return None



aNodes = []
adir = os.getcwd()
afile =gettree('','js.txt')
# Convertir le contenu en une structure Python
if afile:
    try:
        aNodes = json.loads(afile)  # Convertit le JSON en liste/dictionnaire Python
    except json.JSONDecodeError as e:
        print("Erreur de décodage JSON :", e)
else:
    print("Impossible de charger le fichier.")

############################################################################
gen = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='asset',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = gen.server

##############################################################################
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    },
    'cab': {
        "font-size": "6",
        'line-height': '2'
    }
}

my_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    {
        'selector': '.pink',
        'style': {
            'background-color': 'pink',
            'line-color': 'pink',
            "font-size": "6",
            "text-wrap": "wrap",
            'line-height': '2',
            "text-max-width": 40,
            'text-halign': 'center',
        }
    },
    {
        'selector': '.yellow',
        'style': {
            'background-color': 'yellow',
            'line-color': 'yellow',
            "font-size": "6",
            "text-wrap": "wrap",
            'line-height': '2',
            "text-max-width": 40
        }
    },
    {
        'selector': '.green',
        'style': {
            'background-color': 'green',
            'line-color': 'green',
            "font-size": "6",
            "text-wrap": "wrap",
            "text-max-width": 40
        }
    }
]


aphoto =  getfilegithub('photos','homme.jpg')


gen.layout = dbc.Container([
        dbc.Row([
        dbc.Col([ html.Img(id='imagem-dinamica', src=aphoto, style={
            'position': 'absolute',
            'top': '10px',
            'left': '10px'})])
           ]),

    dbc.Row([dbc.Col(html.H1("GÉNÉALOGIE V1.8",className='text-center fs-1'),width=12)]),

    dbc.Row([dbc.Col(html.H1("(Zoom :Rouler la souris)",className='text-center fs-6'),width=12)]),   # fs-6 = font size : maior o numero, menor a font
    dbc.Row(dbc.Col(html.H1("Cliquer sur la Personne pour voir les Détails",className='text-center fs-6'),width=12) ),
    dbc.Row([html.H1()]),  #linhas em branco
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),


    dbc.Row([
        dbc.Col(md=1),
        dbc.Col(dcc.Dropdown(id='my-dpdn',options=[], multi=False, placeholder='Choisir un Document',className='text-center text-primary'),md=3),
        #dbc.Col(md=1),   #coluna em branco para dar espacejamento
        dbc.Col(html.Div(id='output-container'), md=7),  # Container for the generated link
        dbc.Col( html.Div(dcc.Input(id='input-on-rech', type='text', placeholder='Rechercher um Nom',className='text-center ')),md=8),
                 html.H1("(Personnes Trouvées en Jaune)",className='text-center fs-6'),

        #dcc.Download(id="download-file"),  # Add the dcc.Download component
        # Content display
        html.Div(id='file-content'),
        dcc.Store(id='current-node-data')
            ]),

    dbc.Row([html.H1()]),   #Linha em branco.......
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),


    dbc.Row([
        dbc.Col([cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        minZoom=0.5,
        maxZoom=6,
        zoom=6,
        pan={'x': 200, 'y': 200},


        zoomingEnabled=True,

        layout={'name': 'preset'},
        style={'width': '100%', 'height': '800px'},
        stylesheet=my_stylesheet,
        elements=aNodes),# Componente para exibir os dados do nó clicado
        html.Div(id='cytoscape-tapNodeData-json')],width=12),
        dbc.Col([html.Div(id='container-button-func', children='resultat')])
            ]),  ###fim cytoscape
        # Boîte pour afficher les informations du nœud
        html.Div(id='node-info-box', style={'position': 'absolute', 'display': 'none'})
],fluid= True)  #fim container



############# CALLBACK SEARCH

@callback(
    Output('cytoscape-event-callbacks-1', 'stylesheet'),
    Input('input-on-rech', 'value'),
    State('cytoscape-event-callbacks-1', 'stylesheet')
)
def update_search(search_text, stylesheet):
    if not search_text:
        return my_stylesheet

    stylesheet = list(my_stylesheet)
    stylesheet.append({
        'selector': f'node[label *= "{search_text}"]',
        'style': {
            'background-color': 'yellow',
        }
    })
    return stylesheet


#######################################
@gen.callback(
    Output('cytoscape-event-callbacks-1', 'viewport'),
    Input('cytoscape-event-callbacks-1', 'tapNodeData')
)
def center_on_node(node_data):
    if not node_data:
        return None

    # Center the view on the tapped node with some zoom
    return {
        'zoom': 2,
        'pan': {'x': 0, 'y': 0},
        'target': f'#{node_data["id"]}'
    }


######################## CALLBACK INFO PESSOA
# Callback pour afficher les informations du nœud sélectionné
@callback(
    Output('node-info-box', 'children'),  # Output: box content
    Output('node-info-box', 'style'),     # Output: box style
    Input('cytoscape-event-callbacks-1', 'tapNodeData')  # Input: clicked node data
)
def display_node_info(node_data):
    if node_data:
        # Construct a more robust info display


        adeces =f"Décédé le  : {node_data.get('deces', 'N/A')} à {node_data.get('lieudeces', 'N/A')}"
        ainhume =f"Inhumé le  : {node_data.get('inhume', 'N/A')} "

        content = html.Div([
            html.H4(f"Informations sur la Personne", style={'marginBottom': '5px'}),


            html.P(f"ID : {node_data.get('id', 'N/A')}"),
            html.P(f"Nom : {node_data.get('label', 'N/A')}"),
            html.P(f"Sexe : {node_data.get('sexe', 'N/A')}"),
            html.P(f"Né le   {node_data.get('naissance', 'N/A')} à {node_data.get('villenaiss', 'N/A')} - {node_data.get('paysnaiss', 'N/A')}"),
            html.P(f"Baptise le {node_data.get('baptise', 'N/A')}"),
            html.P(f"Marié le {node_data.get('marie', 'N/A')}"),
            html.P(f"Profession {node_data.get('profession', 'N/A')}"),
            html.P(adeces),
            html.P(ainhume)],

            style={
            'backgroundColor': '#f9f9f9',
            'padding': '5px',
            'borderRadius': '5px'})

        # Update the global fileid
        global fileid
        fileid = str(node_data.get('personneid', ''))
        ax = int(node_data["x"])
        ay = int(node_data["y"])
        #('x', str(ax))
        #print('y',str(ay))
        # Style for positioning the info box
        style = {
            'position': 'absolute',
            #'top': str(ay),  # Ajustez la position verticale
             # 'left': str(ax),  # Ajustez la position horizontale
            'top': '10px',  # Fixed position near the top
            'left': '120px',  # Fixed position on the right
            'width': '340px',
            'border': '1px solid #ddd',
            'backgroundColor': 'white',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            "font-size": "4",
            'line-height': '0.3',  # Réduire l'interligne ici
            'zIndex': 1000,
            'display': 'block'
        }
        return content, style

    # If no node is selected, hide the box
    return None, {'display': 'none'}
####################### ACESSO GITHUB
@gen.callback(
    Output('test-output', 'children'),
    Input('test-button', 'n_clicks')
)
def test_github_connection(n_clicks):
    if n_clicks:
        try:
            response = requests.get('https://api.github.com/repos/kun-dun/genealog/contents/asset', headers=headers)
            return f"Status Code: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Click to test GitHub connection"

#######################  CALLBACK PHOTO
@gen.callback(
    Output('current-node-data', 'data'),
    [Input('cytoscape-event-callbacks-1', 'tapNodeData')]
)
def update_stored_node_data(data):
    return data

@gen.callback(
    Output('imagem-dinamica', 'src'),
    [Input('current-node-data', 'data')]
)
def update_image(data):
   # if data is None:
       # return bimage(aphoto)
    apath ='photos'
    aimg = str(fileid)+'.jpg'
    photo_path = getfilegithub(apath,aimg ) #dirc + '//repo//photos//'+str(data['personneid'])+'.jpg' #   f"photos/{data['personneid']}.jpg"
   # print(photo_path)

    return photo_path
    #return bimage(aphoto)

######################## CALLBACK DROPDOWN
# Callback to populate the dropdown
@callback(
    Output("my-dpdn", "options"),
    Output("my-dpdn", "value"),
    Input("current-node-data", "data")
)
def update_dropdown(data):
    if data is None:
        return [], None
    filedir = 'asset/'+str(fileid)
    person_dir = f"https://api.github.com/repos/kun-dun/genealog/contents/{filedir}"
    response = requests.get(person_dir)
    if response.status_code == 200:
        files = response.json()
        if files:
            options = [{"label": file["name"], "value": file["name"]} for file in files]
            return options, None
    return [{"label": "Pas de Doc!", "value": ""}], None
############################################################ POPULA DROPDOWN


@gen.callback(
    Output('output-container', 'children'),
    Input('my-dpdn', 'value')
)

def update_output(value):
    if value:
        showfile = 'asset/'+str(fileid)
        fileurl = getfilegithub(showfile, value)
        if fileurl:
            _, ext = os.path.splitext(value.lower())
            if ext == ".pdf":
                # Embed the PDF in an iframe
                return html.Iframe(
                    src=fileurl,
                    style={'width': '100%', 'height': '600px', 'border': 'none'}
                )
            elif ext == ".docx":
                # Extract text from the DOCX file and display it
                response = requests.get(fileurl)
                if response.status_code == 200:
                    try:
                        # Save the DOCX file locally temporarily
                        temp_file = "temp.docx"
                        with open(temp_file, "wb") as f:
                            f.write(response.content)
                        # Extract text from the DOCX file
                        docx_text = process(temp_file)
                        # Remove the temporary file
                        os.remove(temp_file)
                        return html.Pre(docx_text, style={'whiteSpace': 'pre-wrap'})
                    except Exception as e:
                        return html.Div(f"Error processing DOCX file: {str(e)}", style={'color': 'red'})
                else:
                    return html.Div("Error fetching DOCX file.", style={'color': 'red'})
            elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
                # Display the image
                return html.Img(src=fileurl, style={'width': '100%', 'height': 'auto'})
            elif ext == ".txt":
                # Fetch and display the text content
                response = requests.get(fileurl)
                if response.status_code == 200:
                    return html.Pre(response.text, style={'whiteSpace': 'pre-wrap'})
                else:
                    return html.Div("Error fetching text file.", style={'color': 'red'})
            else:
                # For other file types, provide a download link
                return html.Div([
                    html.P("File type not supported for preview. Please download it:"),
                    html.A("Download File", href=fileurl, target="_blank", style={'color': 'blue', 'textDecoration': 'underline'})
                ])
        else:
            return html.Div("File not found or invalid URL.", style={'color': 'red'})
    return ""


if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')
    gen.run(debug=False)
