#-------------------------------------------------------------------------------
# Name:        GEN
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#              Usadso dashboard.render4.com para expor na WB
#              Vide video YOUTUBE : https://www.youtube.com/watch?v=H16dZMYmvqo
#              Usar com dados in github/genealog e RENDER DASHBOARD
#
# Author:      ylalo
# Version      1.7
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#import subprocess
import dash
from dash import Dash, html, Input, Output, callback, dash_table,dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import os
import json
import requests
import webbrowser

global fileid
fileid=''

#local_path = 'C:/Users/Public/Downloads'


def getfilegithub(pdir,pfile):     #informar /75/xxxx.xx  devolve o nome do arquvo
    if pdir =='':
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pfile
    else:
        file_url = 'https://raw.githubusercontent.com/kun-dun/genealog/main'+'/'+pdir+'/'+pfile
    response = requests.get(file_url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
    # Chemin local où enregistrer le fichier JPG
       #file_path = local_path + '/'+pfile

    # Enregistrer le fichier JPG localement
      # with open(file_path, 'wb') as file:
      #     file.write(response.content)
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
gen = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
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

    dbc.Row([dbc.Col(html.H1("GÉNÉALOGIE V1.2",className='text-center fs-1'),width=12)]),

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
        dbc.Col(dcc.Dropdown(id='my-dpdn', multi=False, placeholder='Choisir un Document',className='text-center text-primary'),md=3),
        #dbc.Col(md=1),   #coluna em branco para dar espacejamento
        dbc.Col( html.Div(dcc.Input(id='input-on-rech', type='text', placeholder='Rechercher um Nom',className='text-center ')),md=4),
                 html.H1("(Personnes Trouvées en Jaune)",className='text-center fs-6'),
                 html.Div(id='output-container'),

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
        print('x', str(ax))
        print('y',str(ay))
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
#######################ACESSO GITHUB
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
    #print(photo_path)
  # if os.path.exists(photo_path):
    return photo_path
    #return bimage(aphoto)

######################## CALLBACK DROPDOWN
@callback(
    Output('my-dpdn', 'options'),
    Output('my-dpdn', 'value'),
    Input('current-node-data', 'data')
)
def update_dropdown(data):
    #if data == None:
        #return [], None
    filedir ='asset/'+str(fileid)

    person_dir = 'https://api.github.com/repos/kun-dun/genealog/contents/'+filedir
    # Token d'accès personnel
   # access_token = os.getenv('GITLALO')
    #print (access_token)
    # En-têtes de la requête

    response = requests.get(person_dir)
    files=[]
    options = [{'label': 'Pas de Doc!', 'value': ''} ]

# Vérifier si la requête a réussi

    if response.status_code == 200:
       files = response.json()
       if not files==[]:
          options = [{'label': file['name'], 'value': file['name']} for file in files]
    else:
       options = [{'label': 'Erreur Request!'+filedir, 'value': ''} ]
    return options, None

@gen.callback(
    Output('output-container', 'children'),
    Input('my-dpdn', 'value')
)
def update_output(value):
    if not value == None:
        #webbrowser.open(value,new=1,autoraise=True)
        showfile = 'asset/'+fileid
        webbrowser.open_new( getfilegithub(showfile,value))
        return ''

if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')
    gen.run(debug=False)
