# -*- coding: utf-8 -*-
from collections import deque, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def max_flow(edges, s, t):
    """Ford-Fulkerson with BFS (Edmonds-Karp). Returns flow, paths, residual, min-cut."""
    cap = defaultdict(lambda: defaultdict(int))
    nodes = set()
    for u, v, c in edges:
        cap[u][v] += c
        nodes.add(u)
        nodes.add(v)
        cap[v][u] += 0

    flow = defaultdict(lambda: defaultdict(int))
    paths = []

    def residual(u, v):
        return cap[u][v] - flow[u][v]

    def bfs():
        parent = {s: None}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in list(cap[u].keys()) + list(cap[v].keys() if False else []):
                pass
            nbrs = set(cap[u].keys()) | set(x for x in cap if cap[x][u] or cap[u][x])
            # all possible neighbors
            nbrs = set(cap[u]) | {x for x in cap if u in cap[x]}
            for v in nbrs:
                if v not in parent and residual(u, v) > 0:
                    parent[v] = u
                    if v == t:
                        return parent
                    q.append(v)
        return None

    while True:
        parent = bfs()
        if parent is None or t not in parent:
            break
        path = [t]
        while path[-1] != s:
            path.append(parent[path[-1]])
        path.reverse()
        bneck = min(residual(path[i], path[i + 1]) for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow[u][v] += bneck
            flow[v][u] -= bneck
        paths.append((path, bneck))

    total = sum(flow[s][v] for v in cap[s])

    # min cut: reachable in residual from s
    seen = set()
    q = deque([s])
    seen.add(s)
    while q:
        u = q.popleft()
        nbrs = set(cap[u]) | {x for x in cap if u in cap[x]}
        for v in nbrs:
            if v not in seen and residual(u, v) > 0:
                seen.add(v)
                q.append(v)
    cut_edges = []
    for u, v, c in edges:
        if u in seen and v not in seen:
            cut_edges.append((u, v, c))
    return total, paths, flow, seen, cut_edges, cap


def draw_net(name, edges, pos, title, directed=True, flow=None):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="#b8d4f0",
                           edgecolors="#1f4e79", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.6, edge_color="#333",
                           arrows=True, arrowstyle="-|>", arrowsize=16,
                           connectionstyle="arc3,rad=0.04",
                           min_source_margin=14, min_target_margin=14)
    if flow is None:
        labels = {(u, v): w for u, v, w in edges}
    else:
        labels = {}
        for u, v, w in edges:
            f = max(0, flow[u][v])
            labels[(u, v)] = f"{f}/{w}"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax, font_size=9)
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


def dump(title, edges, s, t, pos, prefix):
    total, paths, flow, Sset, cut, cap = max_flow(edges, s, t)
    print("=" * 60)
    print(title)
    print("max flow", total)
    print("paths:")
    for p, b in paths:
        print(" ", " -> ".join(map(str, p)), " +", b)
    print("min cut S' =", sorted(Sset, key=str))
    print("cut edges", cut, "cap", sum(c for _, _, c in cut))
    draw_net(f"{prefix}_graf.png", edges, pos, title)
    draw_net(f"{prefix}_flow.png", edges, pos, title + "  (поток/ёмкость)", flow=flow)
    return total, paths, flow, Sset, cut


# ---- sam 1 ----
e1 = [
    (1, 2, 3), (1, 4, 5),
    (4, 2, 4), (2, 3, 5),
    (4, 5, 2), (3, 5, 9),
    (3, 6, 5), (5, 6, 7),
]
pos1 = {1: (0, 1), 2: (1.6, 2), 3: (3.4, 2), 4: (1.6, 0), 5: (3.4, 0), 6: (5.2, 1)}
dump("Задание 1. Сеть 1 -> 6", e1, 1, 6, pos1, "sam_1")

# ---- sam 2 ----
e2 = [
    ("S", "A", 10), ("S", "B", 5),
    ("A", "C", 8),
    ("C", "D", 3), ("C", "E", 6),
    ("B", "D", 6),
    ("D", "F", 5), ("E", "F", 8),
    ("F", "T", 10),
]
pos2 = {
    "S": (0, 1), "A": (1.4, 2), "B": (1.4, 0),
    "C": (2.8, 2), "D": (2.8, 0.6), "E": (4.2, 2.4),
    "F": (5.4, 1.2), "T": (6.8, 1.2),
}
dump("Задание 2. Сеть S -> T", e2, "S", "T", pos2, "sam_2")

