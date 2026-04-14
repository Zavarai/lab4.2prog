import tkinter as tk
from tkinter import messagebox

from python_list import PythonListModule


class AppPython:
    # Отдельное решение только на Python
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 4.2 - Python")
        self.root.geometry("950x650")

        self.current = PythonListModule()

        self.build_ui()
        self.refresh_all()

    def build_ui(self):
        top = tk.Frame(self.root, padx=10, pady=10)
        top.pack(fill="x")

        tk.Label(top, text="Решение: Python").grid(row=0, column=0, sticky="w")

        tk.Label(top, text="Число:").grid(row=0, column=1, padx=(15, 5))
        self.entry_number = tk.Entry(top, width=15)
        self.entry_number.grid(row=0, column=2)

        tk.Label(top, text="Строка:").grid(row=0, column=3, padx=(15, 5))
        self.entry_text = tk.Entry(top, width=15)
        self.entry_text.grid(row=0, column=4)

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
            text=f"Текущее решение: Python    Количество элементов: {self.current.count()}    Пустой список: {'да' if self.current.is_empty() else 'нет'}"
        )
        self.show_message(self.current.get_last_message())
        self.draw_list(elements)

    def draw_list(self, elements):
        # Простая отрисовка списка на canvas
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
            text = f"{value1:g}\n{value2}"
            if i == 0:
                text = "HEAD\n" + text
            self.canvas.create_text(x + width / 2, y + height / 2, text=text)

            if i < len(elements) - 1:
                next_x, next_y = positions[i + 1]
                self.canvas.create_line(x + width, y + height / 2, next_x, next_y + height / 2, arrow="last")
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
    AppPython(root)
    root.mainloop()


if __name__ == "__main__":
    main()

