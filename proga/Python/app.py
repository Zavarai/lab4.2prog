# Главное окно программы на tkinter.
# Этот файл запускается первым: он рисует кнопки, поля ввода и список на экране.
# Сама структура данных находится не здесь, а в отдельных модулях.

import importlib  # нужен, чтобы подключать модуль по имени
import sys  # нужен, чтобы читать аргументы запуска из командной строки
import tkinter as tk  # библиотека для обычного оконного интерфейса
from tkinter import messagebox  # готовые окна с сообщениями об ошибках и результатах

# Подключаем Python-реализацию списка заранее.
# Если пользователь выберет C++ вариант, ниже подключится другой модуль.
list_module = importlib.import_module("list_module")


class App:
    """Класс всего окна программы."""

    def __init__(self, root, start_module="Python"):
        # root — это главное окно tkinter.
        self.root = root
        self.root.title("Циклический односвязный список")
        self.root.geometry("760x520")

        # Здесь запоминаем, какую реализацию списка надо использовать:
        # Python, C++ dynamic или C++ STL.
        self.module_name = start_module
        self.data_list = self.load_module(start_module)

        # Рамка для полей ввода числа и строки.
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        # Поле для первого значения элемента списка: число double/float.
        tk.Label(input_frame, text="Число:").grid(row=0, column=0, padx=5)
        self.number_entry = tk.Entry(input_frame, width=15)
        self.number_entry.grid(row=0, column=1, padx=5)

        # Поле для второго значения элемента списка: строка.
        tk.Label(input_frame, text="Строка:").grid(row=0, column=2, padx=5)
        self.text_entry = tk.Entry(input_frame, width=20)
        self.text_entry.grid(row=0, column=3, padx=5)

        # Рамка для кнопок действий со списком.
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        # Каждая кнопка вызывает свой метод этого класса.
        tk.Button(
            button_frame, text="Создать список", width=20, command=self.create_structure
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(
            button_frame, text="Удалить список", width=20, command=self.delete_structure
        ).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            button_frame, text="Добавить в конец", width=20, command=self.add_end
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            button_frame, text="Добавить в начало", width=20, command=self.add_beg
        ).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(
            button_frame, text="Удалить элемент", width=20, command=self.delete_element
        ).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(
            button_frame, text="Количество", width=20, command=self.show_count
        ).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(
            button_frame, text="Проверить пустоту", width=20, command=self.check_empty
        ).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(
            button_frame,
            text="Поиск по двум полям",
            width=20,
            command=self.search_by_value,
        ).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(
            button_frame,
            text="Поиск по числу",
            width=20,
            command=self.search_by_first_value,
        ).grid(row=2, column=2, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Поиск по строке",
            width=20,
            command=self.search_by_second_value,
        ).grid(row=3, column=0, padx=5, pady=5)
        # Кнопку "Показать все" убрали: список и так обновляется автоматически
        # после создания, удаления и добавления элементов.
        tk.Button(button_frame, text="Выход", width=20, command=root.destroy).grid(
            row=3, column=1, padx=5, pady=5
        )

        # Listbox — это большая область, где видны все элементы списка.
        tk.Label(root, text="Элементы списка:").pack()
        self.listbox = tk.Listbox(root, width=80, height=12)
        self.listbox.pack(pady=5)

        # Строка состояния внизу окна.
        self.status_label = tk.Label(
            root,
            text=f"Реализация: {self.module_name}. Список пока не создан",
            fg="blue",
        )
        self.status_label.pack(pady=5)

    def get_input(self, need_number=True, need_text=True):
        """Получить число и/или строку из полей ввода."""
        number = None
        text = None

        # Если методу нужно число, пробуем перевести текст из поля в float.
        if need_number:
            try:
                number = float(self.number_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Введите правильное число")
                return None

        # Если методу нужна строка, проверяем, что она не пустая.
        if need_text:
            text = self.text_entry.get().strip()
            if text == "":
                messagebox.showerror("Ошибка", "Введите строку")
                return None

        return number, text

    def show_message(self, success, text):
        """Показать сообщение пользователю."""
        # Сначала меняем нижнюю строку состояния.
        self.status_label.config(text=text)

        # Потом показываем отдельное окно: info при успехе, warning при проблеме.
        if success:
            messagebox.showinfo("Сообщение", text)
        else:
            messagebox.showwarning("Внимание", text)

    def load_module(self, selected):
        """Загрузить нужную реализацию списка."""
        try:
            # У всех модулей одинаковые функции, поэтому GUI может работать с ними одинаково.
            if selected == "Python":
                return list_module
            if selected == "C++ dynamic":
                return importlib.import_module("cpp_dynamic_module")
            if selected == "C++ STL":
                return importlib.import_module("cpp_stl_module")
        except FileNotFoundError as error:
            messagebox.showwarning("DLL не найдена", str(error))
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось подключить модуль: {error}")

        # Если C++ модуль не загрузился, безопасно возвращаем Python-вариант.
        self.module_name = "Python"
        return list_module

    def create_structure(self):
        """Создать пустой список."""
        success, text = self.data_list.create_structure()
        self.show_message(success, text)
        if success:
            self.update_view()

    def delete_structure(self):
        """Удалить весь список."""
        success, text = self.data_list.delete_structure()
        self.show_message(success, text)
        if success:
            self.update_view()

    def add_end(self):
        """Добавить новый элемент в конец списка."""
        values = self.get_input()
        if values is None:
            return

        success, text = self.data_list.add_end(values[0], values[1])
        self.show_message(success, text)
        if success:
            self.update_view()

    def add_beg(self):
        """Добавить новый элемент в начало списка."""
        values = self.get_input()
        if values is None:
            return

        success, text = self.data_list.add_beg(values[0], values[1])
        self.show_message(success, text)
        if success:
            self.update_view()

    def delete_element(self):
        """Удалить элемент, совпадающий по числу и строке."""
        values = self.get_input()
        if values is None:
            return

        success, text = self.data_list.delete_element(values[0], values[1])
        self.show_message(success, text)
        if success:
            self.update_view()

    def show_count(self):
        """Показать количество элементов."""
        if not self.data_list.is_created():
            messagebox.showwarning("Внимание", "Списка нет, сначала создайте его")
            return

        messagebox.showinfo(
            "Количество", f"Количество элементов: {self.data_list.count()}"
        )

    def check_empty(self):
        """Проверить, пустой список или нет."""
        if not self.data_list.is_created():
            messagebox.showwarning("Внимание", "Списка нет, сначала создайте его")
            return

        if self.data_list.is_empty():
            messagebox.showinfo("Проверка", "Список пуст")
        else:
            messagebox.showinfo("Проверка", "Список не пуст")

    def search_by_value(self):
        """Найти элементы, где совпали и число, и строка."""
        values = self.get_input()
        if values is None:
            return

        result = self.data_list.search_by_value(values[0], values[1])
        self.show_search_result(result)

    def search_by_first_value(self):
        """Найти элементы только по числу."""
        values = self.get_input(need_text=False)
        if values is None:
            return

        result = self.data_list.search_by_first_value(values[0])
        self.show_search_result(result)

    def search_by_second_value(self):
        """Найти элементы только по строке."""
        values = self.get_input(need_number=False)
        if values is None:
            return

        result = self.data_list.search_by_second_value(values[1])
        self.show_search_result(result)

    def show_search_result(self, result):
        """Показать результат поиска в отдельном окне."""
        if not self.data_list.is_created():
            messagebox.showwarning("Внимание", "Списка нет, сначала создайте его")
            return

        if len(result) == 0:
            messagebox.showinfo("Поиск", "Ничего не найдено")
            return

        text = "Найдено:\n"
        for item in result:
            text += f"{item[0]} | {item[1]}\n"

        messagebox.showinfo("Поиск", text)

    def update_view(self):
        """Обновить Listbox, то есть заново вывести все элементы списка."""
        # Сначала очищаем старый вывод.
        self.listbox.delete(0, tk.END)

        # Потом берём элементы из выбранного модуля и вставляем их в окно.
        elements = self.data_list.get_elements()
        for index, item in enumerate(elements, start=1):
            self.listbox.insert(
                tk.END, f"{index}. Число: {item[0]}    Строка: {item[1]}"
            )

        self.status_label.config(text=f"Элементов в списке: {len(elements)}")


if __name__ == "__main__":
    # Этот блок выполняется только при прямом запуске файла app.py.
    # Примеры запуска из папки Python:
    # python app.py
    # python app.py python
    # python app.py dynamic
    # python app.py stl
    selected_module = "Python"

    # Если после имени файла передали слово dynamic или stl,
    # выбираем соответствующую C++ реализацию.
    if len(sys.argv) > 1:
        argument = sys.argv[1].lower()
        if argument == "dynamic":
            selected_module = "C++ dynamic"
        elif argument == "stl":
            selected_module = "C++ STL"
        else:
            selected_module = "Python"

    # Создаём окно и запускаем бесконечный цикл обработки кнопок.
    window = tk.Tk()
    app = App(window, selected_module)
    window.mainloop()
