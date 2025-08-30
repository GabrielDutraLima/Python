
"""
Atividade 3 — Travessias DFS em Árvore Binária (In-Order, Pre-Order, Post-Order)
--------------------------------------------------------------------------------
Requisitos atendidos:
- Linguagem: Python
- Implementação de travessias: inorder, preorder e postorder
- Duas árvores (fixa e aleatória) com visualização via matplotlib
- Saída clara com as sequências das três travessias para cada árvore


Arquivos gerados:
    - arvore3_fixa.png
    - arvore3_random.png
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple, Iterable
import random
import matplotlib.pyplot as plt


# ----------------------
# Estrutura de Dados
# ----------------------
@dataclass
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    def __hash__(self) -> int:
        # permite usar nós como chaves em dicionários (para posicionamento)
        return id(self)


class BinarySearchTree:
    """BST com inserção e travessias DFS."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # Inserção padrão de BST (sem duplicatas)
    def insert(self, key: int) -> None:
        def _insert(n: Optional[Node], k: int) -> Node:
            if n is None:
                return Node(k)
            if k < n.key:
                n.left = _insert(n.left, k)
            elif k > n.key:
                n.right = _insert(n.right, k)
            return n
        self.root = _insert(self.root, key)

    # ---------- Travessias DFS ----------
    def inorder(self) -> List[int]:
        """Esquerda-Raiz-Direita."""
        res: List[int] = []
        def _in(n: Optional[Node]):
            if not n: return
            _in(n.left)
            res.append(n.key)
            _in(n.right)
        _in(self.root)
        return res

    def preorder(self) -> List[int]:
        """Raiz-Esquerda-Direita."""
        res: List[int] = []
        def _pre(n: Optional[Node]):
            if not n: return
            res.append(n.key)
            _pre(n.left)
            _pre(n.right)
        _pre(self.root)
        return res

    def postorder(self) -> List[int]:
        """Esquerda-Direita-Raiz."""
        res: List[int] = []
        def _post(n: Optional[Node]):
            if not n: return
            _post(n.left)
            _post(n.right)
            res.append(n.key)
        _post(self.root)
        return res


# ----------------------
# Visualização (matplotlib)
# ----------------------
def _assign_positions_inorder(root: Optional[Node]) -> dict[Node, tuple[float, float]]:
    """Atribui coordenadas (x,y) por percurso em-ordem e ajusta pais sobre a média dos filhos."""
    positions: dict[Node, tuple[float, float]] = {}
    x_counter = 0

    def inorder(n: Optional[Node], depth: int) -> None:
        nonlocal x_counter
        if n is None: return
        inorder(n.left, depth + 1)
        positions[n] = (x_counter, -depth)
        x_counter += 1
        inorder(n.right, depth + 1)
    inorder(root, 0)

    def fix_parent(n: Optional[Node]) -> None:
        if n is None: return
        fix_parent(n.left); fix_parent(n.right)
        if n.left or n.right:
            xs = []
            if n.left: xs.append(positions[n.left][0])
            if n.right: xs.append(positions[n.right][0])
            if xs:
                y = positions[n][1]
                positions[n] = (sum(xs)/len(xs), y)
    fix_parent(root)
    return positions


def draw_bst_png(root: Optional[Node], outfile: str) -> None:
    """Desenha a árvore em PNG."""
    if root is None:
        plt.figure(figsize=(6,3), dpi=150)
        plt.text(0.5,0.5,"Árvore vazia", ha="center", va="center")
        plt.axis("off"); plt.savefig(outfile, bbox_inches="tight"); plt.close(); return
    pos = _assign_positions_inorder(root)
    plt.figure(figsize=(10,4.5), dpi=150)

    def draw_edges(n: Optional[Node]):
        if n is None: return
        for child in (n.left, n.right):
            if child:
                (x1,y1),(x2,y2)=pos[n],pos[child]
                plt.plot([x1,x2],[y1,y2])
        draw_edges(n.left); draw_edges(n.right)
    draw_edges(root)

    for n,(x,y) in pos.items():
        circle = plt.Circle((x,y), 0.18, fill=False)
        plt.gca().add_patch(circle)
        plt.text(x,y,str(n.key), ha="center", va="center")

    xs = [x for x,_ in pos.values()]; ys = [y for _,y in pos.values()]
    plt.xlim(min(xs)-1, max(xs)+1); plt.ylim(min(ys)-1, max(ys)+1)
    plt.axis("off"); plt.tight_layout(); plt.savefig(outfile, bbox_inches="tight"); plt.close()


# ----------------------
# Demonstrações (main)
# ----------------------
def make_bst_from_list(values: List[int]) -> BinarySearchTree:
    bst = BinarySearchTree()
    for v in values:
        bst.insert(v)
    return bst

def demo_fixed() -> None:
    values = [55, 30, 80, 20, 45, 70, 90]
    bst = make_bst_from_list(values)
    draw_bst_png(bst.root, "arvore3_fixa.png")
    print("=== Árvore FIXA ===")
    print("Valores inseridos:", values)
    print("In-Order  (E-R-D):", bst.inorder())
    print("Pre-Order (R-E-D):", bst.preorder())
    print("Post-Order(E-D-R):", bst.postorder())
    print()

def demo_random() -> None:
    values = random.sample(range(1,201), 10)  # 10 distintos para evitar duplicatas
    bst = make_bst_from_list(values)
    draw_bst_png(bst.root, "arvore3_random.png")
    print("=== Árvore RANDÔMICA ===")
    print("Valores inseridos:", values)
    print("In-Order  (E-R-D):", bst.inorder())
    print("Pre-Order (R-E-D):", bst.preorder())
    print("Post-Order(E-D-R):", bst.postorder())
    print()

def main() -> None:
    random.seed(123)  # reprodutibilidade da parte randômica
    demo_fixed()
    demo_random()
    print("Imagens geradas: arvore3_fixa.png, arvore3_random.png")

if __name__ == "__main__":
    main()
