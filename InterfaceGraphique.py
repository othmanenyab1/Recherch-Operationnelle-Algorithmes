import tkinter as tk
from tkinter import messagebox, Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import matplotlib.pyplot as plt
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

def welsh_powell_coloriage(G):
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    node_colors = {}
    for node in sorted_nodes:
        neighbor_colors = {node_colors[neighbor] for neighbor in G.neighbors(node) if neighbor in node_colors}
        color = 0
        while color in neighbor_colors:
            color += 1
        node_colors[node] = color
    return node_colors

def afficher_welsh_powell():
    
    try:
        nb_sommets = int(entry_sommets.get())
        if nb_sommets <= 0:
            raise ValueError("Le nombre de sommets doit être positif.")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    G = generer_graphe_aleatoire(nb_sommets)
    colors = welsh_powell_coloriage(G)
    color_list = [colors[node] for node in G.nodes()]
    
    figure = plt.figure()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=color_list, cmap=plt.get_cmap("Set3"), node_size=500)
    plt.title("Welsh-Powell - Coloriage")
    canvas = FigureCanvasTkAgg(figure, master=frame_graphique)
    canvas.draw()
    canvas.get_tk_widget().pack()

def afficher_dijkstra():
    
    try:
        nb_sommets = int(entry_sommets.get())
        depart = entry_depart.get()
        arrivee = entry_arrivee.get()
        if nb_sommets <= 0:
            raise ValueError("Le nombre de sommets doit être positif.")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    G = generer_graphe_aleatoire(nb_sommets)
    try:
        chemin = nx.dijkstra_path(G, depart, arrivee, weight='weight')
        distance_totale = nx.dijkstra_path_length(G, depart, arrivee, weight='weight')

        text_info.insert(tk.END, f"Chemin le plus court : {' -> '.join(chemin)}\n")
        text_info.insert(tk.END, f"Distance totale : {distance_totale}\n")

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
        nx.draw_networkx_edges(G, pos, edgelist=zip(chemin, chemin[1:]), edge_color='red', width=2)
        plt.title("Dijkstra - Chemin le Plus Court")
        figure = plt.figure()
        canvas = FigureCanvasTkAgg(figure, master=frame_graphique)
        canvas.draw()
        canvas.get_tk_widget().pack()
    except nx.NetworkXNoPath:
        messagebox.showerror("Erreur", "Aucun chemin trouvé entre ces deux sommets.")

def afficher_kruskal():
   
    try:
        nb_sommets = int(entry_sommets.get())
        if nb_sommets <= 0:
            raise ValueError("Le nombre de sommets doit être positif.")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return

    G = generer_graphe_aleatoire(nb_sommets)
    mst = nx.minimum_spanning_tree(G, weight='weight')
    cout_mst = sum(data['weight'] for _, _, data in mst.edges(data=True))

    text_info.insert(tk.END, f"Coût du MST : {cout_mst}\n")

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), edge_color='green', width=2)
    plt.title("Kruskal - Arbre de Recouvrement Minimal")
    figure = plt.figure()
    canvas = FigureCanvasTkAgg(figure, master=frame_graphique)
    canvas.draw()
    canvas.get_tk_widget().pack()


root = tk.Tk()
root.title("Algorithme Graphique")
root.geometry("900x700")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Nombre de Sommets :", font=("Arial", 12)).grid(row=0, column=0, padx=5)
entry_sommets = tk.Entry(frame_top, width=10)
entry_sommets.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Départ :", font=("Arial", 12)).grid(row=1, column=0, padx=5)
entry_depart = tk.Entry(frame_top, width=10)
entry_depart.grid(row=1, column=1, padx=5)

tk.Label(frame_top, text="Arrivée :", font=("Arial", 12)).grid(row=2, column=0, padx=5)
entry_arrivee = tk.Entry(frame_top, width=10)
entry_arrivee.grid(row=2, column=1, padx=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Welsh-Powell", command=afficher_welsh_powell, bg="lightcoral", relief=tk.GROOVE).grid(row=0, column=0, padx=10, pady=5)
tk.Button(frame_buttons, text="Dijkstra", command=afficher_dijkstra, bg="lightseagreen", relief=tk.GROOVE).grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame_buttons, text="Kruskal", command=afficher_kruskal, bg="lightgoldenrodyellow", relief=tk.GROOVE).grid(row=0, column=2, padx=10, pady=5)
options = ["Welsh-Powell", "Dijkstra", "Kruskal"]
selected_option = tk.StringVar()
selected_option.set(options[0])

tk.Label(frame_buttons, text="Choisissez un algorithme :", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
option_menu = tk.OptionMenu(frame_buttons, selected_option, *options)
option_menu.grid(row=0, column=1, padx=10, pady=5)

def afficher_selection():
    algo = selected_option.get()
    if algo == "Welsh-Powell":
        afficher_welsh_powell()
    elif algo == "Dijkstra":
        afficher_dijkstra()
    elif algo == "Kruskal":
        afficher_kruskal()

tk.Button(frame_buttons, text="Afficher", command=afficher_selection, bg="lightblue", relief=tk.GROOVE).grid(row=0, column=2, padx=10, pady=5)
frame_graphique = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
frame_graphique.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_info = tk.Frame(root)
frame_info.pack(fill=tk.BOTH, expand=True)

tk.Label(frame_info, text="Informations :", font=("Arial", 14)).pack()
text_info = tk.Text(frame_info, font=("Arial", 12), height=10)
text_info.pack(fill=tk.BOTH, expand=True)

root.mainloop()
