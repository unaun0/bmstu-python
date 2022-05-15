import tkinter as tk
import tkinter.messagebox as mb


def add_point_with_button(): # Ввод координат x,y - добавлние точки
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
    except Exception:
        mb.showerror('Error', 'Некорректные координаты!')
        return None
    points.append((x, y))
    canvas.create_oval((x - 1, y - 1), (x + 1, y + 1))


def add_point_with_mouse(event): # Добавление точки с помощью ЛКМ
    x = event.x
    y = event.y
    points.append((x, y))
    canvas.create_oval((x - 1, y - 1), (x + 1, y + 1))


def find_equation(p1, p2): # Уравнение прямой
    if p1[0] == p2[0]:
        return None
    k = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - k * p1[0]
    return lambda x: k * x + b


def solve(): # Построение прямой
    if len(points) < 2:
        mb.showerror('Error', 'Невозможно построить прямую!')
        return None

    min_diff = float('+inf')
    result = None
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            curr_diff = 0
            p1 = points[i]
            p2 = points[j]
            if p1[0] == p2[0]:
                for point in points:
                    if point[1] < p1[0]:
                        curr_diff += 1
                    elif point[1] > p1[0]:
                        curr_diff -= 1
            else:
                equation = find_equation(p1, p2)
                for point in points:
                    y = equation(point[0])
                    if point[1] < y:
                        curr_diff += 1
                    elif point[1] > y:
                        curr_diff -= 1
            curr_diff = abs(curr_diff)
            if curr_diff < min_diff:
                result = (p1, p2)
                min_diff = curr_diff
    if not (last_number[-1] is None):
        canvas.delete(last_number[-1])
    last_number[-1] = canvas.create_line(*result)


points = []
last_number = [None]

WIDTH, HEIGHT = SIZE = (500, 500)

window = tk.Tk()

window.geometry(f'{WIDTH}x{HEIGHT}')
window.resizable(False, False)

label_x = tk.Label(window, text='x')
label_x.grid(row=0, column=0)

label_y = tk.Label(window, text='y')
label_y.grid(row=0, column=1)

entry_x = tk.Entry(window)
entry_x.grid(row=1, column=0)

entry_y = tk.Entry(window)
entry_y.grid(row=1, column=1)

button_solve = tk.Button(window, text='Решить', command=solve)
button_solve.grid(row=0, column=2)

button_add_point = tk.Button(window, text='Поставить точку', command=add_point_with_button)
button_add_point.grid(row=1, column=2)

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg='white')
canvas.grid(row=2, column=0, columnspan=3)
canvas.bind('<ButtonRelease-1>', add_point_with_mouse)

window.mainloop()
