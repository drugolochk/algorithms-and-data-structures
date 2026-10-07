# -*- coding: utf-8 -*-
from pathlib import Path
import heapq
import matplotlib.pyplot as plt
import networkx as nx

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path.name)


def draw_directed(name, edges, pos, title, highlight=None):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=950, node_color="#c6e6c6",
                           edgecolors="#2d5a2d", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13, font_weight="bold")
    hl = set(highlight or [])
    normal = [(u, v) for u, v, _ in edges if (u, v) not in hl]
    extra = [(u, v) for u, v, _ in edges if (u, v) in hl]
    if normal:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=normal, width=1.6,
                               edge_color="#333333", arrows=True, arrowstyle="-|>",
                               arrowsize=18, connectionstyle="arc3,rad=0.04",
                               min_source_margin=15, min_target_margin=15)
    if extra:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=extra, width=2.8,
                               edge_color="#c0392b", arrows=True, arrowstyle="-|>",
                               arrowsize=18, connectionstyle="arc3,rad=0.04",
                               min_source_margin=15, min_target_margin=15)
    labels = {(u, v): w for u, v, w in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=10)
    ax.set_title(title, fontsize=13, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


def draw_undirected(name, edges, pos, title, highlight=None):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=950, node_color="#f7d774",
                           edgecolors="#7a5b00", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13, font_weight="bold")
    hl = {frozenset(e) for e in (highlight or [])}
    widths, colors = [], []
    for u, v in G.edges():
        if frozenset((u, v)) in hl:
            widths.append(2.8)
            colors.append("#c0392b")
        else:
            widths.append(1.6)
            colors.append("#333333")
    nx.draw_networkx_edges(G, pos, ax=ax, width=widths, edge_color=colors)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=10)
    ax.set_title(title, fontsize=13, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


def dijkstra(edges, source, directed=True):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_weighted_edges_from(edges)
    dist = {v: float("inf") for v in G.nodes()}
    prev = {v: None for v in G.nodes()}
    dist[source] = 0
    pq = [(0, source)]
    visited = []
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.append(u)
        for v, data in G[u].items():
            nd = d + data["weight"]
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev, visited


def path_of(prev, t):
    if prev.get(t) is None and t not in prev:
        return []
    chain = [t]
    while prev[chain[-1]] is not None:
        chain.append(prev[chain[-1]])
    chain.reverse()
    return chain


# --- sam 1: орграф 1 -> 6 ---
e1 = [
    (1, 2, 1), (1, 3, 2), (1, 4, 7),
    (2, 3, 4),
    (4, 3, 13), (4, 5, 1),
    (5, 3, 12), (5, 6, 5),
    (6, 3, 2),
]
pos1 = {1: (0.0, 1.1), 2: (1.4, 2.2), 3: (3.2, 2.2),
        4: (1.4, 0.0), 5: (3.2, 0.0), 6: (4.8, 1.1)}
d1, p1, _ = dijkstra(e1, 1, True)
path1 = path_of(p1, 6)
print("sam1", d1[6], path1)
draw_directed("sam_1_graf.png", e1, pos1, "Задание 1. Орграф. Кратчайший путь 1 -> 6")
draw_directed("sam_1_path.png", e1, pos1,
              "Задание 1. Кратчайший путь выделен красным",
              highlight=list(zip(path1, path1[1:])))

# --- sam 2: на рисунке без стрелок, считаем неориентированным ---
e2 = [
    (1, 2, 3), (1, 4, 7), (1, 5, 8),
    (2, 3, 1), (2, 4, 4),
    (3, 4, 2), (3, 6, 3),
    (4, 5, 3), (4, 6, 4),
    (5, 6, 9),
]
pos2 = {1: (0.0, 1.1), 2: (1.6, 2.2), 3: (3.4, 2.2),
        4: (2.2, 1.0), 5: (1.2, 0.0), 6: (3.8, 0.4)}
d2, p2, _ = dijkstra(e2, 1, False)
path2 = path_of(p2, 6)
print("sam2", d2[6], path2)
draw_undirected("sam_2_graf.png", e2, pos2, "Задание 2. Граф. Кратчайший путь 1 - 6")
draw_undirected("sam_2_path.png", e2, pos2,
                "Задание 2. Кратчайший путь выделен красным",
                highlight=list(zip(path2, path2[1:])))

# --- sam 3 ---
e3 = [
    ("S", "A", 5), ("S", "B", 10),
    ("A", "C", 3), ("A", "T", 12),
    ("B", "C", 2),
    ("C", "T", 4),
]
pos3 = {"S": (0.0, 1.0), "A": (1.6, 1.8), "B": (1.6, 0.2),
        "C": (3.2, 1.0), "T": (4.8, 1.0)}
d3, p3, _ = dijkstra(e3, "S", True)
path3 = path_of(p3, "T")
print("sam3", d3["T"], path3)
draw_directed("sam_3_graf.png", e3, pos3, "Задание 3. Маршрут склада S -> торговый центр T")
draw_directed("sam_3_path.png", e3, pos3,
              "Задание 3. Кратчайший маршрут выделен красным",
              highlight=list(zip(path3, path3[1:])))

# --- hard 1 ---
e_h1 = [
    ("S", "A", 10), ("S", "B", 15),
    ("A", "C", 12), ("A", "D", 15),
    ("B", "E", 10),
    ("C", "F", 5),
    ("D", "F", 10), ("D", "G", 20),
    ("E", "G", 5),
    ("F", "G", 10),
]
pos_h1 = {
    "S": (0.0, 1.5),
    "A": (1.6, 2.6), "B": (1.6, 0.4),
    "C": (3.2, 2.6), "D": (3.2, 1.5), "E": (3.2, 0.4),
    "F": (4.8, 2.0), "G": (6.4, 1.5),
}
d_h1, p_h1, _ = dijkstra(e_h1, "S", True)
print("hard1", {k: d_h1[k] for k in "SABCDEFG"})
for v in "ABCDEFG":
    print(" ", v, path_of(p_h1, v), d_h1[v])
draw_directed("hard_1_graf.png", e_h1, pos_h1,
              "Повышенная 1. Склады. Кратчайшие пути от S")

# --- hard 2 ---
e_h2 = [
    (1, 2, 4), (1, 3, 3), (1, 4, 7),
    (2, 4, 9), (2, 5, 4),
    (3, 6, 3), (3, 7, 4),
    (4, 7, 11),
    (5, 6, 1), (5, 8, 4),
    (6, 8, 8),
    (7, 8, 5),
]
pos_h2 = {
    1: (0.0, 1.0), 2: (1.4, 2.2), 3: (2.2, 1.2), 4: (1.6, 0.0),
    5: (3.2, 2.4), 6: (3.4, 1.2), 7: (4.4, 0.2), 8: (5.2, 1.8),
}
d_h2, p_h2, _ = dijkstra(e_h2, 1, False)
path_h2 = path_of(p_h2, 8)
print("hard2", d_h2[8], path_h2)
draw_undirected("hard_2_graf.png", e_h2, pos_h2,
                "Повышенная 2. Кратчайший путь 1 - 8")
draw_undirected("hard_2_path.png", e_h2, pos_h2,
                "Повышенная 2. Кратчайший путь выделен красным",
                highlight=list(zip(path_h2, path_h2[1:])))

print("done")
