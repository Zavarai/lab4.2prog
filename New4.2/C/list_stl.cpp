#include <cstring>
#include <list>
#include <sstream>
#include <string>

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

struct NodeData {
    // Данные одного элемента списка
    double data1;
    std::string data2;
};

static std::list<NodeData> data_list;
static bool created = false;
static std::string last_message = "Выбран C++ модуль (STL).";

extern "C" {

API int create_structure() {
    // Создание пустой структуры
    if (created) {
        last_message = "Структура уже создана.";
        return 0;
    }
    data_list.clear();
    created = true;
    last_message = "Создан пустой циклический односвязный список (STL).";
    return 1;
}

API int delete_structure() {
    // Удаление всей структуры
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    data_list.clear();
    created = false;
    last_message = "Структура удалена.";
    return 1;
}

API int add_end(double value1, const char* value2) {
    // Добавление элемента в конец
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    data_list.push_back({value1, value2 ? value2 : ""});
    std::ostringstream out;
    out << "Добавлено в конец: " << value1 << " " << data_list.back().data2;
    last_message = out.str();
    return 1;
}

API int add_beg(double value1, const char* value2) {
    // Добавление элемента в начало
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    data_list.push_front({value1, value2 ? value2 : ""});
    std::ostringstream out;
    out << "Добавлено в начало: " << value1 << " " << data_list.front().data2;
    last_message = out.str();
    return 1;
}

API int read_elements() {
    // Формирование текста со всеми элементами
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (data_list.empty()) {
        last_message = "Список пуст.";
        return 1;
    }
    std::ostringstream out;
    out << "Список элементов:\n";
    int i = 1;
    for (const auto& item : data_list) {
        out << i << ". " << item.data1 << " " << item.data2 << "\n";
        i++;
    }
    last_message = out.str();
    return 1;
}

API int delete_element(double value1, const char* value2) {
    // Удаление первого совпавшего элемента
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (data_list.empty()) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    for (auto it = data_list.begin(); it != data_list.end(); ++it) {
        if (it->data1 == value1 && it->data2 == text) {
            data_list.erase(it);
            last_message = "Элемент удален.";
            return 1;
        }
    }
    last_message = "Элемент не найден.";
    return 0;
}

API int search_by_value(double value1, const char* value2) {
    // Поиск по двум полям
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (data_list.empty()) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    std::ostringstream out;
    bool found = false;
    for (const auto& item : data_list) {
        if (item.data1 == value1 && item.data2 == text) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << item.data1 << " " << item.data2 << "\n";
            found = true;
        }
    }
    if (!found) {
        last_message = "Элемент не найден.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API int search_by_first_value(double value1) {
    // Поиск по числу
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (data_list.empty()) {
        last_message = "Список пуст.";
        return 0;
    }
    std::ostringstream out;
    bool found = false;
    for (const auto& item : data_list) {
        if (item.data1 == value1) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << item.data1 << " " << item.data2 << "\n";
            found = true;
        }
    }
    if (!found) {
        last_message = "Элементы не найдены.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API int search_by_second_value(const char* value2) {
    // Поиск по строке
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (data_list.empty()) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    std::ostringstream out;
    bool found = false;
    for (const auto& item : data_list) {
        if (item.data2 == text) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << item.data1 << " " << item.data2 << "\n";
            found = true;
        }
    }
    if (!found) {
        last_message = "Элементы не найдены.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API int is_created() {
    return created ? 1 : 0;
}

API int is_empty() {
    return data_list.empty() ? 1 : 0;
}

API int count() {
    if (!created) {
        return 0;
    }
    return (int)data_list.size();
}

API const char* get_last_message() {
    return last_message.c_str();
}

API int get_element_at(int index, double* value1, char* value2, int value2_size) {
    if (!created || index < 0 || value1 == nullptr || value2 == nullptr || value2_size <= 0) {
        return 0;
    }
    int i = 0;
    for (const auto& item : data_list) {
        if (i == index) {
            *value1 = item.data1;
            std::strncpy(value2, item.data2.c_str(), value2_size - 1);
            value2[value2_size - 1] = '\0';
            return 1;
        }
        i++;
    }
    return 0;
}

}
