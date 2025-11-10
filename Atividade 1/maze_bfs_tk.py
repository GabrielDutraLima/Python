import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import random

# -----------------------------
# Configurações gerais
# -----------------------------
GRID_COLS = 30
GRID_ROWS = 20
CELL_SIZE = 28  # pixels
PADDING = 8

# Paleta de cores sugerida
COLOR_WALL       = "#1E3A5F"  # Parede
COLOR_PATH       = "#FFFFFF"  # Caminho
COLOR_START      = "#4CAF50"  # Início S
COLOR_END        = "#F44336"  # Fim E
COLOR_FRONTIER   = "#AED6F1"  # Na fila
COLOR_VISITED    = "#D6EAF8"  # Visitado
COLOR_SHORTEST   = "#FFD700"  # Caminho final

TOOLS = {
    "Parede (#)": "#",
    "Caminho ( )": " ",
    "Início (S)": "S",
    "Fim (E)": "E",
}

DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1)]  # 4-vizinhos


class MazeEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Labirintos - BFS (Tkinter)")
        self.mode = tk.StringVar(value="Modo Edição")  # "Modo Edição" | "Modo Simulação"
        self.tool_var = tk.StringVar(value=" ")        # ferramenta atual (modelo: ' ', '#', 'S', 'E')
        self.speed_ms = tk.IntVar(value=20)            # velocidade da animação (ms entre passos)

        # Modelo de dados do labirinto
        self.labirinto = [[' ' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.grid_cells = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

        # Posições únicas de início/fim
        self.inicio_pos = None  # (r, c)
        self.fim_pos = None     # (r, c)

        # Estruturas da BFS
        self.fila = None
        self.visitados = None
        self.predecessores = None
        self.encontrou = False
        self.job_after = None   # id para cancelar .after

        # Para impedir repintar indevidamente durante arrasto
        self._is_dragging = False

        self._build_ui()
        self._draw_initial_grid()

    # -----------------------------
    # Construção da UI
    # -----------------------------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=PADDING)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Canvas (lado esquerdo)
        canvas_w = GRID_COLS * CELL_SIZE
        canvas_h = GRID_ROWS * CELL_SIZE
        self.canvas = tk.Canvas(main, width=canvas_w, height=canvas_h, bg="#EEE", highlightthickness=1, highlightbackground="#CCC")
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, PADDING), pady=(0, PADDING))
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        # Painel de controles (lado direito)
        controls = ttk.Frame(main)
        controls.grid(row=0, column=1, sticky="n", padx=(0, PADDING))

        # Estado/Modo
        ttk.Label(controls, textvariable=self.mode, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, pady=(0, 8), sticky="w")

        # Grupo de Ferramentas (Radiobuttons)
        tools_frame = ttk.LabelFrame(controls, text="Ferramenta de Edição")
        tools_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for i, (label, val) in enumerate(TOOLS.items()):
            ttk.Radiobutton(tools_frame, text=label, value=val, variable=self.tool_var).grid(row=i, column=0, sticky="w", padx=6, pady=2)

        # Velocidade
        speed_frame = ttk.LabelFrame(controls, text="Velocidade (ms)")
        speed_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        ttk.Scale(speed_frame, from_=0, to=200, variable=self.speed_ms, orient="horizontal").grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        speed_frame.columnconfigure(0, weight=1)
        ttk.Label(speed_frame, text="0 = mais rápido").grid(row=1, column=0, padx=6, sticky="w")

        # Botões
        btns = ttk.Frame(controls)
        btns.grid(row=3, column=0, sticky="ew")
        ttk.Button(btns, text="Iniciar Busca (BFS)", command=self.iniciar_busca).grid(row=0, column=0, sticky="ew", pady=4)
        ttk.Button(btns, text="Resetar Busca", command=self.resetar_busca).grid(row=1, column=0, sticky="ew", pady=4)
        ttk.Button(btns, text="Limpar Labirinto", command=self.limpar_labirinto).grid(row=2, column=0, sticky="ew", pady=4)
        ttk.Button(btns, text="Gerar Labirinto Aleatório", command=self.gerar_labirinto_aleatorio).grid(row=3, column=0, sticky="ew", pady=4)

        # Ajuda
        help_box = ttk.LabelFrame(controls, text="Dicas")
        help_box.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        help_text = (
            "• Clique/arraste para desenhar.\n"
            "• Só pode haver 1 'S' e 1 'E'.\n"
            "• Durante a simulação, a edição é desativada.\n"
            "• Resetar: limpa cores da busca.\n"
            "• Limpar: zera tudo.\n"
            "• Gerar: cria um labirinto aleatório."
        )
        ttk.Label(help_box, text=help_text, justify="left").grid(row=0, column=0, padx=6, pady=6, sticky="w")

        # Bindings de mouse no Canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Estilo básico
        try:
            self.root.style = ttk.Style()
            if "vista" in self.root.style.theme_names():
                self.root.style.theme_use("vista")
        except Exception:
            pass

    def _draw_initial_grid(self):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_PATH, outline="#DDD")
                self.grid_cells[r][c] = rect

    # -----------------------------
    # Utilidades de grade e pintura
    # -----------------------------
    def _coords_to_cell(self, x, y):
        c = x // CELL_SIZE
        r = y // CELL_SIZE
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
            return (r, c)
        return None

    def _paint_cell(self, r, c, color):
        rect = self.grid_cells[r][c]
        self.canvas.itemconfig(rect, fill=color)

    def _color_for_model(self, ch):
        if ch == "#": return COLOR_WALL
        if ch == "S": return COLOR_START
        if ch == "E": return COLOR_END
        return COLOR_PATH

    # -----------------------------
    # Edição com mouse
    # -----------------------------
    def on_canvas_click(self, event):
        self._is_dragging = True
        cell = self._coords_to_cell(event.x, event.y)
        if not cell: return
        self._apply_tool_at(cell)

    def on_canvas_drag(self, event):
        if not self._is_dragging: return
        cell = self._coords_to_cell(event.x, event.y)
        if not cell: return
        self._apply_tool_at(cell)

    def on_canvas_release(self, event):
        self._is_dragging = False

    def _apply_tool_at(self, cell):
        if self.mode.get() != "Modo Edição":
            return  # edição desativada durante simulação

        r, c = cell
        tool = self.tool_var.get()

        if tool == "#":
            self._set_cell(r, c, "#")
        elif tool == " ":
            self._set_cell(r, c, " ")
        elif tool == "S":
            self._set_start(r, c)
        elif tool == "E":
            self._set_end(r, c)

    def _set_cell(self, r, c, ch):
        # impede sobrescrever S/E inadvertidamente quando desenhando paredes ou caminho
        if ch in ("#", " "):
            if self.labirinto[r][c] == "S": self.inicio_pos = None
            if self.labirinto[r][c] == "E": self.fim_pos = None

        self.labirinto[r][c] = ch
        self._paint_cell(r, c, self._color_for_model(ch))

    def _set_start(self, r, c):
        # limpa S antigo
        if self.inicio_pos is not None:
            rr, cc = self.inicio_pos
            self.labirinto[rr][cc] = " "
            self._paint_cell(rr, cc, COLOR_PATH)
        # define novo
        self.labirinto[r][c] = "S"
        self.inicio_pos = (r, c)
        self._paint_cell(r, c, COLOR_START)

    def _set_end(self, r, c):
        # limpa E antigo
        if self.fim_pos is not None:
            rr, cc = self.fim_pos
            self.labirinto[rr][cc] = " "
            self._paint_cell(rr, cc, COLOR_PATH)
        # define novo
        self.labirinto[r][c] = "E"
        self.fim_pos = (r, c)
        self._paint_cell(r, c, COLOR_END)

    # -----------------------------
    # Controles de estado
    # -----------------------------
    def _set_mode(self, mode):
        self.mode.set(mode)

    def _enable_editing(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        # desabilitar os radiobuttons e slider
        def set_state_in(frame):
            for child in frame.winfo_children():
                try:
                    child.configure(state=state)
                except Exception:
                    pass
                set_state_in(child)
        set_state_in(self.root)

        # Reativar botões de ação apropriados
        def enable_buttons_by_text(texts, en_state):
            stack = [self.root]
            while stack:
                w = stack.pop()
                try:
                    if isinstance(w, ttk.Button) and (w.cget("text") in texts):
                        w.configure(state=en_state)
                except Exception:
                    pass
                for ch in w.winfo_children():
                    stack.append(ch)

        if enabled:
            enable_buttons_by_text({"Iniciar Busca (BFS)", "Resetar Busca", "Limpar Labirinto", "Gerar Labirinto Aleatório"}, "normal")
        else:
            enable_buttons_by_text({"Resetar Busca"}, "normal")
            enable_buttons_by_text({"Iniciar Busca (BFS)", "Limpar Labirinto", "Gerar Labirinto Aleatório"}, "disabled")

    # -----------------------------
    # BFS e animação
    # -----------------------------
    def iniciar_busca(self):
        if self.inicio_pos is None or self.fim_pos is None:
            messagebox.showwarning("Aviso", "Defina um ponto de Início (S) e um ponto de Fim (E) antes de iniciar a busca.")
            return

        self.resetar_busca(full_clear_colors=True)  # limpa cores de buscas anteriores
        self._set_mode("Modo Simulação")
        self._enable_editing(False)

        self.fila = deque()
        self.visitados = set()
        self.predecessores = dict()
        self.encontrou = False

        sr, sc = self.inicio_pos
        self.fila.append((sr, sc))
        self.visitados.add((sr, sc))

        # agenda o primeiro passo
        self._schedule_next_step()

    def _schedule_next_step(self):
        delay = max(0, int(self.speed_ms.get()))
        self.job_after = self.root.after(delay, self.processar_passo_bfs)

    def processar_passo_bfs(self):
        # caso sem elementos, terminar
        if not self.fila:
            self._finalizar_busca(encontrou=False)
            return

        r, c = self.fila.popleft()

        # pinta atual como visitado (exceto S/E)
        if (r, c) != self.inicio_pos and (r, c) != self.fim_pos:
            if self.labirinto[r][c] not in ("#",):
                self._paint_cell(r, c, COLOR_VISITED)

        # se chegamos no fim
        if (r, c) == self.fim_pos:
            self._finalizar_busca(encontrou=True)
            return

        # expande vizinhos
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                if self.labirinto[nr][nc] != "#" and (nr, nc) not in self.visitados:
                    self.visitados.add((nr, nc))
                    self.predecessores[(nr, nc)] = (r, c)
                    if (nr, nc) != self.fim_pos and self.labirinto[nr][nc] != "#":
                        self._paint_cell(nr, nc, COLOR_FRONTIER)
                    self.fila.append((nr, nc))

        self._schedule_next_step()

    def _finalizar_busca(self, encontrou: bool):
        self.encontrou = encontrou
        if self.job_after is not None:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None

        if encontrou:
            self.reconstruir_caminho()
        else:
            messagebox.showinfo("Resultado", "Caminho não encontrado.")

        self._set_mode("Modo Edição")
        self._enable_editing(True)

    # -----------------------------
    # Reconstrução do caminho final
    # -----------------------------
    def reconstruir_caminho(self):
        caminho = []
        cur = self.fim_pos
        while cur != self.inicio_pos:
            caminho.append(cur)
            cur = self.predecessores.get(cur)
            if cur is None:
                break
        for (r, c) in caminho:
            if (r, c) != self.inicio_pos and (r, c) != self.fim_pos:
                self._paint_cell(r, c, COLOR_SHORTEST)

    # -----------------------------
    # Reset e limpar
    # -----------------------------
    def resetar_busca(self, full_clear_colors=False):
        if self.job_after is not None:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None

        self.fila = None
        self.visitados = None
        self.predecessores = None
        self.encontrou = False

        # repinta todas as células conforme modelo
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                ch = self.labirinto[r][c]
                self._paint_cell(r, c, self._color_for_model(ch))

        self._set_mode("Modo Edição")
        self._enable_editing(True)

    def limpar_labirinto(self):
        if self.job_after is not None:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self.labirinto[r][c] = " "
                self._paint_cell(r, c, COLOR_PATH)

        self.inicio_pos = None
        self.fim_pos = None
        self.fila = None
        self.visitados = None
        self.predecessores = None
        self.encontrou = False

        self._set_mode("Modo Edição")
        self._enable_editing(True)

    # -----------------------------
    # Geração de labirinto aleatório (DFS aleatório)
    # -----------------------------
    def gerar_labirinto_aleatorio(self):
        # cancelar animação em curso e limpar buscas
        if self.job_after is not None:
            try:
                self.root.after_cancel(self.job_after)
            except Exception:
                pass
            self.job_after = None
        self._set_mode("Modo Edição")
        self._enable_editing(True)

        # 1) Começa com tudo parede
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self.labirinto[r][c] = "#"

        # garante contornos como parede
        def in_bounds(rr, cc):
            return 0 < rr < GRID_ROWS-1 and 0 < cc < GRID_COLS-1

        # lista de células "vivas" (ímpares) para o algoritmo
        odd_rows = list(range(1, GRID_ROWS-1, 2))
        odd_cols = list(range(1, GRID_COLS-1, 2))
        if not odd_rows or not odd_cols:
            # se a grade for muito pequena, apenas limpa (fallback)
            self.limpar_labirinto()
            return

        start_r = random.choice(odd_rows)
        start_c = random.choice(odd_cols)

        self.labirinto[start_r][start_c] = " "
        stack = [(start_r, start_c)]
        visited = {(start_r, start_c)}

        def odd_neighbors(rr, cc):
            for dr, dc in [(2,0),(-2,0),(0,2),(0,-2)]:
                nr, nc = rr + dr, cc + dc
                if in_bounds(nr, nc) and (nr, nc) not in visited:
                    yield (nr, nc, rr + dr//2, cc + dc//2)  # célula destino e parede entre elas

        while stack:
            cr, cc = stack[-1]
            neighs = list(odd_neighbors(cr, cc))
            if not neighs:
                stack.pop()
                continue
            nr, nc, wr, wc = random.choice(neighs)
            # abre parede entre (cr,cc) e (nr,nc)
            self.labirinto[wr][wc] = " "
            self.labirinto[nr][nc] = " "
            visited.add((nr, nc))
            stack.append((nr, nc))

        # 3) escolhe S e E em células de caminho
        self.inicio_pos = None
        self.fim_pos = None
        # S = primeira célula de caminho; E = última célula de caminho (varredura simples)
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if self.labirinto[r][c] == " ":
                    if self.inicio_pos is None:
                        self.inicio_pos = (r, c)
                    self.fim_pos = (r, c)
        # marca no modelo
        if self.inicio_pos:
            sr, sc = self.inicio_pos
            self.labirinto[sr][sc] = "S"
        if self.fim_pos:
            er, ec = self.fim_pos
            # se coincidir com S, tenta achar outro caminho
            if (er, ec) == self.inicio_pos:
                # acha alguma célula longe (procura reverso)
                for r in range(GRID_ROWS-1, -1, -1):
                    for c in range(GRID_COLS-1, -1, -1):
                        if self.labirinto[r][c] == " ":
                            self.fim_pos = (r, c)
                            er, ec = r, c
                            break
                    else:
                        continue
                    break
            self.labirinto[er][ec] = "E"

        # 4) repinta tudo
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self._paint_cell(r, c, self._color_for_model(self.labirinto[r][c]))

        # limpa estruturas de busca anteriores
        self.fila = None
        self.visitados = None
        self.predecessores = None
        self.encontrou = False


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeEditorGUI(root)
    root.mainloop()
