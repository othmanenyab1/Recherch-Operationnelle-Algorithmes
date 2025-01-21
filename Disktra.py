import networkx as nx
import matplotlib.pyplot as plt
import random


def creer_graphe(n):
    G = nx.Graph()  
    sommets = [f"x{i}" for i in range(n)]  
    

    for sommet in sommets:
        G.add_node(sommet)
    
    for i in range(n - 1):
        distance = random.randint(1, 100)  
        G.add_edge(sommets[i], sommets[i + 1], weight=distance)  

    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]) and not G.has_edge(sommets[i], sommets[j]):
                distance = random.randint(1, 100)
                G.add_edge(sommets[i], sommets[j], weight=distance)
    
    return G


def afficher_chemin_court(G, depart, arrivee):
    try:
    
        chemin = nx.dijkstra_path(G, depart, arrivee, weight='weight')
        distance_totale = nx.dijkstra_path_length(G, depart, arrivee, weight='weight')
        
        print(f"Le plus court chemin entre {depart} et {arrivee} est : {' -> '.join(chemin)}")
        print(f"Distance totale : {distance_totale}")
        
    
        pos = nx.spring_layout(G)
        edges = G.edges(data=True)
        
        edge_colors = ['red' if (u, v) in zip(chemin, chemin[1:]) or (v, u) in zip(chemin, chemin[1:]) else 'black' for u, v, d in edges]
        node_colors = ['green' if node in chemin else 'lightblue' for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in edges})
        plt.show()
        
    except nx.NetworkXNoPath:
        print(f"Aucun chemin entre {depart} et {arrivee}.")


n = int(input("Entrez le nombre de sommets pour le graphe : "))
G = creer_graphe(n)


depart = input("Entrez le sommet de départ : ")
arrivee = input("Entrez le sommet d'arrivée : ")


afficher_chemin_court(G, depart, arrivee)
