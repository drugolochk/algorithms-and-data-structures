# -*- coding: utf-8 -*-
"""Симулятор безмасштабной сети Барабаши–Альберт."""
import random
from collections import Counter

random.seed(42)

m0 = 3
N = 1000
m = 2

# старт: полный граф на m0 вершинах (рёбра в обе стороны как список концов)
# ends: список вершин с повторением по степени (для preferential attachment)
ends = []
for i in range(m0):
    for j in range(i + 1, m0):
        ends.append(i)
        ends.append(j)

n_start = m0
for new in range(m0, m0 + N):
    # выбираем m различных вершин пропорционально степени
    chosen = set()
    while len(chosen) < m:
        chosen.add(random.choice(ends))
    for v in chosen:
        ends.append(v)
        ends.append(new)

deg = Counter(ends)
top = deg.most_common(5)
print("Вершин всего:", m0 + N)
print("Рёбер:", len(ends) // 2)
print("Топ-5 хабов (вершина, степень):")
for v, d in top:
    print(f"  узел {v}: степень {d}")
