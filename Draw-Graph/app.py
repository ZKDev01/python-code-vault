import networkx as nx
import matplotlib.pyplot as plt

# Crear grafo
G = nx.Graph()

# Añadir vértices
G.add_nodes_from([1, 2, 3, 4, 5])

# Añadir aristas
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)])

# Graficar el grafo
nx.draw(G, with_labels=True)
plt.show()