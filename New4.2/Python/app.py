import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from build_cpp import main as build_cpp_modules
from python_list import PythonListModule


BASE_DIR = Path(__file__).resolve().parent
C_DIR = BASE_DIR.parent / "C"
BUILD_DIR = C_DIR / "build"
DYNAMIC_DLL = BUILD_DIR / "list_dynamic.dll"
STL_DLL = BUILD_DIR / "list_stl.dll"


class CppListModule:
    def __init__(self, dll_path):
        self.lib = ctypes.CDLL(str(dll_path))
        self.lib.create_structure.argtypes = []
        self.lib.create_structure.restype = ctypes.c_int
        self.lib.delete_structure.argtypes = []
        self.lib.delete_structure.restype = ctypes.c_int
        self.lib.add_end.argtypes = [ctypes.c_double, ctypes.c_char_p]
        self.lib.add_end.restype = ctypes.c_int
        self.lib.add_beg.argtypes = [ctypes.c_double, ctypes.c_char_p]
        self.lib.add_beg.restype = ctypes.c_int
        self.lib.read_elements.argtypes = []
        self.lib.read_elements.restype = ctypes.c_int
        self.lib.delete_element.argtypes = [ctypes.c_double, ctypes.c_char_p]
        self.lib.delete_element.restype = ctypes.c_int
        self.lib.search_by_value.argtypes = [ctypes.c_double, ctypes.c_char_p]
        self.lib.search_by_value.restype = ctypes.c_int
        self.lib.search_by_first_value.argtypes = [ctypes.c_double]
        self.lib.search_by_first_value.restype = ctypes.c_int
        self.lib.search_by_second_value.argtypes = [ctypes.c_char_p]
        self.lib.search_by_second_value.restype = ctypes.c_int
        self.lib.is_created.argtypes = []
        self.lib.is_created.restype = ctypes.c_int
        self.lib.is_empty.argtypes = []
        self.lib.is_empty.restype = ctypes.c_int
        self.lib.count.argtypes = []
        self.lib.count.restype = ctypes.c_int
        self.lib.get_last_message.argtypes = []
        self.lib.get_last_message.restype = ctypes.c_char_p
        self.lib.get_element_at.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_int]
        self.lib.get_element_at.restype = ctypes.c_int

    def create_structure(self):
        return bool(self.lib.create_structure())

    def delete_structure(self):
        return bool(self.lib.delete_structure())

    def add_end(self, value1, value2):
        return bool(self.lib.add_end(value1, value2.encode("utf-8")))

    def add_beg(self, value1, value2):
        return bool(self.lib.add_beg(value1, value2.encode("utf-8")))

    def read_elements(self):
        return bool(self.lib.read_elements())

    def delete_element(self, value1, value2):
        return bool(self.lib.delete_element(value1, value2.encode("utf-8")))

    def search_by_value(self, value1, value2):
        return bool(self.lib.search_by_value(value1, value2.encode("utf-8")))

    def search_by_first_value(self, value1):
        return bool(self.lib.search_by_first_value(value1))

    def search_by_second_value(self, value2):
        return bool(self.lib.search_by_second_value(value2.encode("utf-8")))

    def is_empty(self):
        return bool(self.lib.is_empty())

    def count(self):
        return self.lib.count()

    def get_last_message(self):
        value = self.lib.get_last_message()
        if not value:
            return ""
        return value.decode("utf-8", errors="replace")

    def get_elements(self):
        result = []
        total = self.count()
        for i in range(total):
            value1 = ctypes.c_double()
            value2 = ctypes.create_string_buffer(100)
            ok = self.lib.get_element_at(i, ctypes.byref(value1), value2, 100)
            if ok:
                result.append((value1.value, value2.value.decode("utf-8", errors="replace")))
        return result


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 4.2")
        self.root.geometry("950x650")

        build_cpp_modules()

        self.backends = {
            "Python": PythonListModule(),
            "C++ dynamic": CppListModule(DYNAMIC_DLL),
            "C++ STL": CppListModule(STL_DLL),
        }

        self.backend_name = tk.StringVar(value="Python")
        self.current = self.backends["Python"]

        self.build_ui()
        self.refresh_all()

    def build_ui(self):
        top = tk.Frame(self.root, padx=10, pady=10)
        top.pack(fill="x")

        tk.Label(top, text="Модуль:").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(top, self.backend_name, *self.backends.keys(), command=self.change_backend).grid(row=0, column=1, sticky="w")

        tk.Label(top, text="Число:").grid(row=0, column=2, padx=(15, 5))
        self.entry_number = tk.Entry(top, width=15)
        self.entry_number.grid(row=0, column=3)

        tk.Label(top, text="Строка:").grid(row=0, column=4, padx=(15, 5))
        self.entry_text = tk.Entry(top, width=15)
        self.entry_text.grid(row=0, column=5)

        buttons = tk.Frame(self.root, padx=10)
        buttons.pack(fill="x")

        button_list = [
            ("Создать", self.create_structure),
            ("Удалить", self.delete_structure),
            ("В конец", self.add_end),
            ("В начало", self.add_beg),
            ("Показать", self.read_elements),
            ("Пусто?", self.check_empty),
            ("Количество", self.show_count),
            ("Поиск 2 поля", self.search_two),
            ("Поиск число", self.search_number),
            ("Поиск строка", self.search_text),
            ("Удалить элемент", self.delete_one),
        ]

        for i, (text, command) in enumerate(button_list):
            tk.Button(buttons, text=text, width=16, command=command).grid(row=i // 4, column=i % 4, padx=4, pady=4, sticky="ew")

        middle = tk.Frame(self.root, padx=10, pady=10)
        middle.pack(fill="both", expand=True)

        left = tk.Frame(middle)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Элементы списка").pack(anchor="w")
        self.listbox = tk.Listbox(left, height=15, width=40)
        self.listbox.pack(fill="both", expand=True)

        right = tk.Frame(middle)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="Визуализация").pack(anchor="w")
        self.canvas = tk.Canvas(right, bg="white", width=420, height=320)
        self.canvas.pack(fill="both", expand=True)

        bottom = tk.Frame(self.root, padx=10, pady=10)
        bottom.pack(fill="both")

        self.info_label = tk.Label(bottom, text="", anchor="w", justify="left")
        self.info_label.pack(fill="x")

        tk.Label(bottom, text="Сообщение").pack(anchor="w")
        self.message_box = tk.Text(bottom, height=8, wrap="word")
        self.message_box.pack(fill="both", expand=True)
        self.message_box.configure(state="disabled")

    def change_backend(self, value):
        self.current = self.backends[value]
        self.refresh_all()

    def get_number(self):
        text = self.entry_number.get().strip().replace(",", ".")
        if text == "":
            raise ValueError("Введите число.")
        return float(text)

    def get_text(self):
        text = self.entry_text.get().strip()
        if text == "":
            raise ValueError("Введите строку.")
        return text

    def show_message(self, text):
        self.message_box.configure(state="normal")
        self.message_box.delete("1.0", "end")
        self.message_box.insert("1.0", text)
        self.message_box.configure(state="disabled")

    def refresh_all(self):
        self.listbox.delete(0, "end")
        elements = self.current.get_elements()
        for i, (value1, value2) in enumerate(elements, start=1):
            self.listbox.insert("end", f"{i}. {value1:g} {value2}")

        self.info_label.config(
            text=f"Текущий модуль: {self.backend_name.get()}    Количество элементов: {self.current.count()}    Пустой список: {'да' if self.current.is_empty() else 'нет'}"
        )
        self.show_message(self.current.get_last_message())
        self.draw_list(elements)

    def draw_list(self, elements):
        self.canvas.delete("all")
        if not elements:
            self.canvas.create_text(200, 150, text="Список пуст", font=("Arial", 16))
            return

        width = 90
        height = 45
        step_x = 130
        step_y = 120
        start_x = 20
        start_y = 60
        max_in_row = 3
        positions = []

        for i in range(len(elements)):
            row = i // max_in_row
            col = i % max_in_row
            x = start_x + col * step_x
            y = start_y + row * step_y
            positions.append((x, y))

        for i, (value1, value2) in enumerate(elements):
            x, y = positions[i]
            color = "#d9edf7" if i == 0 else "#f5f5f5"
            self.canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="black")
            label = f"{value1:g}\n{value2}"
            if i == 0:
                label = "HEAD\n" + label
            self.canvas.create_text(x + width / 2, y + height / 2, text=label)

            if i < len(elements) - 1:
                next_x, next_y = positions[i + 1]
                self.canvas.create_line(
                    x + width,
                    y + height / 2,
                    next_x,
                    next_y + height / 2,
                    arrow="last"
                )
            else:
                first_x, first_y = positions[0]
                self.canvas.create_line(x + width / 2, y + height, x + width / 2, y + 80)
                self.canvas.create_line(x + width / 2, y + 80, first_x - 10, y + 80)
                self.canvas.create_line(first_x - 10, y + 80, first_x - 10, first_y + height / 2)
                self.canvas.create_line(first_x - 10, first_y + height / 2, first_x, first_y + height / 2, arrow="last")

    def run_action(self, func, need_number=False, need_text=False):
        try:
            number = self.get_number() if need_number else None
            text = self.get_text() if need_text else None

            if need_number and need_text:
                func(number, text)
            elif need_number:
                func(number)
            elif need_text:
                func(text)
            else:
                func()

            self.refresh_all()
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def create_structure(self):
        self.current.create_structure()
        self.refresh_all()

    def delete_structure(self):
        self.current.delete_structure()
        self.refresh_all()

    def add_end(self):
        self.run_action(self.current.add_end, True, True)

    def add_beg(self):
        self.run_action(self.current.add_beg, True, True)

    def read_elements(self):
        self.current.read_elements()
        self.refresh_all()

    def check_empty(self):
        if self.current.is_empty():
            self.show_message("Список пуст или еще не создан.")
        else:
            self.show_message("Список не пуст.")
        self.refresh_all()

    def show_count(self):
        self.show_message(f"Количество элементов: {self.current.count()}")
        self.refresh_all()

    def search_two(self):
        self.run_action(self.current.search_by_value, True, True)

    def search_number(self):
        self.run_action(self.current.search_by_first_value, True, False)

    def search_text(self):
        self.run_action(self.current.search_by_second_value, False, True)

    def delete_one(self):
        self.run_action(self.current.delete_element, True, True)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
