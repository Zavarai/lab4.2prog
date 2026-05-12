// C++ модуль: список на STL контейнере std::list.
// Этот файл тоже собирается в DLL и вызывается из Python через ctypes.
// В отличие от dynamic-варианта, здесь памятью управляет контейнер std::list.

#include <list>    // std::list — готовый двусвязный список из STL
#include <string>  // std::string — удобная строка C++
#include <cstring> // strncpy нужен, чтобы отдавать строку обратно в Python

// Item — один элемент списка.
struct Item {
    double data1;      // первое поле: число
    std::string data2; // второе поле: строка C++
};

// Глобальный список items хранит все элементы.
// std::list сам выделяет и освобождает память для своих узлов.
std::list<Item> items;

// created показывает, была ли создана структура.
bool created = false;

// extern "C" нужен, чтобы имена функций в DLL были простыми для Python.
extern "C" {

// create_structure создаёт пустой список.
__declspec(dllexport) int create_structure() {
    if (created) {
        return 0;
    }

    // На всякий случай очищаем контейнер перед началом работы.
    items.clear();
    created = true;
    return 1;
}

// delete_structure удаляет все элементы и помечает список как не созданный.
__declspec(dllexport) int delete_structure() {
    if (!created) {
        return 0;
    }

    // clear удаляет все элементы контейнера.
    items.clear();
    created = false;
    return 1;
}

// is_created возвращает 1, если список создан.
__declspec(dllexport) int is_created() {
    return created ? 1 : 0;
}

// is_empty возвращает 1, если в std::list нет элементов.
__declspec(dllexport) int is_empty() {
    return items.empty() ? 1 : 0;
}

// add_end добавляет элемент в конец списка.
__declspec(dllexport) int add_end(double data1, const char* data2) {
    if (!created) {
        return 0;
    }

    // push_back добавляет в конец контейнера.
    // data2 автоматически превращается в std::string.
    items.push_back({data1, data2});
    return 1;
}

// add_beg добавляет элемент в начало списка.
__declspec(dllexport) int add_beg(double data1, const char* data2) {
    if (!created) {
        return 0;
    }

    // push_front добавляет в начало контейнера.
    items.push_front({data1, data2});
    return 1;
}

// count возвращает количество элементов.
__declspec(dllexport) int count() {
    return (int)items.size();
}

// get_item возвращает элемент по номеру index.
// std::list не умеет быстро обращаться по индексу, поэтому идём циклом от начала.
__declspec(dllexport) int get_item(int index, double* data1, char* data2, int data2_size) {
    if (index < 0 || index >= (int)items.size()) {
        return 0;
    }

    int i = 0;
    for (Item item : items) {
        if (i == index) {
            *data1 = item.data1;
            strncpy(data2, item.data2.c_str(), data2_size - 1);
            data2[data2_size - 1] = '\0';
            return 1;
        }
        i++;
    }

    return 0;
}

// search_by_value ищет элемент по числу и строке.
__declspec(dllexport) int search_by_value(double data1, const char* data2) {
    for (Item item : items) {
        // std::string можно сравнивать с const char* через ==.
        if (item.data1 == data1 && item.data2 == data2) {
            return 1;
        }
    }

    return 0;
}

// search_by_first_value ищет элемент только по числу.
__declspec(dllexport) int search_by_first_value(double data1) {
    for (Item item : items) {
        if (item.data1 == data1) {
            return 1;
        }
    }

    return 0;
}

// search_by_second_value ищет элемент только по строке.
__declspec(dllexport) int search_by_second_value(const char* data2) {
    for (Item item : items) {
        if (item.data2 == data2) {
            return 1;
        }
    }

    return 0;
}

// delete_element удаляет первый элемент, где совпали число и строка.
__declspec(dllexport) int delete_element(double data1, const char* data2) {
    if (!created || items.empty()) {
        return 0;
    }

    // Итератор it указывает на текущий элемент std::list.
    for (auto it = items.begin(); it != items.end(); ++it) {
        if (it->data1 == data1 && it->data2 == data2) {
            // erase удаляет элемент из контейнера.
            items.erase(it);
            return 1;
        }
    }

    return 0;
}

}
