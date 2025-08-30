
"""
Atividade 4 — Árvore AVL (auto-balanceada)
------------------------------------------
Requisitos atendidos:
- Linguagem: Python
- Classe AVLTree com inserção balanceada, fator de balanceamento e rotações:
  * Rotação simples à direita (LL)
  * Rotação simples à esquerda (RR)
  * Rotação dupla esquerda-direita (LR)
  * Rotação dupla direita-esquerda (RL)
- Demonstrações:
  1) Sequência [10, 20, 30] (força rotação simples)
  2) Sequência [10, 30, 20] (força rotação dupla)
  3) 20 números aleatórios (árvore permanece balanceada)
- Visualização via matplotlib (PNG) a cada passo quando relevante


Arquivos gerados (nomes principais):
    - avl_LL_step1.png, avl_LL_step2.png, avl_LL_step3.png
    - avl_LR_step1.png, avl_LR_step2.png, avl_LR_step3.png
    - avl_random.png
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
import random
import matplotlib.pyplot as plt


# ----------------------
# Estruturas e AVL Tree
# ----------------------
@dataclass
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    height: int = 0

    def __hash__(self) -> int:
        # permite usar o nó como chave de dicionário (para posicionamento)
        return id(self)


def _h(n: Optional[Node]) -> int:
    return -1 if n is None else n.height


def _update_height(n: Node) -> None:
    n.height = 1 + max(_h(n.left), _h(n.right))


def _balance_factor(n: Optional[Node]) -> int:
    """Fator de balanceamento: altura(esq) - altura(dir)."""
    if n is None:
        return 0
    return _h(n.left) - _h(n.right)


class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # ---------- Rotações ----------
    def _rotate_right(self, y: Node) -> Node:
        """Rotação simples à direita (LL)."""
        x = y.left
        T2 = x.right if x else None

        # Rotaciona
        x.right = y
        y.left = T2

        # Atualiza alturas
        _update_height(y)
        _update_height(x)
        return x

    def _rotate_left(self, x: Node) -> Node:
        """Rotação simples à esquerda (RR)."""
        y = x.right
        T2 = y.left if y else None

        # Rotaciona
        y.left = x
        x.right = T2

        # Atualiza alturas
        _update_height(x)
        _update_height(y)
        return y

    # ---------- Inserção balanceada ----------
    def insert(self, key: int) -> None:
        """Insere uma chave mantendo as propriedades da AVL."""
        def _insert(n: Optional[Node], key: int) -> Node:
            # inserção BST padrão
            if n is None:
                return Node(key)
            if key < n.key:
                n.left = _insert(n.left, key)
            elif key > n.key:
                n.right = _insert(n.right, key)
            else:
                # não insere duplicata
                return n

            # atualiza altura deste nó
            _update_height(n)

            # verifica balanceamento
            bf = _balance_factor(n)

            # Casos de desbalanceamento:
            # 1) LL (esq-esq): bf > 1 e key < n.left.key
            if bf > 1 and key < (n.left.key if n.left else key):
                return self._rotate_right(n)

            # 2) RR (dir-dir): bf < -1 e key > n.right.key
            if bf < -1 and key > (n.right.key if n.right else key):
                return self._rotate_left(n)

            # 3) LR (esq-dir): bf > 1 e key > n.left.key
            if bf > 1 and key > (n.left.key if n.left else key):
                n.left = self._rotate_left(n.left)
                return self._rotate_right(n)

            # 4) RL (dir-esq): bf < -1 e key < n.right.key
            if bf < -1 and key < (n.right.key if n.right else key):
                n.right = self._rotate_right(n.right)
                return self._rotate_left(n)

            return n

        self.root = _insert(self.root, key)

    # Expor fator de balanceamento (para debug/avaliação)
    def balance_factor(self, node: Optional[Node]) -> int:
        return _balance_factor(node)


# ----------------------
# Visualização (matplotlib)
# ----------------------
def _assign_positions_inorder(root: Optional[Node]) -> Dict[Node, Tuple[float, float]]:
    """Atribui coordenadas (x,y) por percurso em-ordem e centraliza os pais sobre os filhos."""
    positions: Dict[Node, Tuple[float, float]] = {}
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


def draw_tree_png(root: Optional[Node], outfile: str, title: Optional[str] = None) -> None:
    """Desenha a árvore em PNG. Mostra chave e altura em cada nó."""
    if root is None:
        plt.figure(figsize=(6,3), dpi=150)
        plt.text(0.5, 0.5, "Árvore vazia", ha="center", va="center")
        if title: plt.title(title)
        plt.axis("off")
        plt.savefig(outfile, bbox_inches="tight"); plt.close(); return

    pos = _assign_positions_inorder(root)
    plt.figure(figsize=(10, 4.5), dpi=150)

    # Arestas
    def draw_edges(n: Optional[Node]):
        if n is None: return
        for child in (n.left, n.right):
            if child:
                (x1,y1),(x2,y2)=pos[n],pos[child]
                plt.plot([x1,x2],[y1,y2])
        draw_edges(n.left); draw_edges(n.right)
    draw_edges(root)

    # Nós: chave e altura
    for n,(x,y) in pos.items():
        circle = plt.Circle((x,y), 0.2, fill=False)
        plt.gca().add_patch(circle)
        plt.text(x, y+0.12, str(n.key), ha="center", va="center", fontsize=10)
        plt.text(x, y-0.12, f"h={n.height}", ha="center", va="center", fontsize=8)

    xs = [x for x,_ in pos.values()]; ys = [y for _,y in pos.values()]
    plt.xlim(min(xs)-1, max(xs)+1); plt.ylim(min(ys)-1, max(ys)+1)
    if title: plt.title(title)
    plt.axis("off"); plt.tight_layout(); plt.savefig(outfile, bbox_inches="tight"); plt.close()


# ----------------------
# Demonstrações
# ----------------------
def demo_sequence(seq: List[int], prefix: str) -> None:
    """Insere elementos de `seq` em ordem, salvando PNG a cada passo."""
    avl = AVLTree()
    for i, v in enumerate(seq, start=1):
        avl.insert(v)
        draw_tree_png(avl.root, f"{prefix}_step{i}.png", title=f"{prefix}: após inserir {v}")
        print(f"{prefix}: inserido {v}, altura da raiz = {_h(avl.root)}")
    # No final, mostra fatores de balanceamento da raiz
    print(f"{prefix}: fator de balanceamento (raiz) = {avl.balance_factor(avl.root)}")


def demo_random(n: int = 20) -> None:
    """Gera n números distintos e insere em uma AVL, salvando a árvore final."""
    values = random.sample(range(1, 500), n)
    avl = AVLTree()
    for v in values:
        avl.insert(v)
    draw_tree_png(avl.root, "avl_random.png", title="AVL com 20 valores aleatórios")
    print("Valores aleatórios inseridos:", values)
    print("Altura final:", _h(avl.root))


def main() -> None:
    random.seed(2025)  # reprodutibilidade da parte aleatória

    # 1) Sequência que força rotação simples (LL): [10, 20, 30]
    print("=== Sequência que força rotação simples (LL) ===")
    demo_sequence([10, 20, 30], prefix="avl_LL")

    # 2) Sequência que força rotação dupla (LR): [10, 30, 20]
    print("\\n=== Sequência que força rotação dupla (LR) ===")
    demo_sequence([10, 30, 20], prefix="avl_LR")

    # 3) 20 números randômicos
    print("\\n=== AVL com 20 valores aleatórios ===")
    demo_random(20)
    print("\\nImagens geradas: avl_LL_step1.png..step3.png, avl_LR_step1.png..step3.png, avl_random.png")


if __name__ == "__main__":
    main()
