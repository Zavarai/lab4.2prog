class Node:
    def __init__(self, number, text):
        self.number = number
        self.text = text
        self.next = None


class CircularList:
    def __init__(self):
        self.head = None
        self.created = False
        self.last_message = ""

    def last_node(self):
        if self.head is None:
            return None
        p = self.head
        while p.next != self.head:
            p = p.next
        return p

    def create_structure(self):
        self.head = None
        self.created = True
        self.last_message = "Создан пустой список."

    def delete_structure(self):
        self.head = None
        self.created = False
        self.last_message = "Структура удалена."

    def is_created(self):
        return self.created

    def is_empty(self):
        if not self.created:
            return True
        return self.head is None

    def count(self):
        if not self.created or self.head is None:
            return 0
        k = 0
        p = self.head
        while True:
            k += 1
            p = p.next
            if p == self.head:
                break
        return k

    def add_end(self, number, text):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        p = Node(number, text)
        if self.head is None:
            self.head = p
            p.next = p
        else:
            last = self.last_node()
            last.next = p
            p.next = self.head
        self.last_message = "Добавлено в конец."

    def add_beg(self, number, text):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        p = Node(number, text)
        if self.head is None:
            self.head = p
            p.next = p
        else:
            last = self.last_node()
            p.next = self.head
            last.next = p
            self.head = p
        self.last_message = "Добавлено в начало."

    def delete_element(self, number, text):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        if self.head is None:
            self.last_message = "Список пуст."
            return
        prev = self.last_node()
        p = self.head
        while True:
            if p.number == number and p.text == text:
                if p.next == p:
                    self.head = None
                else:
                    prev.next = p.next
                    if p == self.head:
                        self.head = p.next
                self.last_message = "Элемент удален."
                return
            prev = p
            p = p.next
            if p == self.head:
                break
        self.last_message = "Элемент не найден."

    def search_two(self, number, text):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        if self.head is None:
            self.last_message = "Список пуст."
            return
        result = []
        p = self.head
        while True:
            if p.number == number and p.text == text:
                result.append(f"{p.number} {p.text}")
            p = p.next
            if p == self.head:
                break
        self.last_message = "\n".join(result) if result else "Элемент не найден."

    def search_number(self, number):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        if self.head is None:
            self.last_message = "Список пуст."
            return
        result = []
        p = self.head
        while True:
            if p.number == number:
                result.append(f"{p.number} {p.text}")
            p = p.next
            if p == self.head:
                break
        self.last_message = "\n".join(result) if result else "Элементы не найдены."

    def search_text(self, text):
        if not self.created:
            self.last_message = "Сначала создайте структуру."
            return
        if self.head is None:
            self.last_message = "Список пуст."
            return
        result = []
        p = self.head
        while True:
            if p.text == text:
                result.append(f"{p.number} {p.text}")
            p = p.next
            if p == self.head:
                break
        self.last_message = "\n".join(result) if result else "Элементы не найдены."

    def get_all(self):
        result = []
        if not self.created or self.head is None:
            return result
        p = self.head
        while True:
            result.append((p.number, p.text))
            p = p.next
            if p == self.head:
                break
        return result

