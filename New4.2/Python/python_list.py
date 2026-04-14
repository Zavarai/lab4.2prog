class Node:
    # Узел циклического односвязного списка
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2
        self.next = None


class PythonListModule:
    # Простая реализация списка на Python
    def __init__(self):
        self.created = False
        self.head = None
        self.size = 0
        self.last_message = "Выбран Python модуль."

    def _find_last(self):
        # Поиск последнего элемента списка
        if self.head is None:
            return None
        current = self.head
        while current.next != self.head:
            current = current.next
        return current

    def create_structure(self):
        # Создание пустой структуры
        if self.created:
            self.last_message = "Структура уже создана."
            return False
        self.created = True
        self.head = None
        self.size = 0
        self.last_message = "Создан пустой циклический односвязный список."
        return True

    def delete_structure(self):
        # Полное удаление структуры
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        self.created = False
        self.head = None
        self.size = 0
        self.last_message = "Структура удалена."
        return True

    def add_end(self, value1, value2):
        # Добавление элемента в конец списка
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        new_node = Node(value1, value2)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            last = self._find_last()
            last.next = new_node
            new_node.next = self.head
        self.size += 1
        self.last_message = f"Добавлено в конец: {value1:g} {value2}"
        return True

    def add_beg(self, value1, value2):
        # Добавление элемента в начало списка
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        new_node = Node(value1, value2)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            last = self._find_last()
            new_node.next = self.head
            last.next = new_node
            self.head = new_node
        self.size += 1
        self.last_message = f"Добавлено в начало: {value1:g} {value2}"
        return True

    def read_elements(self):
        # Подготовка текста со всеми элементами
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        if self.head is None:
            self.last_message = "Список пуст."
            return True
        lines = ["Список элементов:"]
        current = self.head
        i = 1
        while True:
            lines.append(f"{i}. {current.data1:g} {current.data2}")
            current = current.next
            i += 1
            if current == self.head:
                break
        self.last_message = "\n".join(lines)
        return True

    def delete_element(self, value1, value2):
        # Удаление первого найденного элемента
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        if self.head is None:
            self.last_message = "Список пуст."
            return False

        current = self.head
        prev = self._find_last()
        while True:
            if current.data1 == value1 and current.data2 == value2:
                if current.next == current:
                    self.head = None
                else:
                    prev.next = current.next
                    if current == self.head:
                        self.head = current.next
                self.size -= 1
                self.last_message = "Элемент удален."
                return True
            prev = current
            current = current.next
            if current == self.head:
                break

        self.last_message = "Элемент не найден."
        return False

    def search_by_value(self, value1, value2):
        # Поиск по двум полям сразу
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        if self.head is None:
            self.last_message = "Список пуст."
            return False

        lines = []
        current = self.head
        while True:
            if current.data1 == value1 and current.data2 == value2:
                lines.append(f"{current.data1:g} {current.data2}")
            current = current.next
            if current == self.head:
                break

        if not lines:
            self.last_message = "Элемент не найден."
            return False
        self.last_message = "Результат поиска:\n" + "\n".join(lines)
        return True

    def search_by_first_value(self, value1):
        # Поиск по числовому полю
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        if self.head is None:
            self.last_message = "Список пуст."
            return False

        lines = []
        current = self.head
        while True:
            if current.data1 == value1:
                lines.append(f"{current.data1:g} {current.data2}")
            current = current.next
            if current == self.head:
                break

        if not lines:
            self.last_message = "Элементы не найдены."
            return False
        self.last_message = "Результат поиска:\n" + "\n".join(lines)
        return True

    def search_by_second_value(self, value2):
        # Поиск по строковому полю
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return False
        if self.head is None:
            self.last_message = "Список пуст."
            return False

        lines = []
        current = self.head
        while True:
            if current.data2 == value2:
                lines.append(f"{current.data1:g} {current.data2}")
            current = current.next
            if current == self.head:
                break

        if not lines:
            self.last_message = "Элементы не найдены."
            return False
        self.last_message = "Результат поиска:\n" + "\n".join(lines)
        return True

    def is_empty(self):
        if not self.created:
            return True
        return self.head is None

    def count(self):
        if not self.created:
            return 0
        return self.size

    def get_last_message(self):
        return self.last_message

    def get_elements(self):
        # Возврат списка элементов для GUI
        result = []
        if not self.created or self.head is None:
            return result
        current = self.head
        while True:
            result.append((current.data1, current.data2))
            current = current.next
            if current == self.head:
                break
        return result
