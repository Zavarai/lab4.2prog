#include <cstring>
#include <sstream>
#include <string>

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

struct Node {
    // Узел циклического списка
    double data1;
    std::string data2;
    Node* next;
};

static Node* head = nullptr;
static bool created = false;
static int size_list = 0;
static std::string last_message = "Выбран C++ модуль (dynamic memory).";

static Node* find_last() {
    // Поиск последнего элемента
    if (head == nullptr) {
        return nullptr;
    }
    Node* current = head;
    while (current->next != head) {
        current = current->next;
    }
    return current;
}

static void clear_all() {
    // Полная очистка списка
    if (head == nullptr) {
        size_list = 0;
        return;
    }
    Node* last = find_last();
    last->next = nullptr;
    Node* current = head;
    while (current != nullptr) {
        Node* next = current->next;
        delete current;
        current = next;
    }
    head = nullptr;
    size_list = 0;
}

extern "C" {

API int create_structure() {
    // Создание пустой структуры
    if (created) {
        last_message = "Структура уже создана.";
        return 0;
    }
    clear_all();
    created = true;
    last_message = "Создан пустой циклический односвязный список.";
    return 1;
}

API int delete_structure() {
    // Удаление всей структуры
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    clear_all();
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
    Node* node = new Node{value1, value2 ? value2 : "", nullptr};
    if (head == nullptr) {
        head = node;
        node->next = node;
    } else {
        Node* last = find_last();
        last->next = node;
        node->next = head;
    }
    size_list++;
    std::ostringstream out;
    out << "Добавлено в конец: " << value1 << " " << node->data2;
    last_message = out.str();
    return 1;
}

API int add_beg(double value1, const char* value2) {
    // Добавление элемента в начало
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    Node* node = new Node{value1, value2 ? value2 : "", nullptr};
    if (head == nullptr) {
        head = node;
        node->next = node;
    } else {
        Node* last = find_last();
        node->next = head;
        last->next = node;
        head = node;
    }
    size_list++;
    std::ostringstream out;
    out << "Добавлено в начало: " << value1 << " " << node->data2;
    last_message = out.str();
    return 1;
}

API int read_elements() {
    // Формирование текста со всеми элементами
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 1;
    }
    std::ostringstream out;
    out << "Список элементов:\n";
    Node* current = head;
    int i = 1;
    do {
        out << i << ". " << current->data1 << " " << current->data2 << "\n";
        current = current->next;
        i++;
    } while (current != head);
    last_message = out.str();
    return 1;
}

API int delete_element(double value1, const char* value2) {
    // Удаление первого совпавшего элемента
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    Node* current = head;
    Node* prev = find_last();
    do {
        if (current->data1 == value1 && current->data2 == text) {
            if (current->next == current) {
                delete current;
                head = nullptr;
            } else {
                prev->next = current->next;
                if (current == head) {
                    head = current->next;
                }
                delete current;
            }
            size_list--;
            last_message = "Элемент удален.";
            return 1;
        }
        prev = current;
        current = current->next;
    } while (current != head);
    last_message = "Элемент не найден.";
    return 0;
}

API int search_by_value(double value1, const char* value2) {
    // Поиск по двум полям
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    std::ostringstream out;
    bool found = false;
    Node* current = head;
    do {
        if (current->data1 == value1 && current->data2 == text) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << current->data1 << " " << current->data2 << "\n";
            found = true;
        }
        current = current->next;
    } while (current != head);
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
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::ostringstream out;
    bool found = false;
    Node* current = head;
    do {
        if (current->data1 == value1) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << current->data1 << " " << current->data2 << "\n";
            found = true;
        }
        current = current->next;
    } while (current != head);
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
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string text = value2 ? value2 : "";
    std::ostringstream out;
    bool found = false;
    Node* current = head;
    do {
        if (current->data2 == text) {
            if (!found) {
                out << "Результат поиска:\n";
            }
            out << current->data1 << " " << current->data2 << "\n";
            found = true;
        }
        current = current->next;
    } while (current != head);
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
    return head == nullptr ? 1 : 0;
}

API int count() {
    if (!created) {
        return 0;
    }
    return size_list;
}

API const char* get_last_message() {
    return last_message.c_str();
}

API int get_element_at(int index, double* value1, char* value2, int value2_size) {
    if (!created || head == nullptr || index < 0 || value1 == nullptr || value2 == nullptr || value2_size <= 0) {
        return 0;
    }
    Node* current = head;
    int i = 0;
    do {
        if (i == index) {
            *value1 = current->data1;
            std::strncpy(value2, current->data2.c_str(), value2_size - 1);
            value2[value2_size - 1] = '\0';
            return 1;
        }
        current = current->next;
        i++;
    } while (current != head);
    return 0;
}

}
