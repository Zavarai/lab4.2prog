#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>

// Структура узла
typedef struct Node {
    double data1;
    char data2[100];
    struct Node* next;
} Node;

// Массив структур (вместо списка)
Node nodes[1000];  // Фиксированный массив на 1000 элементов
int node_count = 0; // Сколько реально используется
int head_index = -1; // Индекс головы в массиве
int empty_list = 0;

// Функции
void create_structure();
void delete_structure();
void add_end(double v1, char v2[]);
void add_beg(double v1, char v2[]);
void read_elements();
void delete_element(double v1, char v2[]);
int empty();
int count();
int search_by_value(double v1, char v2[]);
void search_by_first_value(double v1);
void search_by_second_value(char v2[]);
void print_menu(int selected);
int get_key();

// Главная функция
int main() {
    int selected = 1;
    int key;
    double value1;
    char value2[100];
    
    system("cls");
    
    while (1) {
        print_menu(selected);
        key = get_key();
        
        if (key == 'Up') {
            selected--;
            if (selected < 1) selected = 12;
        }
        else if (key == 'Down') {
            selected++;
            if (selected > 12) selected = 1;
        }
        else if (key == 13) {
            system("cls");
            
            switch (selected) {
                case 1:
                    create_structure();
                    break;
                    
                case 2:
                    delete_structure();
                    break;
                    
                case 3:
                    if (empty()) {
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    } else {
                        printf("Введите значение (число): ");
                        scanf("%lf", &value1);
                        printf("Введите значение (строка): ");
                        scanf("%s", value2);
                        add_end(value1, value2);
                    }
                    break;

                case 4:
                    if (empty()) {
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    } else {
                        printf("Введите значение (число): ");
                        scanf("%lf", &value1);
                        printf("Введите значение (строка): ");
                        scanf("%s", value2);
                        add_beg(value1, value2);
                    }
                    break;
                case 5:
                    read_elements();
                    break;
                    
                case 6:
                    if (empty())
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    else
                        printf("Список не пуст\n");
                    break;
                    
                case 7:
                    if (empty())
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    else
                        printf("Количество элементов: %d\n", count());
                    break;
                    
                case 8:
                   if (empty()) {
                       printf("Списка нет, сначала создайте его (пункт 1)\n");
                   } else {
                      printf("Введите значение (число): ");
                       scanf("%lf", &value1);
                       printf("Введите значение (строка): ");
                       scanf("%s", value2);
                      search_by_value(value1, value2);
                   }
                   break;
                    
                case 9:
                    if (empty()) {
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    } else {
                        printf("Введите значение (число): ");
                        scanf("%lf", &value1);
                        search_by_first_value(value1);
                    }
                    break;
                    
                case 10:
                    if (empty()) {
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    } else {
                        printf("Введите значение (строка): ");
                        scanf("%s", value2);
                        search_by_second_value(value2);
                    }
                    break;
                    
                case 11:
                    if (empty()) {
                        printf("Списка нет, сначала создайте его (пункт 1)\n");
                    } else {
                        printf("Введите элемент (число) для удаления: ");
                        scanf("%lf", &value1);
                        printf("Введите элемент (строку) для удаления: ");
                        scanf("%s", value2);
                        delete_element(value1, value2);
                    }
                    break;
                    
                case 12:
                    system("cls");
                    printf("Выход из программы...\n");
                    return 0;
            }
            
            printf("\nНажмите любую клавишу для продолжения...");
            getch();
        }
    }
    
    return 0;
}

int get_key() {
    int ch = getch();
    
    if (ch == 224) {
        ch = getch();
        if (ch == 72) return 'Up';
        if (ch == 80) return 'Down';
        return ch;
    }
}

void print_menu(int selected) {
    system("cls");
    printf("======== МЕНЮ ========\n\n");
    
    char* menu_items[] = {
        "1 - Создание структуры",
        "2 - Удаление структуры",
        "3 - Добавить элемент в конец",
        "4 - Добавить элемент в начало",
        "5 - Просмотр элементов структуры",
        "6 - Определение пустоты структуры",
        "7 - Определение количества элементов в структуре",
        "8 - Поиск элемента по двум полям",
        "9 - Поиск по первому полю",
        "10 - Поиск по второму полю",
        "11 - Удаление элемента структуры",
        "12 - Выход"
    };
    
    for (int i = 0; i < 12; i++) {
        if (selected == i + 1) {
            printf(" -> %s\n", menu_items[i]);
        } else {
            printf("    %s\n", menu_items[i]);
        }
    }
    
    printf("\nИспользуйте стрелки вверх/вниз для выбора, Enter - подтвердить\n");
    printf("Текущий размер списка: %d элементов\n", count());
}

// 1. Создание структуры
void create_structure() {
    if (empty_list == 1) {
        printf("Список уже создан, для сначала удалите (пункт 2)\n");
    } else {
        node_count = 0;
        head_index = -1;
        empty_list = 1;
        printf("Создан пустой циклический односвязный список\n");
    }
}

// 2. Удаление структуры
void delete_structure() {
    if (empty_list == 1) {
        node_count = 0;
        head_index = -1;
        empty_list = 0;
        printf("Список удалён\n");
    } else {
        printf("Списка нет, сначала создайте его (пункт 1)\n");
    }
}

