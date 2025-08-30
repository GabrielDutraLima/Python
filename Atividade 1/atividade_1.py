"""
Atividade 1 — Árvores de Expressão 
-------------------------------------------------
Este script demonstra como:
1) Converter uma expressão aritmética em notação infixa (string) para
   uma estrutura hierárquica (árvore binária de expressão).
2) Visualizar a árvore resultante como imagem.
3) Repetir o processo para uma expressão aleatória simples.


Como executar:
    python atividade_1.py

Saídas geradas:
    - arvore_fixa.png       (imagem da árvore da expressão fixa)
    - arvore_random.png     (imagem da árvore da expressão aleatória)
    - arvore_fixa.txt       (árvore ASCII para conferência)
    - arvore_random.txt
    - arvore_fixa.dot       (opcional: DOT para usar com Graphviz)
    - arvore_random.dot
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union, Iterable, Tuple
import random
import re
import math

# anytree é usada para representar nós e percorrer a árvore;
# DotExporter exporta a árvore para o formato DOT (Graphviz).
from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter

# matplotlib é usada para desenhar a árvore em PNG, sem exigir Graphviz instalado.
import matplotlib.pyplot as plt


# =========================================================
# 1) Tokenização da expressão
#    - Converte a string em uma lista de tokens (números,
#      operadores e parênteses), ignorando espaços.
# =========================================================

# Especificação de tokens via regex:
#  NUMBER: inteiros ou decimais
#  OP:     operadores + - * /
#  LPAREN: (
#  RPAREN: )
#  SPACE:  espaços/tabs (serão ignorados)
_TOKEN_SPEC = [
    ("NUMBER",  r"\d+(\.\d+)?"),
    ("OP",      r"[\+\-\*/]"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("SPACE",   r"[ \t]+"),
]

# Compila uma única regex com grupos nomeados para cada tipo de token.
_TOKEN_RE = re.compile("|".join(f"(?P<{name}>{regex})" for name, regex in _TOKEN_SPEC))

def tokenize(expr: str) -> List[str]:
    """
    Converte string `expr` em lista de tokens.
    Exemplos:
        "( 7 + 3 )" -> ["(", "7", "+", "3", ")"]
    """
    tokens = []
    for m in _TOKEN_RE.finditer(expr):
        kind = m.lastgroup   # tipo de token encontrado
        value = m.group()    # texto correspondente
        if kind == "SPACE":
            continue         # ignora espaços
        tokens.append(value)
    return tokens


# =========================================================
# 2) Shunting-yard: infixo -> pós-fixo (RPN)
#    - Converte a lista de tokens da notação infixa para
#      notação pós-fixa (Reverse Polish Notation).
#    - Facilita a montagem da árvore a partir de uma pilha.
# =========================================================

# Precedência e associatividade dos operadores.
_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}
_ASSOC = {"+": "L", "-": "L", "*": "L", "/": "L"}  # L = associativo à esquerda

def infix_to_postfix(tokens: List[str]) -> List[str]:
    """
    Implementação do algoritmo de Dijkstra (Shunting-yard).
    Recebe tokens em infixo e devolve lista de tokens em pós-fixo (RPN).
    """
    out: List[str] = []     # saída (fila)
    opstack: List[str] = [] # pilha de operadores
    for t in tokens:
        if re.fullmatch(r"\d+(\.\d+)?", t):  # número
            out.append(t)
        elif t in _PRECEDENCE:               # operador
            # Desempilha enquanto o topo tem maior/igual precedência
            # (para operadores associativos à esquerda).
            while opstack and opstack[-1] in _PRECEDENCE:
                top = opstack[-1]
                if (_ASSOC[t] == "L" and _PRECEDENCE[t] <= _PRECEDENCE[top]) or \
                   (_ASSOC[t] == "R" and _PRECEDENCE[t] < _PRECEDENCE[top]):
                    out.append(opstack.pop())
                else:
                    break
            opstack.append(t)
        elif t == "(":                        # abre parêntese
            opstack.append(t)
        elif t == ")":                        # fecha parêntese
            # Desempilha até encontrar "("
            while opstack and opstack[-1] != "(":
                out.append(opstack.pop())
            if not opstack:
                raise ValueError("Parênteses desbalanceados")
            opstack.pop()  # remove "("
        else:
            raise ValueError(f"Token desconhecido: {t}")
    # Move operadores restantes para a saída
    while opstack:
        op = opstack.pop()
        if op in ("(", ")"):
            raise ValueError("Parênteses desbalanceados no final")
        out.append(op)
    return out


# =========================================================
# 3) Construção da árvore a partir da RPN (pós-fixa)
#    - Percorre a lista pós-fixa; empilha operandos (nós folha)
#      e, ao encontrar um operador, desempilha 2 nós como filhos.
# =========================================================
def postfix_to_tree(postfix: List[str]) -> Node:
    """
    Constroi a árvore de expressão a partir da lista em notação pós-fixa (RPN).
    Retorna a raiz (Node) da árvore.
    """
    stack: List[Node] = []
    for t in postfix:
        if t in _PRECEDENCE:
            # Cada operador binário consome dois operandos da pilha
            if len(stack) < 2:
                raise ValueError("Expressão inválida: operandos insuficientes")
            right = stack.pop()
            left  = stack.pop()
            op = Node(t, children=[left, right])  # operador no pai; filhos em ordem
            stack.append(op)
        else:
            # Operando (número) vira nó folha
            stack.append(Node(t))
    if len(stack) != 1:
        raise ValueError("Expressão inválida: tokens restantes após montagem")
    return stack[0]


# =========================================================
# 4) Layout e desenho da árvore (matplotlib)
#    - Atribui coordenadas (x,y) por percurso em-ordem (inorder)
#      para espaçar nós folhas; depois ajusta pais sobre a média
#      dos filhos. Por fim, desenha arestas e nós.
# =========================================================
def assign_positions_inorder(root: Node) -> dict[Node, Tuple[float, float]]:
    """
    Atribui coordenadas (x,y) aos nós usando percurso em-ordem.
    y é a profundidade negativa para que a raiz fique no topo.
    Retorna um dicionário {nó: (x, y)}.
    """
    positions: dict[Node, Tuple[float, float]] = {}
    x_counter = 0

    def inorder(n: Node, depth: int) -> None:
        nonlocal x_counter
        if n.children:
            left = n.children[0]
            inorder(left, depth + 1)
        positions[n] = (x_counter, -depth)  # define posição do nó
        x_counter += 1
        if n.children and len(n.children) > 1:
            right = n.children[1]
            inorder(right, depth + 1)

    inorder(root, 0)

    # Ajuste fino: reposiciona o pai na média dos X dos filhos (pós-ordem)
    def fix_parent_positions(n: Node):
        for c in n.children or []:
            fix_parent_positions(c)
        if n.children:
            xs = [positions[c][0] for c in n.children]
            x_parent = sum(xs) / len(xs)
            y_parent = positions[n][1]
            positions[n] = (x_parent, y_parent)

    fix_parent_positions(root)
    return positions


def draw_tree(root: Node, outfile: str) -> None:
    """
    Desenha a árvore (nós e arestas) usando matplotlib e salva em PNG.
    """
    pos = assign_positions_inorder(root)

    plt.figure(figsize=(8, 4), dpi=150)

    # Desenha arestas (linhas pai->filho)
    for n in PreOrderIter(root):
        for c in n.children or []:
            x1, y1 = pos[n]
            x2, y2 = pos[c]
            plt.plot([x1, x2], [y1, y2])

    # Desenha nós (círculos) e rótulos (valores/operadores)
    for n in PreOrderIter(root):
        x, y = pos[n]
        circle = plt.Circle((x, y), 0.18, fill=False)
        plt.gca().add_patch(circle)
        plt.text(x, y, str(n.name), ha="center", va="center")

    # Ajustes de enquadramento
    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]
    if xs and ys:
        plt.xlim(min(xs) - 1, max(xs) + 1)
        plt.ylim(min(ys) - 1, max(ys) + 1)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(outfile, bbox_inches="tight")
    plt.close()


def save_ascii_and_dot(root: Node, ascii_path: str, dot_path: str) -> None:
    """
    Gera uma visualização textual da árvore (ASCII) e
    exporta o mesmo conteúdo em formato DOT (Graphviz).
    """
    # ASCII (árvore “deitada” com ramos)
    with open(ascii_path, "w", encoding="utf-8") as f:
        for pre, fill, node in RenderTree(root):
            f.write(f"{pre}{node.name}\n")
    # DOT (pode ser renderizado externamente com o binário do Graphviz)
    DotExporter(root).to_dotfile(dot_path)


# =========================================================
# 5) Geração de expressão aleatória simples
#    - Monta uma árvore binária aleatória de operadores e operandos,
#      depois imprime a expressão infixa totalmente parentizada.
# =========================================================
def random_expression(min_oper=2, max_oper=3) -> str:
    """
    Cria uma expressão aleatória com entre [min_oper, max_oper] operadores
    e (min_oper + 1) operandos. Usa +, -, *, / e números de 1 a 9.
    Retorna a expressão em notação infixa com parênteses.
    """
    n_ops = random.randint(min_oper, max_oper)
    nums = [str(random.randint(1, 9)) for _ in range(n_ops + 1)]
    ops_pool = ["+", "-", "*", "/"]
    ops = [random.choice(ops_pool) for _ in range(n_ops)]

    # Constrói uma árvore binária aleatória combinando nós de forma randômica
    def build_rand_tree(values: List[str], operators: List[str]) -> Node:
        nodes = [Node(v) for v in values]     # folhas (operandos)
        ops_nodes = [Node(op) for op in operators]  # nós internos (operadores)
        while ops_nodes:
            op_i = random.randrange(len(ops_nodes))
            left_i = random.randrange(len(nodes))
            right_i = random.randrange(len(nodes))
            while right_i == left_i:          # garante filhos distintos
                right_i = random.randrange(len(nodes))
            op = ops_nodes.pop(op_i)
            # Retira dois nós da lista e conecta como filhos do operador
            left = nodes.pop(max(left_i, right_i))
            right = nodes.pop(min(left_i, right_i))
            op.children = [right, left]       # ordem importa (esq, dir)
            nodes.append(op)                  # volta o novo subárvore para a lista
        assert len(nodes) == 1
        return nodes[0]

    root = build_rand_tree(nums, ops)

    # Converte a árvore para infixo com parênteses
    def to_infix(n: Node) -> str:
        if not n.children:
            return str(n.name)
        a = to_infix(n.children[0])
        b = to_infix(n.children[1])
        return f"( {a} {n.name} {b} )"

    return to_infix(root)


# =========================================================
# 6) Funções utilitárias e ponto de entrada
# =========================================================
def build_and_visualize(expr: str, png_name: str, ascii_name: str, dot_name: str) -> None:
    """
    Pipeline completo para uma expressão:
    - tokeniza -> infixo→pós-fixo -> monta árvore -> desenha PNG -> ASCII/DOT.
    """
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    root = postfix_to_tree(postfix)
    draw_tree(root, png_name)
    save_ascii_and_dot(root, ascii_name, dot_name)


def main() -> None:
    expr_fixa = "( ( 7 + 3 ) * ( 5 - 2 ) )"
    build_and_visualize(
        expr_fixa,
        png_name="arvore_fixa.png",
        ascii_name="arvore_fixa.txt",
        dot_name="arvore_fixa.dot",
    )

  
    expr_rand = random_expression(min_oper=2, max_oper=3)
    build_and_visualize(
        expr_rand,
        png_name="arvore_random.png",
        ascii_name="arvore_random.txt",
        dot_name="arvore_random.dot",
    )

    # Mensagens de console para referência rápida
    print("Expressão fixa:", expr_fixa)
    print("Expressão aleatória gerada:", expr_rand)
    print("Arquivos gerados: arvore_fixa.png, arvore_random.png, *.txt, *.dot")


if __name__ == "__main__":
    main()
