import requests                       # pour aller chercher l'url
from bs4 import BeautifulSoup         # pour découper le html 
import time                           
import pandas as pd                   # pour classer les données dans un tableau
import csv





# Base_Url
base_url = 'https://www.erafrance.com/catalog/agences.php?page='

# liste contenant tous les liens pour accéder aux coordonées des employés de chaque agence
agences = []




# boucle pour récupérer les 9 liens des 45 pages
for i in range(1, 2):
   
    # Recupère chaque requete de chaque page
    r = requests.get(base_url+str(i))
     
    # Convertit en chaine puis en objet BS
    r = r.text
    content = BeautifulSoup(r, 'lxml')
   
    # Sélectionne tous les liens (voir le site de l'agence) de la classe 'contact_agence_mail'
    all_links = content.findAll('a', {'class':'contact_agence_mail'})
    

    
    
    
    # boucle pour reconstruire chacun des 9 liens pour ainsi obtenir les liens complets (et les ajouter à 'agences')
    for a in all_links:

        # ajout du 'début' au lien incomplet   +   replace pour remplacer les '..' en trop du lien recomposé par du vide      
        lienAgence = 'https://www.erafrance.com'+a['href'].replace('..','').replace('?contact=open','') 
       
        # ajout dans la liste 'agences'
        agences.append(lienAgence)
        




        

        
Noms_et_Prenoms = []
Prenoms = []
Noms = []
Jobs = []
Emails = []
Tels = []








# parcour chaque lien de la liste agences

for agence in agences:

    
    
    # prend le lien donné, extrait le code html de la page (du lien) et le convertit en chaine puis en objet BeautifulSoup
    try :
        r = requests.get(agence)       
        content = BeautifulSoup(r.text, 'lxml')
        
        
        time.sleep(2)

        
        # div contenant tous les blocs (bloc contenant les coordonées d'une personne)
        blocs = content.find('div', {'class':'fiche_interlocuteurs'})
        
        
        
        
        
        # titre de l'agence  -->  prend la chaine de charactère (string) que contient la balise 'title'
#        titre = content.title.string
#        print(titre)        
  

        # nom --> trouve la div 'infos' puis cible le 1er <p> contenant le nom-prénom avec find('p') et récupère que le texte
        for noms in blocs.findAll('div', {'class':'fiche_agent_infos'}):
            Noms_et_Prenoms.append(noms.find('p').getText())           
       
        
        # job  -->  trouve la même div puis cible le <p> (juste en dessous du premier) contenant le poste et récupère le texte
        for noms in blocs.findAll('div', {'class':'fiche_agent_infos'}):
            Jobs.append(noms.p.next_sibling.text)                      # 'next_sibling' pour récupérer la même balise suivante
                
        
        # email --> trouve le 'a' contenant le lien puis ne récupère que celui-ci + supression d'un bout qui était en trop
        for emails in blocs.findAll('a', {'class':'contact_nego_mail'}):
            Emails.append(emails.get('href').replace('mailto:', ''))
               
        
        # tel  -->  trouve la balise 'p' contenant le tel et récupère celui-ci (en chaîne de charactère)
        for tels in blocs.findAll('p', {'class':'contact_nego_tel'}):
            Tels.append(tels.getText())
        
   
        # séparer les Noms des Prénoms et les mettre dans 2 listes différentes
        Prenoms.split()
        

        
    # s'il y a une erreur (pas d'employés par exemple...), il la 'pass', affiche 'erreur' et continu le script
    except :
        pass
      # print('erreur')
    
    

    
    
# parcours chaque élément de la liste Noms_Prenoms, le sépare en deux au 1er espace, et fait une liste de Prenoms et de Noms
for n in Noms_et_Prenoms:
    separation = n.split(' ', 1)
    Prenoms.append(separation[0])
    Noms.append(separation[1])

        


# tableau des données        
tableau = pd.DataFrame(list(zip(Prenoms,Noms,Jobs,Emails,Tels)), columns = ['prénoms','noms','jobs','emails','tels'])
tableau        
