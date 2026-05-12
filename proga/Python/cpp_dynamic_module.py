# Обёртка для C++ DLL из папки CPP/dynamic.
# Этот файл нужен, чтобы Python-приложение могло вызвать функции из C++.
# В GUI он выглядит так же, как list_module.py, потому что функции названы одинаково.

import ctypes  # библиотека Python для вызова функций из DLL
import os  # нужна для правильного составления пути к DLL

# Полный путь к DLL с динамическим списком.
# __file__ — путь к этому Python-файлу, от него поднимаемся на папку выше.
DLL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "CPP", "dynamic", "list_dynamic.dll"
)

# Если DLL не собрана, программа сразу скажет понятную ошибку.
if not os.path.exists(DLL_PATH):
    raise FileNotFoundError("Не найдена DLL: CPP/dynamic/list_dynamic.dll")

# Загружаем DLL, чтобы дальше вызывать её функции.
lib = ctypes.CDLL(DLL_PATH)

# Здесь объясняем ctypes, какие типы аргументов принимает каждая C++ функция.
# c_double соответствует double, c_char_p соответствует char*.
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
    """Перевести строку Python в байты для C++."""
    # C++ DLL ждёт const char*, поэтому обычную строку надо закодировать.
    return text.encode("utf-8")


def create_structure():
    """Создать список внутри C++ DLL."""
    if lib.create_structure() == 1:
        return True, "Создан пустой циклический список"
    return False, "Список уже создан"


def delete_structure():
    """Удалить список внутри C++ DLL."""
    if lib.delete_structure() == 1:
        return True, "Список удалён"
    return False, "Списка нет, сначала создайте его"


def is_created():
    """Узнать, создан ли список в DLL."""
    return lib.is_created() == 1


def is_empty():
    """Узнать, пустой ли список в DLL."""
    return lib.is_empty() == 1


def add_end(data1, data2):
    """Добавить элемент в конец C++ списка."""
    if lib.add_end(data1, to_bytes(data2)) == 1:
        return True, "Элемент добавлен в конец"
    return False, "Списка нет, сначала создайте его"


def add_beg(data1, data2):
    """Добавить элемент в начало C++ списка."""
    if lib.add_beg(data1, to_bytes(data2)) == 1:
        return True, "Элемент добавлен в начало"
    return False, "Списка нет, сначала создайте его"


def count():
    """Вернуть количество элементов из C++ списка."""
    return lib.count()


def get_elements():
    """Получить все элементы из C++ DLL и вернуть их Python-списком."""
    result = []

    # В DLL есть функция get_item(index), поэтому идём по индексам от 0 до count - 1.
    for i in range(count()):
        # number — переменная, куда C++ запишет число.
        number = ctypes.c_double()
        # text_buffer — буфер на 100 символов, куда C++ запишет строку.
        text_buffer = ctypes.create_string_buffer(100)

        # byref(number) передаёт адрес переменной, чтобы C++ мог её изменить.
        ok = lib.get_item(i, ctypes.byref(number), text_buffer, 100)
        if ok == 1:
            text = text_buffer.value.decode("utf-8", errors="ignore")
            result.append((number.value, text))

    return result


def search_by_value(data1, data2):
    """Поиск по двум полям."""
    # Для удобного вывода возвращаем не 0/1 из DLL, а список найденных элементов.
    result = []
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
    """Удалить элемент через C++ DLL."""
    if not is_created():
        return False, "Списка нет, сначала создайте его"

    if is_empty():
        return False, "Список пуст, удалять нечего"

    if lib.delete_element(data1, to_bytes(data2)) == 1:
        return True, "Элемент удалён"

    return False, "Элемент не найден"
