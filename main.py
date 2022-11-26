

def main():
    action = 1
    try:
        action = int(input("[Авторизация] Выберите: 1 - Администратор, 2 - Студент и нажмите ENTER\n>>> "))
    except ValueError:
        exit("[Ошибка] Введите число")
    if action == 1:
        key = input("Введите ключ доступа >>> ")
        if key == "4444":

    elif action == 2:
        pass
    else:
        exit("[Ошибка] 1 или 2. Программа завершила работу")
if __name__ == '__main__':
    main()