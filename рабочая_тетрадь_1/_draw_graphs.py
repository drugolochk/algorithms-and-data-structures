# -*- coding: utf-8 -*-
from pathlib import Path
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path.name)


def draw_undirected(name, edges, pos, title, weighted=False, highlight=None):
    G = nx.Graph()
    if weighted:
        G.add_weighted_edges_from(edges)
    else:
        G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(8, 6.2))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="#c6e6c6", edgecolors="#2d5a2d", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13, font_weight="bold")
    edge_color = []
    width = []
    for e in G.edges():
        a, b = e
        key = frozenset((a, b))
        if highlight and key in highlight:
            edge_color.append("#c0392b")
            width.append(2.8)
        else:
            edge_color.append("#333333")
            width.append(1.6)
    nx.draw_networkx_edges(G, pos, ax=ax, width=width, edge_color=edge_color)
    if weighted:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=11)
    ax.set_title(title, fontsize=13, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


def draw_directed(name, edges, pos, title, weighted=False):
    G = nx.DiGraph()
    if weighted:
        G.add_weighted_edges_from(edges)
    else:
        G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(8.4, 6.6))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="#b8d4f0", edgecolors="#1f4e79", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(
        G, pos, ax=ax, width=1.6, edge_color="#333333", arrows=True,
        arrowstyle="-|>", arrowsize=18, connectionstyle="arc3,rad=0.05",
        min_source_margin=14, min_target_margin=14,
    )
    if weighted:
        labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=10, label_pos=0.45)
    ax.set_title(title, fontsize=13, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


# --- sam 1 ---
draw_directed(
    "sam_1_graf.png",
    [(1, 2), (2, 3), (2, 4), (3, 5), (4, 5), (5, 1)],
    {1: (1.6, 1.6), 2: (0.6, 2.2), 3: (2.4, 0.3), 4: (0.0, 1.6), 5: (0.7, 0.2)},
    "Задание 1. Ориентированный граф G",
)

# --- sam 2 ---
draw_undirected(
    "sam_2_graf.png",
    [("X", "Y", 2), ("X", "Z", 4), ("Y", "Z", 1), ("Y", "W", 3), ("Z", "W", 5)],
    {"X": (0.0, 1.6), "Y": (1.8, 1.6), "Z": (0.0, 0.2), "W": (1.8, 0.2)},
    "Задание 2. Неориентированный взвешенный граф G",
    weighted=True,
)

# --- sam 3 ---
pos3 = {i: (math.cos(math.pi / 2 + 2 * math.pi * (i - 1) / 6),
            math.sin(math.pi / 2 + 2 * math.pi * (i - 1) / 6)) for i in range(1, 7)}
draw_undirected(
    "sam_3_graf.png",
    [(1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)],
    pos3,
    "Задание 3. Неориентированный граф G",
)

# --- sam 4 ---
pos4 = {
    1: (0.0, 1.2), 2: (2.0, 2.0), 3: (2.0, 0.2),
    4: (1.1, 1.2), 5: (0.3, 2.1), 6: (0.3, 0.3), 7: (2.6, 1.2),
}
draw_undirected(
    "sam_4_graf.png",
    [(1, 4), (1, 5), (1, 6), (1, 7), (2, 4), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7), (4, 7)],
    pos4,
    "Задание 4. Неориентированный граф G",
)

# --- sam 5 ---
pos5 = {
    1: (0.0, 1.6), 2: (0.0, 0.5), 3: (1.2, 2.0), 4: (2.2, 2.0),
    5: (3.2, 2.0), 6: (1.2, 0.8), 7: (2.4, 0.0), 8: (2.4, 1.1),
}
draw_undirected(
    "sam_5_graf.png",
    [(1, 6), (1, 8), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 8), (4, 5), (4, 6), (4, 8), (7, 8)],
    pos5,
    "Задание 5. Неориентированный граф G",
)

# --- sam 6 ---
pos6 = {
    "A": (0.0, 1.0), "B": (1.2, 1.8), "C": (1.2, 0.2),
    "D": (2.4, 1.8), "E": (2.4, 0.2), "F": (3.6, 1.0),
}
draw_directed(
    "sam_6_graf.png",
    [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E"), ("D", "F"), ("E", "F")],
    pos6,
    "Задание 6. Ориентированный граф G",
)

# --- sam 7 ---
pos7 = {
    1: (0.0, 1.0), 2: (1.2, 1.8), 3: (1.2, 0.2),
    4: (2.4, 1.8), 5: (2.4, 0.6), 6: (3.6, 1.4), 7: (4.6, 0.6),
}
draw_undirected(
    "sam_7_graf.png",
    [(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 6), (5, 6), (5, 7), (6, 7)],
    pos7,
    "Задание 7. Неориентированный граф G",
)

# --- hard 1 ---
pos_h1 = {
    1: (3.2, 3.4), 2: (2.2, 3.2), 3: (2.6, 2.2), 4: (4.4, 3.0),
    5: (1.8, 1.6), 6: (0.8, 2.4), 7: (3.6, 1.2), 8: (0.0, 1.4),
    9: (1.4, 0.9), 10: (1.6, 0.0),
}
draw_directed(
    "hard_1_graf.png",
    [
        (1, 2, 4), (1, 3, 2), (2, 4, 7), (2, 5, 1), (2, 6, 3),
        (3, 6, 3), (3, 7, 6), (4, 7, 5), (5, 7, 8), (5, 10, 7),
        (6, 8, 6), (6, 10, 5), (7, 9, 2), (8, 9, 4), (9, 10, 9),
    ],
    pos_h1,
    "Повышенная 1. Ориентированный взвешенный граф G",
    weighted=True,
)

# --- hard 2 ---
pos_h2 = {i: (math.cos(math.pi / 2 + 2 * math.pi * (i - 1) / 9),
              math.sin(math.pi / 2 + 2 * math.pi * (i - 1) / 9)) for i in range(1, 10)}
draw_undirected(
    "hard_2_graf.png",
    [(1, 2), (1, 3), (1, 5), (1, 9), (2, 3), (2, 6), (2, 8),
     (3, 4), (3, 9), (4, 5), (4, 7), (4, 8), (5, 6), (5, 7),
     (6, 8), (6, 9), (8, 9)],
    pos_h2,
    "Повышенная 2. Неориентированный граф G",
)

# --- hard 3 original ---
pos_h3 = {
    "A": (0.0, 2.0), "B": (1.5, 3.0), "C": (1.5, 1.6), "D": (1.5, 0.4),
    "E": (3.2, 3.0), "F": (3.2, 1.6), "G": (3.2, 0.4), "H": (4.7, 1.6),
}
draw_undirected(
    "hard_3_graf.png",
    [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "E"), ("C", "D"),
     ("C", "F"), ("D", "G"), ("E", "F"), ("E", "H"), ("F", "G"), ("F", "H"), ("G", "H")],
    pos_h3,
    "Повышенная 3. Исходный граф G (не эйлеров)",
)

draw_undirected(
    "hard_3_euler_graf.png",
    [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "E"), ("C", "D"),
     ("C", "F"), ("D", "G"), ("E", "F"), ("E", "H"), ("F", "G"), ("F", "H"), ("G", "H"),
     ("A", "E"), ("B", "G"), ("D", "H")],
    pos_h3,
    "Повышенная 3. Эйлеров граф (красные — добавленные рёбра)",
    highlight={frozenset(("A", "E")), frozenset(("B", "G")), frozenset(("D", "H"))},
)

print("done")
