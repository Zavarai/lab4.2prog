#include <cstring>
#include <sstream>
#include <string>

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

struct Node {
    double number;
    std::string text;
    Node* next;
};

static Node* head = nullptr;
static bool created = false;
static std::string last_message = "";

static Node* last_node() {
    if (head == nullptr) {
        return nullptr;
    }
    Node* p = head;
    while (p->next != head) {
        p = p->next;
    }
    return p;
}

static void clear_list() {
    if (head == nullptr) {
        return;
    }
    Node* last = last_node();
    last->next = nullptr;
    while (head != nullptr) {
        Node* p = head;
        head = head->next;
        delete p;
    }
}

extern "C" {

API int create_structure() {
    clear_list();
    head = nullptr;
    created = true;
    last_message = "Создан пустой список.";
    return 1;
}

API int delete_structure() {
    clear_list();
    head = nullptr;
    created = false;
    last_message = "Структура удалена.";
    return 1;
}

API int add_end(double number, const char* text) {
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    Node* p = new Node{number, text ? text : "", nullptr};
    if (head == nullptr) {
        head = p;
        p->next = p;
    } else {
        Node* last = last_node();
        last->next = p;
        p->next = head;
    }
    last_message = "Добавлено в конец.";
    return 1;
}

API int add_beg(double number, const char* text) {
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    Node* p = new Node{number, text ? text : "", nullptr};
    if (head == nullptr) {
        head = p;
        p->next = p;
    } else {
        Node* last = last_node();
        p->next = head;
        last->next = p;
        head = p;
    }
    last_message = "Добавлено в начало.";
    return 1;
}

API int is_empty() {
    if (!created) {
        return 1;
    }
    return head == nullptr ? 1 : 0;
}

API int is_created() {
    return created ? 1 : 0;
}

API int count() {
    if (!created) {
        return 0;
    }
    if (head == nullptr) {
        return 0;
    }
    int k = 0;
    Node* p = head;
    do {
        k++;
        p = p->next;
    } while (p != head);
    return k;
}

API int delete_element(double number, const char* text) {
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string t = text ? text : "";
    Node* prev = last_node();
    Node* p = head;
    do {
        if (p->number == number && p->text == t) {
            if (p->next == p) {
                delete p;
                head = nullptr;
            } else {
                prev->next = p->next;
                if (p == head) {
                    head = p->next;
                }
                delete p;
            }
            last_message = "Элемент удален.";
            return 1;
        }
        prev = p;
        p = p->next;
    } while (p != head);
    last_message = "Элемент не найден.";
    return 0;
}

API int search_by_value(double number, const char* text) {
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string t = text ? text : "";
    std::ostringstream out;
    bool found = false;
    Node* p = head;
    do {
        if (p->number == number && p->text == t) {
            out << p->number << " " << p->text << "\n";
            found = true;
        }
        p = p->next;
    } while (p != head);
    if (!found) {
        last_message = "Элемент не найден.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API int search_by_first_value(double number) {
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
    Node* p = head;
    do {
        if (p->number == number) {
            out << p->number << " " << p->text << "\n";
            found = true;
        }
        p = p->next;
    } while (p != head);
    if (!found) {
        last_message = "Элементы не найдены.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API int search_by_second_value(const char* text) {
    if (!created) {
        last_message = "Сначала создайте структуру.";
        return 0;
    }
    if (head == nullptr) {
        last_message = "Список пуст.";
        return 0;
    }
    std::string t = text ? text : "";
    std::ostringstream out;
    bool found = false;
    Node* p = head;
    do {
        if (p->text == t) {
            out << p->number << " " << p->text << "\n";
            found = true;
        }
        p = p->next;
    } while (p != head);
    if (!found) {
        last_message = "Элементы не найдены.";
        return 0;
    }
    last_message = out.str();
    return 1;
}

API const char* get_last_message() {
    return last_message.c_str();
}

API int get_element_at(int index, double* number, char* text, int text_size) {
    if (!created) {
        return 0;
    }
    if (head == nullptr || index < 0 || number == nullptr || text == nullptr || text_size <= 0) {
        return 0;
    }
    Node* p = head;
    int i = 0;
    do {
        if (i == index) {
            *number = p->number;
            std::strncpy(text, p->text.c_str(), text_size - 1);
            text[text_size - 1] = '\0';
            return 1;
        }
        i++;
        p = p->next;
    } while (p != head);
    return 0;
}

}
