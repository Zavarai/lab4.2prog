import tkinter as tk
from tkinter import messagebox

from py_list import CircularList


lst_obj = CircularList()


def get_number():
    s = e1.get().strip().replace(",", ".")
    if s == "":
        raise ValueError("Введите число")
    return float(s)


def get_text():
    s = e2.get().strip()
    if s == "":
        raise ValueError("Введите строку")
    return s


def show_message(text):
    info.delete("1.0", "end")
    info.insert("1.0", text)


def refresh():
    data = lst_obj.get_all()
    lst.delete(0, "end")
    for i, item in enumerate(data, start=1):
        lst.insert("end", f"{i}. {item[0]} {item[1]}")

    canvas.delete("all")
    if not data:
        canvas.create_text(350, 90, text="Список пуст", font=("Arial", 16))
    else:
        x = 20
        for i, item in enumerate(data):
            canvas.create_rectangle(x, 50, x + 80, 100, fill="#eeeeee")
            text = f"{item[0]}\n{item[1]}"
            if i == 0:
                text = "HEAD\n" + text
            canvas.create_text(x + 40, 75, text=text)
            if i < len(data) - 1:
                canvas.create_line(x + 80, 75, x + 110, 75, arrow="last")
            x += 120
        canvas.create_line(x - 40, 100, x - 40, 140)
        canvas.create_line(x - 40, 140, 10, 140)
        canvas.create_line(10, 140, 10, 75)
        canvas.create_line(10, 75, 20, 75, arrow="last")

    show_message(lst_obj.last_message)


def safe_run(func):
    try:
        func()
        refresh()
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


def create_structure():
    lst_obj.create_structure()
    refresh()


def delete_structure():
    lst_obj.delete_structure()
    refresh()


def add_end():
    lst_obj.add_end(get_number(), get_text())
    refresh()


def add_beg():
    lst_obj.add_beg(get_number(), get_text())
    refresh()


def check_empty():
    if not lst_obj.is_created():
        show_message("Сначала создайте структуру.")
        return
    if lst_obj.is_empty():
        show_message("Список пуст")
    else:
        show_message("Список не пуст")


def show_count():
    if not lst_obj.is_created():
        show_message("Сначала создайте структуру.")
        return
    show_message(f"Количество: {lst_obj.count()}")


def find_two():
    lst_obj.search_two(get_number(), get_text())
    refresh()


def find_number():
    lst_obj.search_number(get_number())
    refresh()


def find_text():
    lst_obj.search_text(get_text())
    refresh()


def delete_one():
    lst_obj.delete_element(get_number(), get_text())
    refresh()


root = tk.Tk()
root.title("Лабораторная 4.2 Python")
root.geometry("800x600")

top = tk.Frame(root)
top.pack(pady=10)

tk.Label(top, text="Число").grid(row=0, column=0)
e1 = tk.Entry(top, width=12)
e1.grid(row=0, column=1, padx=5)

tk.Label(top, text="Строка").grid(row=0, column=2)
e2 = tk.Entry(top, width=12)
e2.grid(row=0, column=3, padx=5)

btns = tk.Frame(root)
btns.pack()

buttons = [
    ("Создать", create_structure),
    ("Удалить структуру", delete_structure),
    ("В конец", lambda: safe_run(add_end)),
    ("В начало", lambda: safe_run(add_beg)),
    ("Пусто?", check_empty),
    ("Количество", show_count),
    ("Поиск 2 поля", lambda: safe_run(find_two)),
    ("Поиск число", lambda: safe_run(find_number)),
    ("Поиск строка", lambda: safe_run(find_text)),
    ("Удалить", lambda: safe_run(delete_one)),
]

for i, (name, cmd) in enumerate(buttons):
    tk.Button(btns, text=name, width=14, command=cmd).grid(row=i // 5, column=i % 5, padx=4, pady=4)

lst = tk.Listbox(root, width=40, height=10)
lst.pack(pady=10)

canvas = tk.Canvas(root, width=700, height=180, bg="white")
canvas.pack()

info = tk.Text(root, height=8, width=70)
info.pack(pady=10)

refresh()
root.mainloop()

