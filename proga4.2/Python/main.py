import ctypes
import tkinter as tk
from tkinter import messagebox

from build_dll import main as build_dll


build_dll()

DLL = ctypes.CDLL(r"..\C\build\list.dll")

DLL.create_structure.argtypes = []
DLL.create_structure.restype = ctypes.c_int
DLL.delete_structure.argtypes = []
DLL.delete_structure.restype = ctypes.c_int
DLL.add_end.argtypes = [ctypes.c_double, ctypes.c_char_p]
DLL.add_end.restype = ctypes.c_int
DLL.add_beg.argtypes = [ctypes.c_double, ctypes.c_char_p]
DLL.add_beg.restype = ctypes.c_int
DLL.is_empty.argtypes = []
DLL.is_empty.restype = ctypes.c_int
DLL.count.argtypes = []
DLL.count.restype = ctypes.c_int
DLL.delete_element.argtypes = [ctypes.c_double, ctypes.c_char_p]
DLL.delete_element.restype = ctypes.c_int
DLL.search_by_value.argtypes = [ctypes.c_double, ctypes.c_char_p]
DLL.search_by_value.restype = ctypes.c_int
DLL.search_by_first_value.argtypes = [ctypes.c_double]
DLL.search_by_first_value.restype = ctypes.c_int
DLL.search_by_second_value.argtypes = [ctypes.c_char_p]
DLL.search_by_second_value.restype = ctypes.c_int
DLL.get_last_message.argtypes = []
DLL.get_last_message.restype = ctypes.c_char_p
DLL.get_element_at.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_int]
DLL.get_element_at.restype = ctypes.c_int


def msg():
    value = DLL.get_last_message()
    if not value:
        return ""
    return value.decode("utf-8", errors="replace")


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


def get_all():
    result = []
    total = DLL.count()
    for i in range(total):
        number = ctypes.c_double()
        text = ctypes.create_string_buffer(100)
        ok = DLL.get_element_at(i, ctypes.byref(number), text, 100)
        if ok:
            result.append((number.value, text.value.decode("utf-8", errors="replace")))
    return result


def refresh():
    data = get_all()
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

    show_message(msg())


def safe_run(func):
    try:
        func()
        refresh()
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


def create_structure():
    DLL.create_structure()
    refresh()


def delete_structure():
    DLL.delete_structure()
    refresh()


def add_end():
    DLL.add_end(get_number(), get_text().encode("utf-8"))
    refresh()


def add_beg():
    DLL.add_beg(get_number(), get_text().encode("utf-8"))
    refresh()


def check_empty():
    if DLL.is_empty():
        show_message("Список пуст")
    else:
        show_message("Список не пуст")


def show_count():
    show_message(f"Количество: {DLL.count()}")


def find_two():
    DLL.search_by_value(get_number(), get_text().encode("utf-8"))
    refresh()


def find_number():
    DLL.search_by_first_value(get_number())
    refresh()


def find_text():
    DLL.search_by_second_value(get_text().encode("utf-8"))
    refresh()


def delete_one():
    DLL.delete_element(get_number(), get_text().encode("utf-8"))
    refresh()


root = tk.Tk()
root.title("Лабораторная 4.2 DLL")
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
    ("Удалить список", delete_structure),
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

