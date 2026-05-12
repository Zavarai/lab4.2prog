# Обёртка для C++ DLL из папки CPP/stl.
# Этот файл нужен, чтобы GUI на Python мог работать со списком на std::list.
# Названия функций такие же, как в list_module.py и cpp_dynamic_module.py.

import ctypes  # позволяет вызывать функции из DLL
import os  # помогает собрать путь к файлу DLL

# Путь к DLL, где лежит C++ реализация через STL.
DLL_PATH = os.path.join(os.path.dirname(__file__), "..", "CPP", "stl", "list_stl.dll")

# Проверяем, что DLL реально существует.
# Если её нет, значит сначала надо собрать C++ файл.
if not os.path.exists(DLL_PATH):
    raise FileNotFoundError("Не найдена DLL: CPP/stl/list_stl.dll")

# Загружаем DLL в Python.
lib = ctypes.CDLL(DLL_PATH)

# Указываем типы параметров для функций из DLL.
# Это нужно, чтобы Python правильно передавал данные в C++.
lib.add_end.argtypes = [ctypes.c_double, ctypes.c_char_p]
lib.add_beg.argtypes = [ctypes.c_double, ctypes.c_char_p]
lib.delete_element.argtypes = [ctypes.c_double, ctypes.c_char_p]
lib.search_by_value.argtypes = [ctypes.c_double, ctypes.c_char_p]
lib.search_by_first_value.argtypes = [ctypes.c_double]
lib.search_by_second_value.argtypes = [ctypes.c_char_p]
lib.get_item.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_char_p,
    ctypes.c_int,
]


def to_bytes(text):
    """Перевести Python-строку в байты для C++."""
    return text.encode("utf-8")


def create_structure():
    """Создать пустой STL-список."""
    if lib.create_structure() == 1:
        return True, "Создан пустой список на STL"
    return False, "Список уже создан"


def delete_structure():
    """Удалить STL-список."""
    if lib.delete_structure() == 1:
        return True, "Список удалён"
    return False, "Списка нет, сначала создайте его"


def is_created():
    """Проверить, создан ли список."""
    return lib.is_created() == 1


def is_empty():
    """Проверить, пустой ли список."""
    return lib.is_empty() == 1


def add_end(data1, data2):
    """Добавить элемент в конец списка."""
    if lib.add_end(data1, to_bytes(data2)) == 1:
        return True, "Элемент добавлен в конец"
    return False, "Списка нет, сначала создайте его"


def add_beg(data1, data2):
    """Добавить элемент в начало списка."""
    if lib.add_beg(data1, to_bytes(data2)) == 1:
        return True, "Элемент добавлен в начало"
    return False, "Списка нет, сначала создайте его"


def count():
    """Получить количество элементов."""
    return lib.count()


def get_elements():
    """Получить все элементы из C++ STL-списка."""
    result = []

    # Берём элементы по индексам: 0, 1, 2 и так далее.
    for i in range(count()):
        # Сюда C++ запишет число.
        number = ctypes.c_double()
        # Сюда C++ запишет строку, максимум 100 байт.
        text_buffer = ctypes.create_string_buffer(100)

        ok = lib.get_item(i, ctypes.byref(number), text_buffer, 100)
        if ok == 1:
            text = text_buffer.value.decode("utf-8", errors="ignore")
            result.append((number.value, text))

    return result


def search_by_value(data1, data2):
    """Поиск по числу и строке сразу."""
    result = []
    for item_data1, item_data2 in get_elements():
        if item_data1 == data1 and item_data2 == data2:
            result.append((item_data1, item_data2))
    return result


def search_by_first_value(data1):
    """Поиск только по числу."""
    result = []
    for item_data1, item_data2 in get_elements():
        if item_data1 == data1:
            result.append((item_data1, item_data2))
    return result


def search_by_second_value(data2):
    """Поиск только по строке."""
    result = []
    for item_data1, item_data2 in get_elements():
        if item_data2 == data2:
            result.append((item_data1, item_data2))
    return result


def delete_element(data1, data2):
    """Удалить элемент по двум полям."""
    if not is_created():
        return False, "Списка нет, сначала создайте его"

    if is_empty():
        return False, "Список пуст, удалять нечего"

    if lib.delete_element(data1, to_bytes(data2)) == 1:
        return True, "Элемент удалён"

    return False, "Элемент не найден"