# ---- sam 3 (в тексте «1 в 6», на рисунке S..T) ----
e3 = [
    ("S", "A", 12), ("S", "B", 7),
    ("A", "C", 5), ("B", "C", 3),
    ("C", "E", 6), ("C", "D", 10),
    ("D", "E", 5), ("D", "F", 4),
    ("E", "F", 5), ("F", "T", 7),
]
pos3 = {
    "S": (0, 1.1), "A": (1.5, 2.3), "B": (1.5, 0),
    "C": (3.0, 1.8), "D": (3.2, 0.5), "E": (4.6, 1.5),
    "F": (6.0, 1.1), "T": (7.4, 1.1),
}
dump("Задание 3. Сеть S -> T", e3, "S", "T", pos3, "sam_3")

# ---- hard 1 ----
eh1 = [
    (1, 5, 41), (1, 2, 28),
    (2, 3, 23), (2, 7, 5),
    (3, 5, 23), (3, 4, 19), (3, 7, 47),
    (5, 4, 46), (5, 9, 21),
    (4, 6, 12),
    (6, 9, 17),
    (7, 8, 11),
    (8, 9, 43),
]
pos_h1 = {
    1: (0, 1.2), 2: (1.6, 0.2), 3: (2.4, 1.2), 5: (2.0, 2.4),
    4: (4.0, 1.6), 7: (3.6, 0.0), 6: (5.4, 1.6), 8: (5.4, 0.0), 9: (7.0, 1.8),
}
dump("Повышенная 1. Сеть 1 -> 9", eh1, 1, 9, pos_h1, "hard_1")

# ---- hard 2 ----
eh2 = [
    ("S", "A", 9), ("S", "B", 7),
    ("A", "C", 4), ("B", "D", 6),
    ("C", "E", 8), ("D", "E", 5),
    ("E", "F", 7), ("F", "G", 6), ("G", "T", 10),
]
pos_h2 = {
    "S": (0, 1.2), "A": (1.4, 2.3), "B": (1.4, 0.1),
    "C": (2.8, 2.3), "D": (2.8, 0.1), "E": (4.2, 1.2),
    "F": (5.6, 2.2), "G": (5.6, 0.2), "T": (7.2, 0.8),
}
dump("Повышенная 2. Сеть S -> T", eh2, "S", "T", pos_h2, "hard_2")

# ---- hard 3 ----
eh3 = [
    ("S", "A", 10), ("S", "B", 15),
    ("A", "C", 10), ("A", "D", 5),
    ("B", "D", 10), ("B", "E", 10),
    ("C", "F", 10),
    ("D", "F", 10), ("D", "G", 5),
    ("E", "G", 10), ("E", "H", 5),
    ("F", "I", 10),
    ("G", "I", 10), ("G", "J", 5),
    ("H", "J", 10),
    ("I", "K", 15), ("I", "T", 5),
    ("J", "K", 10), ("J", "T", 7),
    ("K", "T", 10),
]
pos_h3 = {
    "S": (0, 1.4), "A": (1.3, 2.4), "B": (1.3, 0.4),
    "C": (2.6, 3.0), "D": (2.6, 1.6), "E": (2.6, 0.0),
    "F": (4.0, 3.0), "G": (4.0, 1.4), "H": (4.0, 0.0),
    "I": (5.4, 2.8), "J": (5.4, 0.8), "K": (6.6, 1.6), "T": (7.8, 1.6),
}
dump("Повышенная 3. Сеть S -> T", eh3, "S", "T", pos_h3, "hard_3")

# ---- hard 4 ----
eh4 = [
    ("S", "A", 10), ("S", "B", 5),
    ("A", "C", 9),
    ("B", "C", 4), ("B", "D", 8),
    ("C", "T", 10), ("D", "T", 10),
]
pos_h4 = {
    "S": (0, 1.2), "A": (1.8, 2.2), "B": (1.8, 0.2),
    "C": (3.6, 2.2), "D": (3.6, 0.2), "T": (5.4, 1.2),
}
dump("Повышенная 4. Сеть S -> T (Эдмондс-Карп)", eh4, "S", "T", pos_h4, "hard_4")

print("done")
