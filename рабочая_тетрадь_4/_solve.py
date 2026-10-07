# -*- coding: utf-8 -*-
from pathlib import Path
import random
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def draw_undirected(name, edges, pos, title, highlight=None, signed=False, colors=None):
    G = nx.Graph()
    if signed:
        for u, v, s in edges:
            G.add_edge(u, v, sign=s)
    else:
        weighted = len(edges[0]) == 3 and isinstance(edges[0][2], (int, float))
        if weighted:
            G.add_weighted_edges_from(edges)
        else:
            G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    node_color = "#c6e6c6"
    if colors:
        palette = {1: "#f6c6c6", 2: "#c6d6f6", 3: "#f6e6a0", 4: "#d4f6c6"}
        node_color = [palette[colors[n]] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=950, node_color=node_color,
                           edgecolors="#333", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13, font_weight="bold")
    hl = {frozenset(e) for e in (highlight or [])}
    widths, ecolors, styles = [], [], []
    for u, v in G.edges():
        if signed:
            s = G[u][v]["sign"]
            ecolors.append("#2e7d32" if s == "+" else "#c0392b")
            widths.append(2.2)
            styles.append("solid")
        elif frozenset((u, v)) in hl:
            ecolors.append("#c0392b")
            widths.append(2.8)
            styles.append("solid")
        else:
            ecolors.append("#555")
            widths.append(1.5)
            styles.append("solid")
    nx.draw_networkx_edges(G, pos, ax=ax, width=widths, edge_color=ecolors)
    if signed:
        labels = {(u, v): G[u][v]["sign"] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=12)
    elif G.edges() and "weight" in next(iter(G.edges(data=True)))[2]:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=10)
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


# ---- task 1 MST ----
e1 = [
    ("A", "B", 4), ("A", "C", 7), ("A", "D", 3),
    ("B", "C", 5), ("B", "D", 2), ("B", "E", 6),
    ("C", "D", 5), ("D", "E", 2), ("D", "F", 1), ("E", "F", 9),
]
pos1 = {"A": (0.2, 2.0), "B": (1.6, 2.6), "C": (1.6, 1.2),
        "D": (3.0, 2.0), "E": (4.2, 2.8), "F": (4.4, 1.2)}
mst = [("D", "F"), ("B", "D"), ("D", "E"), ("A", "D"), ("B", "C")]
draw_undirected("sam_1_graf.png", e1, pos1, "Задание 1. Взвешенный граф")
draw_undirected("sam_1_mst.png", e1, pos1, "Задание 1. MST (красные рёбра), вес 13", highlight=mst)

# ---- task 2 independent set ----
e2 = [
    ("A", "B"), ("A", "C"), ("A", "D"),
    ("B", "D"), ("B", "E"),
    ("C", "D"), ("C", "E"),
    ("D", "E"),
    ("E", "F"),
]
pos2 = {"A": (0.0, 1.6), "B": (1.4, 2.6), "C": (1.4, 0.6),
        "D": (2.6, 1.6), "E": (4.0, 1.6), "F": (5.4, 1.6)}
draw_undirected("sam_2_graf.png", e2, pos2, "Задание 2. Граф для независимого множества")
draw_undirected("sam_2_ind.png", e2, pos2, "Задание 2. Независимое множество {B, C, F}",
                colors={"A": 2, "B": 1, "C": 1, "D": 2, "E": 2, "F": 1})

# ---- task 3 coloring ----
wp = {"D": 1, "E": 2, "A": 2, "B": 3, "C": 3, "F": 1}
draw_undirected("sam_3_color.png", e2, pos2,
                "Задание 3. Раскраска Вельша–Пауэлла, χ(G)=3",
                colors=wp)

# ---- task 4 signed ----
e4 = [
    (1, 2, "+"), (1, 3, "-"), (2, 3, "-"),
    (2, 4, "+"), (3, 4, "-"), (4, 5, "-"), (1, 5, "-"),
]
pos4 = {1: (0.0, 1.5), 2: (1.5, 2.6), 3: (1.5, 0.4), 4: (3.0, 1.5), 5: (1.5, 1.5)}
draw_undirected("sam_4_graf.png", e4, pos4,
                "Задание 4. Знаковый граф (зелёный +, красный −)", signed=True)
draw_undirected("sam_4_cycle.png", e4, pos4,
                "Задание 4. Коалиции: {1,2,4} и {3,5}",
                signed=True, colors={1: 1, 2: 1, 4: 1, 3: 2, 5: 2})

# ---- task 5 Watts-Strogatz ----
import math
ring = [(i, i % 8 + 1) for i in range(1, 9)]
pos8 = {i: (1.6 * math.cos(math.pi / 2 + 2 * math.pi * (i - 1) / 8),
            1.6 * math.sin(math.pi / 2 + 2 * math.pi * (i - 1) / 8))
        for i in range(1, 9)}
G_ring = nx.Graph(); G_ring.add_edges_from(ring)
print("ring diameter", nx.diameter(G_ring))
draw_undirected("sam_5_ring.png", ring, pos8, "Задание 5. Кольцо N=8, k=2. Диаметр = 4")
# для учебного эффекта малого мира оставляем кольцо и добавляем две дальние хорды
rewired = ring + [(1, 5), (3, 7)]
G_rw = nx.Graph(); G_rw.add_edges_from(rewired)
print("rewired diameter", nx.diameter(G_rw))
draw_undirected("sam_5_rewire.png", rewired, pos8,
                "Задание 5. Дальние связи 1-5 и 3-7. Диаметр = 3",
                highlight=[(1, 5), (3, 7)])

# ---- hard 2 interference ----
e_h2 = [
    ("x1", "x2"), ("x1", "x3"), ("x1", "x4"),
    ("x2", "x3"), ("x2", "x5"),
    ("x3", "x6"),
    ("x4", "x5"), ("x4", "x6"),
    ("x5", "x6"),
]
pos_h2 = {"x1": (0.0, 1.6), "x2": (1.5, 2.8), "x3": (1.5, 0.4),
          "x4": (3.2, 1.6), "x5": (4.6, 2.8), "x6": (4.6, 0.4)}
reg = {"x1": 1, "x5": 1, "x2": 2, "x6": 2, "x3": 3, "x4": 3}
draw_undirected("hard_2_graf.png", e_h2, pos_h2, "Повышенная 2. Граф несовместимости переменных")
draw_undirected("hard_2_color.png", e_h2, pos_h2,
                "Повышенная 2. 3 регистра: {x1,x5}, {x2,x6}, {x3,x4}",
                colors=reg)

print("graphs done")
