# Модуль со структурой данных на Python.
# Здесь нет кнопок и окон, тут только функции для работы со списком.
# app.py вызывает эти функции, когда пользователь нажимает кнопки.


class Node:
    """Один элемент циклического односвязного списка."""

    def __init__(self, data1, data2):
        # data1 — первое поле элемента, число.
        self.data1 = data1
        # data2 — второе поле элемента, строка.
        self.data2 = data2
        # next — ссылка на следующий элемент списка.
        # В циклическом списке последний элемент ссылается обратно на первый.
        self.next = None


# head хранит ссылку на первый элемент списка.
# Если head равен None, значит элементов сейчас нет.
head = None

# created показывает, создана ли структура.
# Это нужно, чтобы отличать ситуацию "список не создан" от "список создан, но пустой".
created = False


def create_structure():
    """Создать пустой список."""
    global head, created

    # Нельзя создавать список второй раз, пока старый не удалили.
    if created:
        return False, "Список уже создан"

    # Новый список сначала пустой, поэтому head = None.
    head = None
    created = True
    return True, "Создан пустой циклический список"


def delete_structure():
    """Удалить весь список."""
    global head, created

    if not created:
        return False, "Списка нет, сначала создайте его"

    # В Python достаточно убрать ссылку на голову,
    # а память потом очистит сборщик мусора.
    head = None
    created = False
    return True, "Список удалён"


def is_created():
    """Проверить, создан ли список."""
    return created


def is_empty():
    """Проверить, пустой ли список."""
    return head is None


def add_end(data1, data2):
    """Добавить элемент в конец списка."""
    global head

    if not created:
        return False, "Списка нет, сначала создайте его"

    # Создаём новый узел с числом и строкой.
    new_node = Node(data1, data2)

    if head is None:
        # Если список пустой, новый элемент становится первым.
        head = new_node
        # Так как список циклический, единственный элемент указывает сам на себя.
        new_node.next = new_node
    else:
        # Идём от головы до последнего элемента.
        # Последний элемент — тот, у которого next снова указывает на head.
        current = head
        while current.next != head:
            current = current.next

        # Вставляем новый элемент после последнего.
        current.next = new_node
        # Новый элемент теперь последний, поэтому он указывает на head.
        new_node.next = head

    return True, "Элемент добавлен в конец"


def add_beg(data1, data2):
    """Добавить элемент в начало списка."""
    global head

    if not created:
        return False, "Списка нет, сначала создайте его"

    new_node = Node(data1, data2)

    if head is None:
        # Если список пустой, начало и конец — это один новый элемент.
        head = new_node
        new_node.next = new_node
    else:
        # Чтобы вставить в начало циклического списка,
        # надо найти последний элемент и заставить его указывать на новую голову.
        current = head
        while current.next != head:
            current = current.next

        new_node.next = head
        current.next = new_node
        head = new_node

    return True, "Элемент добавлен в начало"


def get_elements():
    """Вернуть все элементы списком кортежей."""
    result = []

    if head is None:
        return result

    current = head
    while True:
        # Добавляем в обычный Python-список пару: число и строка.
        result.append((current.data1, current.data2))
        current = current.next

        # Когда снова дошли до head, значит круг закончился.
        if current == head:
            break

    return result


def count():
    """Посчитать элементы списка."""
    # Самый простой способ — получить все элементы и взять их количество.
    return len(get_elements())


def search_by_value(data1, data2):
    """Поиск по двум полям."""
    result = []

    # Перебираем все элементы и выбираем только полное совпадение.
    for item_data1, item_data2 in get_elements():
        if item_data1 == data1 and item_data2 == data2:
            result.append((item_data1, item_data2))

    return result


def search_by_first_value(data1):
    """Поиск по числу."""
    result = []

    for item_data1, item_data2 in get_elements():
        if item_data1 == data1:
            result.append((item_data1, item_data2))

    return result


def search_by_second_value(data2):
    """Поиск по строке."""
    result = []

    for item_data1, item_data2 in get_elements():
        if item_data2 == data2:
            result.append((item_data1, item_data2))

    return result


def delete_element(data1, data2):
    """Удалить первый найденный элемент по двум полям."""
    global head

    if not created:
        return False, "Списка нет, сначала создайте его"

    if head is None:
        return False, "Список пуст, удалять нечего"

    current = head
    previous = None

    while True:
        if current.data1 == data1 and current.data2 == data2:
            if current.next == current:
                # Если в списке один элемент, после удаления список станет пустым.
                head = None
            else:
                if current == head:
                    # Если удаляем первый элемент, надо найти последний,
                    # чтобы он начал ссылаться на новую голову.
                    last = head
                    while last.next != head:
                        last = last.next
                    head = head.next
                    last.next = head
                else:
                    # Если удаляем не голову, просто перепрыгиваем через current.
                    previous.next = current.next

            return True, "Элемент удалён"

        previous = current
        current = current.next

        # Если вернулись в начало, значит нужный элемент не найден.
        if current == head:
            break

    return False, "Элемент не найден"