// 3. Добавить элемент в конец 
void add_end(double v1, char v2[]) {
    
    // Находим последний элемент
    int last_index = head_index;
    if (last_index != -1) {
        // В циклическом списке последний указывает на голову
        while (nodes[last_index].next != &nodes[head_index]) {
            last_index = (int)(nodes[last_index].next - nodes);
        }
    }
    
    // Добавляем новый элемент
    nodes[node_count].data1 = v1;
    strcpy(nodes[node_count].data2, v2);
    
    if (head_index == -1) {
        // Первый элемент - указывает сам на себя
        head_index = node_count;
        nodes[node_count].next = &nodes[node_count];
    } else {
        // Вставляем между последним и первым
        nodes[node_count].next = &nodes[head_index];  // Новая указывает на голову
        nodes[last_index].next = &nodes[node_count];  // Последний указывает на новую
    }
    
    node_count++;
    printf("Добавлено в конец: %g %s\n", v1, v2);
}

// 4. Добавить элемент в начало 
void add_beg(double v1, char v2[]) {
    
    // Добавляем новый элемент
    nodes[node_count].data1 = v1;
    strcpy(nodes[node_count].data2, v2);
    
    if (head_index == -1) {
        // Первый элемент - указывает сам на себя
        head_index = node_count;
        nodes[node_count].next = &nodes[node_count];
    } else {
        // Находим последний элемент
        int last_index = head_index;
        while (nodes[last_index].next != &nodes[head_index]) {
            last_index = (int)(nodes[last_index].next - nodes);
        }
        
        // Новая голова указывает на старую голову
        nodes[node_count].next = &nodes[head_index];
        // Последний элемент указывает на новую голову
        nodes[last_index].next = &nodes[node_count];
        // Меняем голову
        head_index = node_count;
    }
    
    node_count++;
    printf("Добавлено в начало: %g %s\n", v1, v2);
}

// 5. Просмотр элементов 
void read_elements() {
    if (empty_list == 0) {
        printf("Списка нет, сначала создайте его (пункт 1)\n");
        return;
    }
    
    int current = head_index;
    int start = head_index;
    int i = 1;
    
    printf("Список элементов:\n");
    
    do {
        printf("%d. %g %s\n", i, nodes[current].data1, nodes[current].data2);
        current = (int)(nodes[current].next - nodes);
        i++;
    } while (current != start);  // Пока не вернёмся к началу
    
    printf("\n");
}

// 6. Определение пустоты
int empty() {
    return (empty_list == 0);
}

// 7. Определение количества элементов 
int count() {
    if (head_index == -1) {
        return 0;
    }
    
    int current = head_index;
    int start = head_index;
    int k = 0;
    
    do {
        k++;
        current = (int)(nodes[current].next - nodes);
    } while (current != start);
    
    return k;
}

// 8. Поиск по двум полям 
int search_by_value(double v1, char v2[]) {
    int current = head_index;
    int start = head_index;
    int found = 0;
    
    printf("Результаты поиска элементов %.2f \"%s\":\n", v1, v2);
    
    do {
        if (nodes[current].data1 == v1 && strcmp(nodes[current].data2, v2) == 0) {
            printf("  %g %s\n", nodes[current].data1, nodes[current].data2);
            found = 1;
        }
        current = (int)(nodes[current].next - nodes);
    } while (current != start);
    
    if (found) {
        printf("Элементы найдены\n");
        return 1;
    } else {
        printf("Элементы не найдены\n");
        return 0;
    }
}

// 9. Поиск по первому полю 
void search_by_first_value(double v1) {
    if (head_index == -1) {
        printf("Список пуст\n");
        return;
    }
    
    int found = 0;
    int current = head_index;
    int start = head_index;
    
    printf("Результаты поиска:\n");
    
    do {
        if (nodes[current].data1 == v1) {
            printf("  %g %s\n", nodes[current].data1, nodes[current].data2);
            found = 1;
        }
        current = (int)(nodes[current].next - nodes);
    } while (current != start);
    
    if (!found) {
        printf("Элементы не найдены\n");
    }
}

// 10. Поиск по второму полю 
void search_by_second_value(char v2[]) {
    if (head_index == -1) {
        printf("Список пуст\n");
        return;
    }
    
    int found = 0;
    int current = head_index;
    int start = head_index;
    
    printf("Результаты поиска:\n");
    
    do {
        if (strcmp(nodes[current].data2, v2) == 0) {
            printf("  %g %s\n", nodes[current].data1, nodes[current].data2);
            found = 1;
        }
        current = (int)(nodes[current].next - nodes);
    } while (current != start);
    
    if (!found) {
        printf("Элементы не найдены\n");
    }
}

// 11. Удаление элемента 
void delete_element(double v1, char v2[]) {
    // Поиск элемента для удаления
    int prev = -1;
    int current = head_index;
    int start = head_index;
    int found = 0;
    
    do {
        if (nodes[current].data1 == v1 && strcmp(nodes[current].data2, v2) == 0) {
            found = 1;
            
            if (current == head_index) {
                // Удаляем голову - нужно найти последний элемент
                int last = head_index;
                while (nodes[last].next != &nodes[head_index]) {
                    last = (int)(nodes[last].next - nodes);
                }
                // Меняем голову на следующий
                head_index = (int)(nodes[head_index].next - nodes);
                // Последний теперь указывает на новую голову
                nodes[last].next = &nodes[head_index];
            } else {
                // Удаляем не голову
                nodes[prev].next = nodes[current].next;
            }
            
            printf("Элемент удален\n");
            break;
        }
        // Переходим к следующему элементу
        prev = current; 
        current = (int)(nodes[current].next - nodes); 
    } while (current != start && !found); 
    
    if (!found) {
        printf("Элемент не найден\n"); 
    }
}
