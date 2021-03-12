sqlInput = input('Вы хотите изменить данные для входа? (Y/N)').lower()
    if sqlInput == 'y':
        checkSqlAdm = input('Введите Ваше имя: ')
        if checkSqlAdm in ('klim', 'Ilya', 'corruptzero'):
            checkSqlPass = input('Введите Ваш пароль: ')
            if checkSqlPass == 'EoniaOneLove2021!':
                sqlHost = input('Введите хост: ')
                sqlUser = input('Введите юзера: ')
                sqlPasswd = input('Введите пароль: ')
                sqlDb = input('Введите имя БД: ')
                #Создать запросы для создания таблиц и вставки в них данных.
                print('Данные добавлены. Если все прошло успешно, тогда Вас попросят ввести пароль.\n')
            else:
                print('Неверный пароль.') 
        else:
            print('Неверное имя. Если вы не админ, обратитесь к администратору.')