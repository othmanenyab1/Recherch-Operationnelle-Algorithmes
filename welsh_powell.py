import networkx as nx  
import random  
import matplotlib.pyplot as plt  

def generer_graphe_aleatoire():
   
    
    nb_sommets = int(input("Entrez le nombre de sommets pour le graphe : "))  

    G = nx.Graph()  # Crée un graphe vide avec NetworkX
    
    G.add_nodes_from(range(nb_sommets))  
    
    
    for i in range(nb_sommets):
        for j in range(i+1, nb_sommets):
            if random.random() > 0.5:  # Avec une probabilité de 50%, ajoute une arête entre deux sommets
                G.add_edge(i, j)

    return G  # Retourne le graphe généré

def welsh_powell_coloriage(G):
    
    
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
   
    
    node_colors = {}  # Dictionnaire pour stocker la couleur de chaque sommet
    current_color = 0  # Variable pour suivre la couleur courante


    for node in sorted_nodes:
       
        neighbor_colors = {node_colors[neighbor] for neighbor in G.neighbors(node) if neighbor in node_colors}
        
        
        color = 0  # Commence à chercher une couleur
        while color in neighbor_colors:
            color += 1  

        node_colors[node] = color 

    return node_colors  


graphe = generer_graphe_aleatoire() 


color_map = welsh_powell_coloriage(graphe)  


print(f"Nombre de sommets : {graphe.number_of_nodes()}") 
print(f"Nombre d'arêtes : {graphe.number_of_edges()}")  
print("Liste des arêtes :")
for edge in graphe.edges():  
    print(edge)


colors = [color_map[node] for node in graphe.nodes()]  

cmap = plt.get_cmap('Set3')  
nx.draw(graphe, with_labels=True, node_color=colors, cmap=cmap, edge_color='gray', node_size=700, font_size=10)


plt.show()  
