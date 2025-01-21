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
arrivee = input("Entrez le sommet d'arrivée : " 


afficher_chemin_court(G, depart, arrivee)    si  kruskal choissi faire ca  import networkx as nx
import matplotlib.pyplot as plt
import random
import string


def generer_noms_sommets(n):
    alphabet = list(string.ascii_uppercase)
    if n <= 26:
        return alphabet[:n]
    else:
        noms_double_lettre = [a + b for a in alphabet for b in alphabet]
        return alphabet + noms_double_lettre[:n - 26]


def generer_graphe_aleatoire(n):
    G = nx.Graph()
    sommets = generer_noms_sommets(n)
    for i in range(n):
        for j in range(i + 1, n):
            
            poids = random.randint(1, 100)
            G.add_edge(sommets[i], sommets[j], weight=poids)
    return G


def calculer_mst_kruskal(G):
    mst = nx.Graph()  
    arretes_tries = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    
    
    parent = {i: i for i in G.nodes()}
    
    def trouver_parent(noeud):
        if parent[noeud] == noeud:
            return noeud
        return trouver_parent(parent[noeud])
    
    def fusionner_ensembles(u, v):
        racine_u = trouver_parent(u)
        racine_v = trouver_parent(v)
        parent[racine_u] = racine_v
    
    cout_mst = 0
    for u, v, data in arretes_tries:
        if trouver_parent(u) != trouver_parent(v):  
            mst.add_edge(u, v, weight=data['weight'])
            cout_mst += data['weight']
            fusionner_ensembles(u, v)
    
    return mst, cout_mst


def dessiner_graphe_et_mst(G, mst):
    pos = nx.spring_layout(G)  
    etiquettes_arretes = nx.get_edge_attributes(G, 'weight')
    

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquettes_arretes)
    

    arretes_mst = list(mst.edges())
    nx.draw_networkx_edges(G, pos, edgelist=arretes_mst, edge_color='r', width=2)
    
    plt.show()


def programme_principal():
    
    n = int(input("Entrez le nombre de sommets: "))
    G = generer_graphe_aleatoire(n)
    
    
    mst, cout_mst = calculer_mst_kruskal(G)
    
    
    print(f"Le coût : {cout_mst}")
    
    
    dessiner_graphe_et_mst(G, mst)


if __name__ == "__main__":
    programme_principal()

