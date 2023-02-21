import sqlite3
MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

def display_menu():
    """Функция вывода на экран главного меню"""
    print('n-----Меню введения учета инструментов')
    print('1. Создать новую позицию')
    print('2. Прочитать позицию')
    print('3. Обновить позицию')
    print('4. Удалить позицию')
    print('5. Выйти из программы')

def get_menu_choice():
    """ Функция позволяет получить от пользователя пункт меню"""
    choice = int(input('Введите ваш вариант: '))
    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Допустимые варианты таковы: {MIN_CHOICE} - {MAX_CHOICE}.')
        choice = int(input('Введите ваш вариант: '))

    return choice

def create():
    """Функция создания новой позиции"""
    print('Создать новую позицию')
    name = input('Название позиции: ')
    price = input('Цена: ')
    insert_row(name, price)

def read():
    """Чтение существующей позиции"""
    name = input('Введите название искомой позиции: ')
    num_found = display_item(name)
    print(f'{num_found} строк(а) найдено. ')


def update():
    """Функция обновляет данные существующей позиции"""
    read() # показываем пользователю найденные строки
    selected_id = int(input('Выберите ID обновляемой позиции: ')) # получить ID обновляемой позиции

    # получаем новые данные для обновления
    name = input('Введите новое название позиции: ')
    price = input('Введите новую цену: ')

    # Обновляем строку
    num_updated = update_row(selected_id, name, price)
    print(f'{num_updated} строк(а) обновлено')

def delete():
    """Функция удаления позиции"""
    read() # показываем пользователю найденные строки
    selected_id = int(input('Выберите ID обновляемой позиции: ')) #получить ID обновляемой позиции
    # Подтверждаем удаление
    sure = input('Вы уверена, что хотите удалить эту позицию? (да/нет): ')
    if sure.lower() == 'да':
        num_deleted = delete_row(selected_id)
        print(f'{num_deleted} строк(а) удалено')

def insert_row(name, price):
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Inventory (ItemName, Price) VALUES (?,?)''', (name, price))
        conn.commit()
    except sqlite3.Error as err:
        print('Ошибка базы данныых', err)
    finally:
        if conn != None:
            conn.close()

def display_item(name):
    """Выводит на экран все позиции с совпадающими названиями позиций"""
    conn = None
    results =[]
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Inventory WHERE ItemName == ?''', (name,))
        results = cur.fetchall()

        for row in results:
            print(f'ID: {row[0]:<3} Название: {row[1]:<15}'
                  f'Цена: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
            return len(results) #возвращает число совпавших строк


def update_row(id, name, price):
    """Обновляет существующее значение новым названием и ценой. Возвращает обновленное число строк"""
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Inventory SET ItemName = ?, Price = ? WHERE ID == ?''', (name, price, id))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
            return num_updated



def delete_row(id):
    '''Удаляет существующую позицию. Возвращает число удаленных строк'''
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Inventory WHERE ID == ?''', (id, ))
        conn.commit()
        num_delete2 = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    except:
        print('Странная ошибка, не связана с базой данных')
    finally:
        if conn != None:
            conn.close()
        return num_delete2

def main():
    '''Главная функция программы'''
    choice = 0
    while choice != EXIT:
        display_menu() # обращаемсяк функции display menu, с помощью которой на экран выводится меню
        choice = get_menu_choice() #обращаемся к функции, позволяющей получить данные от пользователя

        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()

if __name__ == '__main__':
    main()
