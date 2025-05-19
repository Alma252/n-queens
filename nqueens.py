import tkinter as tk
import random

# ----------------------------
# الگوریتم Backtracking
# ----------------------------
def solve_n_queens_backtracking(n):
    solution = []
    columns = set()
    diag1 = set()
    diag2 = set()
    board = [0] * n

    def backtrack(row):
        if row == n:
            solution.extend(board[:])
            return True
        for col in range(n):
            if col not in columns and (row - col) not in diag1 and (row + col) not in diag2:
                columns.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                board[row] = col + 1
                if backtrack(row + 1):
                    return True
                columns.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
        return False

    backtrack(0)
    return solution

# ----------------------------
# الگوریتم Genetic
# ----------------------------
def solve_n_queens_genetic(n, population_size=100, max_generations=1000):
    def fitness(chrom):
        score = 0
        for i in range(n):
            for j in range(i + 1, n):
                if chrom[i] != chrom[j] and abs(chrom[i] - chrom[j]) != abs(i - j):
                    score += 1
        return score

    population = [[random.randint(1, n) for _ in range(n)] for _ in range(population_size)]
    best_chrom = None
    best_score = -1
    total_pairs = n * (n - 1) // 2

    for generation in range(max_generations):
        scored_pop = [(fitness(chrom), chrom) for chrom in population]
        scored_pop.sort(reverse=True, key=lambda x: x[0])
        if scored_pop[0][0] == total_pairs:
            return scored_pop[0][1]
        if scored_pop[0][0] > best_score:
            best_score = scored_pop[0][0]
            best_chrom = scored_pop[0][1]
        cutoff = population_size // 5
        population = [chrom for _, chrom in scored_pop[:cutoff]]
        while len(population) < population_size:
            p1 = random.choice(population)
            p2 = random.choice(population)
            idx = random.randint(0, n - 1)
            child = p1[:idx] + p2[idx:]
            if random.random() < 0.1:
                pos = random.randint(0, n - 1)
                child[pos] = random.randint(1, n)
            population.append(child)
    return best_chrom if best_chrom else population[0]

# ----------------------------
# رابط گرافیکی با Tkinter
# ----------------------------
class NQueensGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("حل‌گر n-Queens")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.n_label = tk.Label(self.frame, text="تعداد وزیرها (N):")
        self.n_label.pack(side=tk.LEFT)
        self.n_entry = tk.Entry(self.frame, width=5)
        self.n_entry.pack(side=tk.LEFT)
        self.n_entry.insert(0, "8")

        self.solve_back_btn = tk.Button(self.frame, text="Backtracking Algoritm", command=self.solve_backtracking)
        self.solve_back_btn.pack(side=tk.LEFT)
        self.solve_gen_btn = tk.Button(self.frame, text="Genetic Algorithm ", command=self.solve_genetic)
        self.solve_gen_btn.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.cell_size = 40
        self.delay = 500

    def draw_board(self, n):
        self.canvas.delete("all")
        size = self.cell_size * n
        self.canvas.config(width=size, height=size)
        for i in range(n):
            for j in range(n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def place_queens(self, positions):
        for col, row in enumerate(positions):
            x = col * self.cell_size + self.cell_size / 2
            y = (row - 1) * self.cell_size + self.cell_size / 2
            self.canvas.after(self.delay * col,
                              lambda x=x, y=y: self.canvas.create_text(
                                  x, y, text="♛", font=("Arial", 24), fill="red"))

    def solve_backtracking(self):
        n = int(self.n_entry.get())
        self.draw_board(n)
        solution = solve_n_queens_backtracking(n)
        self.place_queens(solution)

    def solve_genetic(self):
        n = int(self.n_entry.get())
        self.draw_board(n)
        solution = solve_n_queens_genetic(n)
        self.place_queens(solution)

# ----------------------------
# اجرای برنامه
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
