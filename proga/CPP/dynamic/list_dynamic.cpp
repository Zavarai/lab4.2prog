// C++ модуль: циклический односвязный список на динамической памяти.
// Этот файл собирается в DLL, а Python вызывает функции из этой DLL через ctypes.
// Здесь память выделяется вручную через new и освобождается вручную через delete.

#include <cstring> // нужны функции strncpy и strcmp для работы с char-массивами

// Node — один узел, то есть один элемент списка.
struct Node {
    double data1;       // первое поле элемента: число
    char data2[100];    // второе поле элемента: строка максимум 99 символов + '\0'
    Node* next;         // указатель на следующий элемент списка
};

// head указывает на первый элемент списка.
// Если head == nullptr, значит элементов нет.
Node* head = nullptr;

// created показывает, создана ли структура.
// Это нужно, чтобы отличать "список не создан" от "список создан, но пустой".
bool created = false;

// extern "C" отключает C++-искажение имён функций.
// Благодаря этому Python может найти функции в DLL по простым именам.
extern "C" {

// __declspec(dllexport) экспортирует функцию из DLL.
// create_structure создаёт пустой список.
__declspec(dllexport) int create_structure() {
    if (created) {
        return 0; // 0 означает неудачу: список уже создан
    }

    head = nullptr;
    created = true;
    return 1; // 1 означает успех
}

// delete_structure удаляет все элементы списка и сам список.
__declspec(dllexport) int delete_structure() {
    if (!created) {
        return 0; // список ещё не был создан
    }

    if (head != nullptr) {
        // Начинаем со второго элемента, потому что head удалим отдельно в конце.
        Node* current = head->next;

        // Идём по кругу, пока снова не дошли до head.
        while (current != head) {
            Node* temp = current;
            current = current->next;
            delete temp; // освобождаем память текущего элемента
        }

        delete head; // удаляем первый элемент
    }

    head = nullptr;
    created = false;
    return 1;
}

// is_created возвращает 1, если список создан, иначе 0.
__declspec(dllexport) int is_created() {
    return created ? 1 : 0;
}

// is_empty возвращает 1, если элементов нет.
__declspec(dllexport) int is_empty() {
    return head == nullptr ? 1 : 0;
}

// add_end добавляет новый элемент в конец циклического списка.
__declspec(dllexport) int add_end(double data1, const char* data2) {
    if (!created) {
        return 0;
    }

    // Выделяем память под новый узел.
    Node* new_node = new Node;
    new_node->data1 = data1;

    // Копируем строку безопасно: не больше 99 символов.
    strncpy(new_node->data2, data2, 99);
    new_node->data2[99] = '\0'; // обязательно ставим конец строки

    if (head == nullptr) {
        // Если список пустой, новый элемент становится первым.
        head = new_node;
        // В циклическом списке единственный элемент указывает сам на себя.
        new_node->next = new_node;
    } else {
        // Ищем последний элемент: у него next снова указывает на head.
        Node* current = head;
        while (current->next != head) {
            current = current->next;
        }

        // Прицепляем новый элемент после последнего.
        current->next = new_node;
        // Новый последний элемент должен ссылаться на голову.
        new_node->next = head;
    }

    return 1;
}

// add_beg добавляет новый элемент в начало списка.
__declspec(dllexport) int add_beg(double data1, const char* data2) {
    if (!created) {
        return 0;
    }

    Node* new_node = new Node;
    new_node->data1 = data1;
    strncpy(new_node->data2, data2, 99);
    new_node->data2[99] = '\0';

    if (head == nullptr) {
        head = new_node;
        new_node->next = new_node;
    } else {
        // Чтобы вставить в начало, надо найти последний элемент.
        Node* last = head;
        while (last->next != head) {
            last = last->next;
        }

        // Новый элемент указывает на старую голову.
        new_node->next = head;
        // Последний элемент теперь должен указывать на новую голову.
        last->next = new_node;
        // Переставляем голову списка.
        head = new_node;
    }

    return 1;
}

// count считает количество элементов в списке.
__declspec(dllexport) int count() {
    if (head == nullptr) {
        return 0;
    }

    int result = 0;
    Node* current = head;

    // do while удобен, потому что head тоже надо посчитать.
    do {
        result++;
        current = current->next;
    } while (current != head);

    return result;
}

// get_item возвращает элемент по индексу.
// data1 и data2 передаются как указатели, чтобы функция могла записать туда результат.
__declspec(dllexport) int get_item(int index, double* data1, char* data2, int data2_size) {
    if (head == nullptr || index < 0) {
        return 0;
    }

    Node* current = head;
    int i = 0;

    do {
        if (i == index) {
            *data1 = current->data1;
            strncpy(data2, current->data2, data2_size - 1);
            data2[data2_size - 1] = '\0';
            return 1;
        }

        i++;
        current = current->next;
    } while (current != head);

    return 0;
}

// search_by_value ищет элемент, где совпали и число, и строка.
__declspec(dllexport) int search_by_value(double data1, const char* data2) {
    if (head == nullptr) {
        return 0;
    }

    Node* current = head;

    do {
        // strcmp возвращает 0, если C-строки одинаковые.
        if (current->data1 == data1 && strcmp(current->data2, data2) == 0) {
            return 1;
        }
        current = current->next;
    } while (current != head);

    return 0;
}

// search_by_first_value ищет элемент только по числу.
__declspec(dllexport) int search_by_first_value(double data1) {
    if (head == nullptr) {
        return 0;
    }

    Node* current = head;

    do {
        if (current->data1 == data1) {
            return 1;
        }
        current = current->next;
    } while (current != head);

    return 0;
}

// search_by_second_value ищет элемент только по строке.
__declspec(dllexport) int search_by_second_value(const char* data2) {
    if (head == nullptr) {
        return 0;
    }

    Node* current = head;

    do {
        if (strcmp(current->data2, data2) == 0) {
            return 1;
        }
        current = current->next;
    } while (current != head);

    return 0;
}

// delete_element удаляет первый элемент, где совпали число и строка.
__declspec(dllexport) int delete_element(double data1, const char* data2) {
    if (!created || head == nullptr) {
        return 0;
    }

    Node* current = head;
    Node* previous = nullptr;

    do {
        if (current->data1 == data1 && strcmp(current->data2, data2) == 0) {
            if (current->next == current) {
                // В списке был один элемент.
                delete current;
                head = nullptr;
            } else if (current == head) {
                // Удаляем голову, поэтому надо найти последний элемент.
                Node* last = head;
                while (last->next != head) {
                    last = last->next;
                }

                head = head->next;
                last->next = head;
                delete current;
            } else {
                // Удаляем обычный элемент в середине или в конце.
                previous->next = current->next;
                delete current;
            }

            return 1;
        }

        previous = current;
        current = current->next;
    } while (current != head);

    return 0;
}

}
