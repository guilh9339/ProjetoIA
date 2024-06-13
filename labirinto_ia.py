import tkinter as tk
from tkinter import Label
from collections import deque
import random

class LabirintoIAApp:
    def __init__(self, root, linhas, colunas, inicio, fim):
        self.root = root
        self.root.title("Labirinto IA")
        self.linhas = linhas
        self.colunas = colunas
        self.inicio = inicio
        self.fim = fim
        self.tamanho_celula = 30
        self.canvas = tk.Canvas(root, width=self.colunas * self.tamanho_celula, height=self.linhas * self.tamanho_celula)
        self.canvas.pack()
        self.btn_gerar = tk.Button(root, text="Gerar Labirinto", command=self.gerar_labirinto)
        self.btn_gerar.pack(side=tk.LEFT, padx=10)
        self.btn_resolver = tk.Button(root, text="Iniciar Busca", command=self.resolver_labirinto)
        self.btn_resolver.pack(side=tk.LEFT, padx=10)
        self.lbl_custo = Label(root, text="Custo: 0")
        self.lbl_custo.pack(side=tk.LEFT, padx=10)
        self.labirinto = [[0] * colunas for _ in range(linhas)]
        self.num_obstaculos = 64
        self.custos = {}  # Dicionário para armazenar os custos

        self.gerar_labirinto()

    def gerar_labirinto(self):
        self.labirinto = [[0] * self.colunas for _ in range(self.linhas)]

        obstaculos_colocados = 0
        while obstaculos_colocados < self.num_obstaculos:
            r = random.randint(0, self.linhas - 1)
            c = random.randint(0, self.colunas - 1)
            if self.labirinto[r][c] == 0 and not self.eh_vizinho_proximo((r, c), self.inicio) and not self.eh_vizinho_proximo((r, c), self.fim):
                self.labirinto[r][c] = 1
                obstaculos_colocados += 1

        self.labirinto[self.inicio[0]][self.inicio[1]] = 0
        self.labirinto[self.fim[0]][self.fim[1]] = 0

        self.desenhar_labirinto()

    def desenhar_labirinto(self):
        self.canvas.delete("all")
        for r in range(self.linhas):
            for c in range(self.colunas):
                cor = 'white'
                if self.labirinto[r][c] == 1:
                    cor = '#333333'
                elif (r, c) == self.inicio:
                    cor = 'green'
                elif (r, c) == self.fim:
                    cor = 'red'
                self.canvas.create_rectangle(c * self.tamanho_celula, r * self.tamanho_celula,
                                             (c + 1) * self.tamanho_celula, (r + 1) * self.tamanho_celula, fill=cor)

    def resolver_labirinto(self):
        self.btn_gerar.config(state=tk.DISABLED)

        caminho, custo_total = self.busca_em_largura(self.inicio, self.fim)
        if caminho:
            self.animar_caminho(caminho)
            self.lbl_custo.config(text=f"Custo: {custo_total}")
        else:
            print("Nenhum caminho encontrado.")

        self.btn_gerar.config(state=tk.NORMAL)

    def animar_caminho(self, caminho):
        custo_total = 0
        for i in range(len(caminho) - 1):
            r, c = caminho[i]
            nr, nc = caminho[i + 1]
            self.canvas.create_line(c * self.tamanho_celula + self.tamanho_celula // 2, r * self.tamanho_celula + self.tamanho_celula // 2,
                                    nc * self.tamanho_celula + self.tamanho_celula // 2, nr * self.tamanho_celula + self.tamanho_celula // 2,
                                    fill='blue', width=5)
            self.root.update()
            self.root.after(100)
            custo_total += self.custos.get((nr, nc), 1)  # Somando o custo da célula ao custo total

        self.lbl_custo.config(text=f"Custo: {custo_total}")

    def busca_em_largura(self, inicio, fim):
        fila = deque([(inicio, [inicio])])
        visitados = set()
        visitados.add(inicio)
        self.custos[inicio] = 0  # Custo inicial é zero
        while fila:
            (atual, caminho) = fila.popleft()
            (linha, coluna) = atual
            if atual == fim:
                return caminho, self.custos[atual]  # Retorna o caminho e o custo total
            for dl, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nl, nc = linha + dl, coluna + dc
                if 0 <= nl < self.linhas and 0 <= nc < self.colunas and self.labirinto[nl][nc] == 0 and (nl, nc) not in visitados:
                    visitados.add((nl, nc))
                    fila.append(((nl, nc), caminho + [(nl, nc)]))
                    self.custos[(nl, nc)] = self.custos[(linha, coluna)] + 1  # Atualiza o custo da célula

        return None, None

    def eh_vizinho_proximo(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

if __name__ == "__main__":
    linhas = 15
    colunas = 15
    inicio = (0, 0)
    fim = (linhas - 1, colunas - 1)
    
    root = tk.Tk()
    app = LabirintoIAApp(root, linhas, colunas, inicio, fim)
    root.mainloop()
