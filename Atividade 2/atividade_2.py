
"""
Atividade 2 — Árvore Binária de Busca (BST)
-------------------------------------------
Requisitos atendidos:
- Linguagem: Python
- Classe BinarySearchTree com: insert, search, delete, height, depth
- Demonstração com valores fixos e valores aleatórios
- Visualização "similar ao Graphviz" usando matplotlib (sem depender do binário do Graphviz)
- Geração de imagens PNG da árvore

Como executar localmente:
    pip install matplotlib
    python atividade_2.py

Arquivos gerados na execução:
    - bst_fixa_before.png / bst_fixa_after.png
    - bst_random.png
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
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
    def __hash__(self) -> int:  # permite uso como chave em dicionários
        return id(self)


class BinarySearchTree:
    """BST com inserção, busca, remoção, altura e profundidade."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # --------- Inserção ---------
    def insert(self, key: int) -> None:
        """Insere um novo valor na BST (sem permitir duplicatas)."""
        def _insert(node: Optional[Node], key: int) -> Node:
            if node is None:
                return Node(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            # se igual, ignora (não insere duplicata)
            return node
        self.root = _insert(self.root, key)

    # --------- Busca ---------
    def search(self, key: int) -> Optional[Node]:
        """Retorna o nó com a chave `key` ou None se não encontrado."""
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    # --------- Remoção ---------
    def delete(self, key: int) -> None:
        """Remove a chave `key` tratando os 3 casos (folha, um filho, dois filhos)."""
        def _min_node(n: Node) -> Node:
            while n.left:
                n = n.left
            return n

        def _delete(node: Optional[Node], key: int) -> Optional[Node]:
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Encontrou o nó a remover
                if node.left is None and node.right is None:
                    return None  # caso 1: folha
                if node.left is None:
                    return node.right  # caso 2: um filho (direita)
                if node.right is None:
                    return node.left   # caso 2: um filho (esquerda)
                # caso 3: dois filhos -> substitui por sucessor (menor da subárvore direita)
                succ = _min_node(node.right)
                node.key = succ.key
                node.right = _delete(node.right, succ.key)
            return node

        self.root = _delete(self.root, key)

    # --------- Altura ---------
    def height(self) -> int:
        """Altura da árvore (número de arestas no caminho mais longo da raiz a uma folha).
        Árvore vazia tem altura -1; árvore com um nó tem altura 0.
        """
        def _h(n: Optional[Node]) -> int:
            if n is None:
                return -1
            return 1 + max(_h(n.left), _h(n.right))
        return _h(self.root)

    # --------- Profundidade ---------
    def depth(self, key: int) -> Optional[int]:
        """Profundidade (nível) do nó com valor `key`. Raiz tem profundidade 0.
        Retorna None se não existir.
        """
        cur = self.root
        d = 0
        while cur:
            if key == cur.key:
                return d
            d += 1
            cur = cur.left if key < cur.key else cur.right
        return None


# ----------------------
# Visualização (matplotlib)
# ----------------------
def _assign_positions_inorder(root: Optional[Node]) -> dict[Node, tuple[float, float]]:
    """Atribui coordenadas (x,y) por percurso em-ordem e ajusta pais sobre filhos."""
    positions: dict[Node, tuple[float, float]] = {}
    x_counter = 0

    def inorder(n: Optional[Node], depth: int) -> None:
        nonlocal x_counter
        if n is None:
            return
        inorder(n.left, depth + 1)
        positions[n] = (x_counter, -depth)
        x_counter += 1
        inorder(n.right, depth + 1)

    inorder(root, 0)

    def fix_parent(n: Optional[Node]) -> None:
        if n is None:
            return
        fix_parent(n.left)
        fix_parent(n.right)
        if n.left or n.right:
            xs = []
            if n.left: xs.append(positions[n.left][0])
            if n.right: xs.append(positions[n.right][0])
            if xs:
                positions[n] = (sum(xs)/len(xs), positions[n][1])

    fix_parent(root)
    return positions


def draw_bst_png(root: Optional[Node], outfile: str) -> None:
    """Desenha a BST em um PNG."""
    if root is None:
        # cria uma figura vazia indicando árvore vazia
        plt.figure(figsize=(6, 3), dpi=150)
        plt.text(0.5, 0.5, "Árvore vazia", ha="center", va="center")
        plt.axis("off")
        plt.savefig(outfile, bbox_inches="tight")
        plt.close()
        return

    pos = _assign_positions_inorder(root)
    plt.figure(figsize=(10, 4.5), dpi=150)

    # Arestas
    def draw_edges(n: Optional[Node]):
        if n is None:
            return
        for child in (n.left, n.right):
            if child:
                x1, y1 = pos[n]
                x2, y2 = pos[child]
                plt.plot([x1, x2], [y1, y2])
        draw_edges(n.left)
        draw_edges(n.right)

    draw_edges(root)

    # Nós
    for n, (x, y) in pos.items():
        circle = plt.Circle((x, y), 0.18, fill=False)
        plt.gca().add_patch(circle)
        plt.text(x, y, str(n.key), ha="center", va="center")

    xs = [x for x, _ in pos.values()]
    ys = [y for _, y in pos.values()]
    plt.xlim(min(xs)-1, max(xs)+1)
    plt.ylim(min(ys)-1, max(ys)+1)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(outfile, bbox_inches="tight")
    plt.close()


# ----------------------
# Demonstrações (main)
# ----------------------
def demo_fixed() -> None:
    """Árvore com valores fixos e operações de busca/remoção/inserção."""
    bst = BinarySearchTree()
    values = [55, 30, 80, 20, 45, 70, 90]
    for v in values:
        bst.insert(v)

    # Visualização antes
    draw_bst_png(bst.root, "bst_fixa_before.png")

    # Demonstra: busca, remoção e nova inserção
    search_target = 45
    found = bst.search(search_target) is not None
    print(f"Busca por {search_target}: {'encontrado' if found else 'não encontrado'}")

    delete_target = 30
    bst.delete(delete_target)
    print(f"Remoção do valor {delete_target} realizada.")

    insert_value = 60
    bst.insert(insert_value)
    print(f"Inserção do valor {insert_value} realizada.")

    # Altura e profundidade
    h = bst.height()
    d = bst.depth(search_target)
    print(f"Altura da árvore: {h}")
    print(f"Profundidade do nó {search_target}: {d if d is not None else 'não encontrado'}")

    # Visualização depois das operações
    draw_bst_png(bst.root, "bst_fixa_after.png")


def demo_random() -> None:
    """Árvore com 15 números aleatórios (1..200)."""
    bst = BinarySearchTree()
    nums = random.sample(range(1, 201), 15)  # 15 distintos
    for v in nums:
        bst.insert(v)
    print("Lista aleatória inserida:", nums)
    print("Altura da árvore aleatória:", bst.height())
    draw_bst_png(bst.root, "bst_random.png")


def main() -> None:
    random.seed(42)  # reprodutibilidade
    print("=== Demonstração com valores fixos ===")
    demo_fixed()
    print("\n=== Demonstração com valores aleatórios ===")
    demo_random()
    print("\nArquivos gerados: bst_fixa_before.png, bst_fixa_after.png, bst_random.png")


if __name__ == "__main__":
    main()
