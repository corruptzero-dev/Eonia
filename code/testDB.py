# Тестовая версия
import random
import pymysql
import time
import stdiomask

from pymysql.cursors import Cursor
conn = pymysql.connect(host='sql5.freemysqlhosting.net',
                       user='sql5395376',
                       password='XNkiznZYb6',
                       db='sql5395376')
def isBlank (myString):
    if myString and myString.strip():
        return False
    return True

tabler = 'create table userdata (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, nick varchar(40) NOT NULL, passwd varchar(40) NOT NULL, balance SMALLINT UNSIGNED NOT NULL);'
inserter = "INSERT INTO userdata (nick, passwd, balance) VALUES(%s, %s, 1000)"
topInserter = "INSERT INTO topusers (nick, balance) VALUES(%s, %s)"
topSelector = "SELECT COUNT(DISTINCT nick) FROM topusers"
topChecker = "SELECT * FROM topusers WHERE nick = %s"
topBalance = "SELECT balance FROM topusers WHERE nick = %s"
updateTopBalance = "UPDATE topusers SET balance = %s WHERE nick = %s"
getRating = "SELECT nick,balance FROM topusers ORDER BY balance DESC"
deleteRating = "DELETE FROM topusers WHERE nick = %s"
checker = "SELECT * FROM userdata WHERE nick = %s and passwd = %s;"
checkNick = "SELECT * FROM userdata WHERE nick = %s"
checkPasswd = "SELECT * FROM userdata WHERE passwd = %s;"
updatePoints = "UPDATE userdata SET balance = balance + %s WHERE nick = %s"
money = "SELECT balance FROM userdata WHERE nick = %s"
ruleSelector = "SELECT rules FROM gamerules WHERE title = %s"
chooseEvent = "SELECT title FROM events WHERE id = %s"
isEmail = "SELECT email FROM userdata WHERE nick = %s"
countEvents = "SELECT COUNT(*) FROM events"
email = 'SELECT title FROM events WHERE id = 4'
addmail = 'UPDATE userdata SET email = %s WHERE nick = %s'
resetInserter = "INSERT INTO resetemail(nick, passwd, email) VALUES(%s,%s,%s)"
resetCheckPasswd = "SELECT passwd FROM userdata WHERE nick = %s"
checkReset = "SELECT nick FROM resetemail WHERE nick = %s"
getResetList = "SELECT * FROM resetemail"
addBalance = "UPDATE userdata SET balance = %s WHERE nick = %s"
deleteSent = "DELETE FROM resetemail WHERE nick = %s"
delUser = "DELETE FROM userdata WHERE nick = %s"

print('Добро пожаловать в Eonia! Ваш пароль будет скрыт в целях Вашей конфиденциальности.\n')
wrongTries = 0
while True:
    with conn.cursor() as cur:
        cur.execute(countEvents)
        cntev = cur.fetchone()
        numEvents = cntev[0]
    randEvent = random.randint(1,numEvents)
    nick = input('Введите Ваш ник: ').replace(' ', '')
    passwd = stdiomask.getpass('Введите Ваш пароль: ', mask='*').replace(' ', '')
    if conn.cursor().execute(checkNick,(nick)) == False:
        reg = input(f'Пользователя с именем {nick} нет. Хотите ли вы его создать? (Y/N)').lower()
        if reg == 'y':
            while True:
                passwd = stdiomask.getpass('Введите Ваш пароль: ', mask='*')
                check = stdiomask.getpass('Подтвердите Ваш пароль: ', mask = '*')
                if passwd==check:
                    if isBlank(passwd):
                        print('Пароли не могут быть пустыми. Повторите попытку.')
                        continue
                    elif isBlank(checkPasswd):
                        print('\nПароли не могут быть пустыми. Повторите попытку.\n')
                        continue
                    else:
                        conn.cursor().execute(inserter,(nick,passwd))
                        print(f'Регистрация пользователя {nick} прошла успешно!\n')
                        print('Вам требуется войти в аккаунт.\n')
                        conn.commit()
                        break
                elif passwd!=check:
                    print('Пароли не совпадают. Повторите попытку.')
                    continue
                else:
                    print('Неопознанная ошибка.')
                    raise SystemError
        elif reg == 'n':
            print('Хорошо. Возвращаемся в главное меню.')
            continue
    else:
        conn.select_db('sql5395376')
        if conn.cursor().execute(checker,(nick,passwd)):
            with conn.cursor() as cur:
                cur.execute(money, nick)
                balance = cur.fetchone()
                print(f'\nДобро пожаловать, {nick}!\nВаш баланс: {balance[0]}')
                print()
                #close connection!
                break
        else:
            print(f'Неверный пароль для пользователя {nick}. Повторите попытку.')
            wrongTries += 1
            print(wrongTries)
            if wrongTries >= 3:
                resetChoose = input(f'Вы ввели пароль неверно {wrongTries} раз(а). Хотите восстановить? (Y/N): ').lower()
                if resetChoose == 'y':
                    with conn.cursor() as cur:
                        cur.execute(checkReset, nick)
                        checkResetNick = cur.fetchone()
                    if checkResetNick == nick: 
                        print(f'У вас уже есть активный запрос на восстановление пароля для пользователя {nick}.\nПроверьте почту.\n')
                        continue
                    else:
                        with conn.cursor() as cur:
                            cur.execute(isEmail, nick)
                            userEmail = cur.fetchone()
                            if userEmail:
                                with conn.cursor() as cur:
                                    cur.execute(resetCheckPasswd, nick)
                                    oldPass = cur.fetchone()
                                    oldPass = oldPass[0]
                                    userEmail = userEmail[0]
                                    cur.execute(resetInserter,(nick, oldPass, userEmail))
                                    conn.commit()
                                    continue
                            else:
                                print(f'У аккаунта {nick} не привязана электронная почта. Восстановление невозможно.')
                                continue
                else:
                    print('Хорошо.')
                    continue
            else:
                continue
with conn.cursor() as cur:
    cur.execute(isEmail, nick)
    checkMail = cur.fetchone()
    if "@" in checkMail[0]:
        cur.execute(chooseEvent, randEvent)
        event = cur.fetchone()
        print(f'{nick}, для Вас доступно событие: "{event[0]}"')
    else:
        cur.execute(email)
        emailEvent = cur.fetchone()               
        print(f'{nick}, Вам доступно событие: "{emailEvent[0]}"\nЧтобы оставить email, напишите команду "addmail".')
        

print('\nЕсли вы хотите узнать правила или ваш баланс, напишите "rules" или "balance" соответственно на следующем шаге.\nДля вызова рейтинга, напишите "rating".')

# points = 1000     -- NO MORE NEED TO USE GLOBAL VARIABLE points! 

with conn.cursor() as cur:
    cur.execute(money,nick)
    balance = cur.fetchone()
    if balance[0] < 10000: # Реализовано исключение пользователя из таблицы рейтинга.
        if cur.execute(topChecker,nick):
            cur.execute(deleteRating,nick)
            conn.commit()
            print(f'\n{nick}, Ваш баланс составляет {balance[0]} (<10000). Ваш ник был удален из таблицы рейтинга.')
            print('Если вы захотите вернуть Ваш ник в топ, Ваш баланс должен быть больше, чем 10000.')
        else:
            pass
    else:
        pass
    if balance[0] >= 10000:
        if not cur.execute(topChecker,(nick)):
            while True:
                print(f'\n{nick}, Ваш баланс составляет {balance[0]}.\nЭто означает, что для Вас доступно включение Вашего ника в таблицу рейтинга.')
                top = input('Хотите ли вы оставить свое имя в таблице рейтинга? (Y/N): ').lower()
                if top == 'y':
                    cur.execute(topInserter,(nick, balance[0]))
                    conn.commit()
                    cur.execute(topSelector)
                    count = cur.fetchone()
                    print(f'\nБольшое спасибо за участие. Ник "{nick}" был занесен в таблицу рейтинга.')
                    print(f'Сейчас в таблице рейтинга {count[0]} пользователя (-ей). В том числе и Вы :)\nМожете продолжать игру.')
                    break
                elif top == 'n':
                    print('\nХорошо, спасибо. Можете продолжать игру.')
                    break
                else:
                    print('Неизвестная команда, повторите попытку.')
        else:
            cur.execute(topBalance,nick)
            rateBalance = cur.fetchone()
            if rateBalance[0] < balance[0]:
                newBalance = balance[0]
                cur.execute(updateTopBalance,(newBalance,nick))
                conn.commit()
                print(f'\n{nick}, Ваша запись в таблице рейтинга была обновлена ({rateBalance[0]} => {newBalance}).')
            elif rateBalance[0] > balance[0]:
                newBalance = balance[0]
                cur.execute(updateTopBalance,(newBalance,nick))
                conn.commit()
                print(f'\n{nick}, Ваша запись в таблице рейтинга была обновлена ({rateBalance[0]} => {newBalance}).')
            else:
                pass
    else:
        pass
    eventCounter = 0
    userChoice = ''
    while balance[0] > 0:
        with conn.cursor() as cur:
            def checkEvent1(a,b,c):
                if randEvent == 3:
                    if userChoice == 'б':
                        if (a+b+c) >= 1000:
                            print('Вы выполнили задание. 150 было начислено на Ваш счет.')
                            global eventCounter
                            eventCounter += 1
                            cur.execute(updatePoints,(150,nick))      #This works!!!!!!!!
                            conn.commit()
                        else:
                            pass
                elif randEvent == 1:
                    if (a+b+c)>=1000:
                        print('Вы выполнили задание. 100 было начислено на Ваш счет.')
                        eventCounter += 1
                        cur.execute(updatePoints,(100,nick))      #This works!!!!!!!!
                        conn.commit()
                    else:
                        pass
                elif randEvent == 2:
                    if userChoice == 'м':
                        if (a+b+c) >= 500:
                            print('Вы выполнили задание. 150 было начислено на Ваш счет.')
                            eventCounter += 1
                            cur.execute(updatePoints,(150,nick))      #This works!!!!!!!!
                            conn.commit()
                        else:
                            pass
                elif randEvent == 4:
                    pass
                elif randEvent == 5:
                    if userChoice == 'у':
                        if (a+b+c) >= 500:
                            print('Вы выполнили задание. 200 было начислено на Ваш счет.')
                            eventCounter += 1
                            cur.execute(updatePoints,(200,nick))      #This works!!!!!!!!
                            conn.commit()
                        else:
                            pass
                else:
                    pass
            cur.execute(money,nick)
            balance = cur.fetchone()
            userChoice = input('\nВыберите, в какой режим вы хотите сыграть:\nБомбы, Угадай число, Монетка(Б/У/М): ').lower()
            if userChoice == 'rules':
                while True:
                    ruleChoose = input('\nХорошо. Правила какого режима вы хотите посмотреть? (Или напишите "cancel", чтобы выйти.) \nБомбы,Монетка,Угадай число(B/C/G): ').lower()
                    if ruleChoose == "b":
                        cur.execute(ruleSelector,"Bombs")
                        ruleBombs = cur.fetchone()
                        print(f'\n{ruleBombs[0]}')
                        continue
                    elif ruleChoose == "c":
                        cur.execute(ruleSelector,"Coin")
                        ruleBombs = cur.fetchone()
                        print(f'\n{ruleBombs[0]}')
                        continue
                    elif ruleChoose == "g":
                        cur.execute(ruleSelector,"GN")
                        ruleBombs = cur.fetchone()
                        print(f'\n{ruleBombs[0]}')
                        continue
                    elif ruleChoose == "cancel":
                        break
                    else:
                        print('Неверный ввод, повторите попытку.')
                        continue
                continue
            elif userChoice == 'admin':
                while True:
                    if nick in ('corruptzero', 'Ilya', 'klim'):
                        print(f'{nick}, вы вошли в режим администрирования. Чтобы выйти, напишите "logout"\n')
                        adminChoose = input('Что Вы хотите сделать? Напишите "help", чтобы узнать все возможности: ').lower()
                        if adminChoose == 'help':
                            print('''
                            Команды администрирования:
                            1. "getReset" - получить файл с пользователями, подавшими заявку на reset.
                            2. "comReset" - удалить пользователей из resetEmail.
                            3. "addBalance" - добавить баланс пользователю.
                            4. "delUser" - удалить пользователя из таблицы userData. (ОСТОРОЖНО)
                            5. "addUser" - добавить пользователя в таблицу userData.
                            ''')
                        elif adminChoose == 'getreset':
                            cur.execute(getResetList)
                            resetList = cur.fetchall()
                            file = open("reset.txt", "w")
                            numResets = 0
                            for i in resetList:
                                file.write(f'{i[1]}, {i[2]}, {i[3]}')
                                file.write(f'\n')
                                numResets += 1
                            file.close()
                            print(f'{nick}, в файл "reset.txt" было добавлено {numResets} записи(-ей).')
                            continue
                        elif adminChoose == 'comreset':
                            confirm = input('Вы уверены, что хотите удалить пользователей из базы resetEmail и текстового файла? (Y/N): ').lower()
                            if confirm == 'y':
                                filer = open("reset.txt", "r+")
                                sent = filer.read()
                                sent = sent.replace('\n', ',').replace(' ', '').split(',')
                                sent.pop()
                                comResetNicks = []
                                ind = 0
                                for i in sent:
                                    try:
                                        comResetNicks.append(sent[ind])
                                        ind += 3
                                    except IndexError:
                                        print(f'{len(comResetNicks)} ника(-ов) добавлены в очередь для удаления.')
                                        break
                                for i in comResetNicks:
                                    cur.execute(deleteSent,i)
                                conn.commit()
                                print(f'Было удалено {len(comResetNicks)} ника(-ов) из БД resetemail.')
                                filer.truncate(0)
                                filer.close()
                            else:
                                print('Отмена.')
                                continue
                        elif adminChoose == 'addbalance':
                            adminUser = input('Введите ник пользователя: ')
                            adminBal = input(f'Введите баланс для пользователя {adminUser}: ')
                            cur.execute(money,adminUser)
                            oldMoney = cur.fetchone()
                            cur.execute(addBalance,(adminBal,adminUser))
                            conn.commit()
                            print(f'{nick}, баланс пользователя {adminUser} был изменен ({oldMoney[0]} => {adminBal})')
                            continue
                        elif adminChoose == 'adduser':
                            addUserNick = input('Введите ник: ')
                            addUserPasswd = input('Введите пароль: ')
                            cur.execute(inserter,(addUserNick,addUserPasswd))
                            conn.commit()
                            print(f'Был создан пользователь с ником {addUserNick} и паролем {addUserPasswd}.')
                            continue
                        elif adminChoose == 'deluser':
                            confirm = input('Вы уверены, что хотите удалить пользователя? (Y/N): ').lower()
                            if confirm == 'y':
                                delNick = input('Введите ник пользователя, которого нужно удалить: ')
                                if cur.execute(checkNick,delNick):
                                    cur.execute(delUser,delNick)
                                    print(f'Пользователь с ником {delNick} был удален.')
                                    conn.commit()
                                    continue
                                else:
                                    print('Такого пользователя нет.')
                                    continue
                            else:
                                print('Отмена.')
                                continue
                        elif adminChoose == 'logout':
                            print(f'{nick}, вы вышли из режим администрирования.')
                            break
                    else:
                        print('Доступ запрещен.')
                        break
                continue
            elif userChoice == 'addmail':
                cur.execute(isEmail,nick)
                mail = cur.fetchone()
                if "@" in mail:
                    changeMail = input(f'{nick}, у Вас уже добавлен email. Вы хотите изменить его? (Y/N)').lower()
                    if changeMail == 'y':
                        newMail = input('Введите Ваш новый email: ').replace(' ','')
                        if isBlank(newMail):
                            print('Email не может быть пустым. Повторите попытку.')
                            continue
                        elif '@' not in newMail:
                            print('Это не похоже на email. Повторите попытку.')
                            continue
                        else:
                            commitMail = input(f'Для пользователя {nick} будет изменен email "{mail[0]}". Верно? (Y/N)').lower()
                            if commitMail == 'y':
                                cur.execute(addmail,(newMail,nick))
                                conn.commit()
                                print(f'Email "{newMail}" был привязан к пользователю {nick}.')
                                print(f'Спасибо! Ваш email был изменен("{mail[0]}"=>"{newMail}")')
                                continue
                            elif commitMail == 'n':
                                print('Хорошо. Возращаемся в главное меню.')
                                continue
                    elif changeMail == 'n':
                        print('Хорошо. Возращаемся в главное меню.')
                        continue
                else:
                    userMail = input('Введите Ваш email: ').replace(' ','')
                    if isBlank(userMail):
                        print('Email не может быть пустым. Повторите попытку.')
                        continue
                    elif '@' not in userMail:
                        print('Это не похоже на email. Повторите попытку.')
                        continue
                    else:
                        commitMail = input(f'Для пользователя {nick} будет установлен email "{userMail}". Верно? (Y/N)').lower()
                        if commitMail == 'y':
                            cur.execute(addmail,(userMail,nick))
                            conn.commit()
                            print(f'Email "{userMail}" был привязан к пользователю {nick}.')
                            cur.execute(updatePoints,(1000,nick))
                            conn.commit()
                            print('Спасибо! Вам начислено: 1000')
                            continue
                        elif commitMail == 'n':
                            print('Хорошо. Возращаемся в главное меню.')
                            continue
            elif userChoice == 'rating':
                cur.execute(getRating)
                rating = cur.fetchall()
                try:
                    firstPlace = rating[0]
                    print(f'1 место: {firstPlace[0]} - {firstPlace[1]}')
                except IndexError:
                    print('1 место: пусто.')
                try:
                    secondPlace = rating[1]
                    print(f'2 место: {secondPlace[0]} - {secondPlace[1]}')
                except IndexError:
                    print('2 место: пусто.')
                try:
                    thirdPlace = rating[2]
                    print(f'3 место: {thirdPlace[0]} - {thirdPlace[1]}')
                except IndexError:
                    print('3 место: пусто.')
                continue
            elif userChoice == 'exit':
                print(f'Производится выход из аккаунта {nick}...')
                conn.close()
                time.sleep(1)
                print('____________________________')
                print('Будем рады видеть Вас снова.')
                break
            elif userChoice == 'balance':
                cur.execute(money,nick)
                balance = cur.fetchone()
                print(f'Ваш баланс: {balance[0]}')
                continue
            elif userChoice not in ('б','у','м','exit','rating','addmail'):
                print('\nТакого режима нет. Повторите попытку.')
                continue
            bet = int(input('Введите ставку: '))
            if bet > balance[0]:
                print('Недостаточно средств. Повторите попытку.\n')
                continue
            elif bet <= 0:
                print('Ставка должна быть больше нуля!\n')
                continue
            else:
                if userChoice == "б":
                    bomb = random.randint(1,5)
                    userBomb = int(input("В одной из пяти ячеек лежит бомба.\nУгадайте ячейку, в которой её НЕТ: "))
                    if int(userBomb) in range (1,6):
                        if userBomb == bomb:
                            print('Вы взорвались!\n')
                            print(f'Вы проиграли: {bet}')
                            lose1 = -bet
                            cur.execute(updatePoints,(lose1,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Ваш баланс: {balance[0]}')
                            continue
                        else:
                            print('Верно!\n')
                            print(f'Вы выиграли: {bet*0.2}')
                            win1 = bet*0.2
                            print(f'Бомба была в ячейке: {bomb} \n')
                            cur.execute(updatePoints,(win1,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Ваш баланс: {balance[0]}')
                            cont = input("Хотите продолжить?(Y/N): ").lower()
                            if cont == "y":
                                bomb2 = random.randint(1,3)
                                userBomb2 = int(input("В одной из трех ячеек лежит бомба. \nУгадайте ячейку, в которой её НЕТ: "))
                                if int(userBomb2) in range (1,4):
                                    if userBomb2 == bomb2:
                                        print('Вы взорвались!\n')
                                        lose2 = -(bet*1.2)
                                        print(f'Вы проиграли: {bet*1.2}')
                                        cur.execute(updatePoints,(lose2,nick))      #This works!!!!!!!!
                                        conn.commit()
                                        cur.execute(money,nick)
                                        balance = cur.fetchone()
                                        continue
                                    else:
                                        print(f'Вы выиграли: {bet*0.3}')
                                        win2 = bet*0.3
                                        print(f'Бомба была в ячейке: {bomb2} \n')
                                        cur.execute(updatePoints,(win2,nick))      #This works!!!!!!!!
                                        conn.commit()
                                        cur.execute(money,nick)
                                        balance = cur.fetchone()
                                    cont2 = input("Хотите продолжить?(Y/N): ").lower()
                                    if cont2 =="y":
                                        bomb3 = random.randint(1,2)
                                        userBomb3 = int(input("\nВ одной из двух ячеек лежит бомба. \nУгадайте ячейку, в которой её НЕТ: "))
                                        if int(userBomb3) in range (1,3):
                                            if userBomb3 == bomb3:
                                                print('Вы взорвались!\n')
                                                lose3 = -(bet*1.5)
                                                print(f'Вы проиграли: {bet*1.5}')
                                                cur.execute(updatePoints,(lose3,nick))      #This works!!!!!!!!
                                                conn.commit()
                                                cur.execute(money,nick)
                                                balance = cur.fetchone()
                                                print(f'Ваш баланс: {balance[0]}')
                                                continue
                                            else:
                                                print(f'Вы выиграли: {bet*2.5}')
                                                print(f'Бомба была в ячейке: {bomb3} \n')
                                                print('Победитель!')
                                                win3 = bet*2.5
                                                cur.execute(updatePoints,(win3,nick))      #This works!!!!!!!!
                                                conn.commit()
                                                cur.execute(money,nick)
                                                balance = cur.fetchone()
                                                if eventCounter == 0:
                                                    checkEvent1(win1,win2,win3)
                                                else:
                                                    pass
                                                print(f'Ваш баланс: {balance[0]}')
                                        else:
                                            print('Неверный ввод. Повторите попытку.\n')
                                            continue
                                    else:
                                        print('Спасибо за игру.')
                                        if eventCounter == 0:
                                            checkEvent1(win1,win2, 0)
                                        else:
                                            pass
                                        print(f'Ваш баланс: {balance[0]}')
                                        continue
                                else:
                                    print('Неверный ввод. Повторите попытку.\n')
                                    continue
                            else:
                                print('Спасибо за игру.')
                                if eventCounter == 0:
                                    checkEvent1(win1, 0, 0)
                                else:
                                    pass
                                print(f'Ваш баланс: {balance[0]}')
                                continue
                    else:
                        print('Неверный ввод. Повторите попытку.\n')
                        continue
                elif userChoice == "м":
                    try:
                        userCoin = int(input("\nВыберите: Орёл или Решка\nОрел - 0, Решка - 1: "))
                        coin = random.randint(0, 1)
                        if userCoin not in (0, 1):
                            print('\nНеверно введены данные!')
                            continue
                        elif userCoin == coin:
                            print("Верно!")
                            print(f'Вы выиграли: {bet}')
                            winCoin = bet
                            cur.execute(updatePoints,(winCoin,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            # conn.close()
                            if eventCounter == 0:
                                checkEvent1(winCoin,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        else:
                            print("Не повезло...")
                            print(f'Вы проиграли: {bet}')
                            loseCoin = -(bet)
                            cur.execute(updatePoints,(loseCoin,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            # conn.close()
                            print(f'Ваш баланс: {balance[0]}')
                    except ValueError:
                        print('\nНеверно введены данные!')
                        continue
                elif userChoice == 'у':
                    number = random.randint(1, 100)
                    secret_number = random.randint(1,100)
                    user_answer = input(f'\nБыло загадано число {number}, также было загадано второе число.\nУгадайте, больше оно, меньше, или равно {number} (Б/М/Р): ').lower()
                    if user_answer == 'б' and number < secret_number:
                        if number in range (1, 11) or number in range(90, 101):
                            numWinb1 = bet * 0.1
                            cur.execute(updatePoints,(numWinb1,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.1}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinb1,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (10, 25) or number in range(75, 90):
                            numWinb2 = bet * 0.25
                            cur.execute(updatePoints,(numWinb2,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.25}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinb2,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (25, 75):
                            numWinb3 = bet
                            cur.execute(updatePoints,(numWinb3,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinb3,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        else:
                            print('Ошибка, повторите попытку.')
                    elif user_answer == 'м' and number > secret_number:
                        if number in range (1, 11) or number in range(90, 101):
                            numWinm1 = bet * 0.1
                            cur.execute(updatePoints,(numWinm1,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.1}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinm1,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (10, 25) or number in range(75, 90):
                            numWinm2 = bet * 0.25
                            cur.execute(updatePoints,(numWinm2,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.25}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinm2,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (25, 75):
                            numWinm3 = bet
                            cur.execute(updatePoints,(numWinm3,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet}')
                            print(f'Выпало число: {secret_number}')
                            if eventCounter == 0:
                                checkEvent1(numWinm3,0,0)
                            else:
                                pass
                            print(f'Ваш баланс: {balance[0]}')
                        else:
                            print('Ошибка, повторите попытку.')
                    elif user_answer == 'р' and number == secret_number:
                        numWineq = bet * 100
                        cur.execute(updatePoints,(numWineq,nick))      #This works!!!!!!!!
                        conn.commit()
                        cur.execute(money,nick)
                        balance = cur.fetchone()
                        print('Ничего себе!')
                        print(f'Вы выиграли: {bet * 100}')
                        print(f'Выпало число: {secret_number}')
                        if eventCounter == 0:
                                checkEvent1(numWineq,0,0)
                        else:
                            pass
                        print(f'Ваш баланс: {balance[0]}')
                    elif user_answer == 'б' and number > secret_number:
                        numLoseb = -(bet)
                        cur.execute(updatePoints,(numLoseb,nick))      #This works!!!!!!!!
                        conn.commit()
                        cur.execute(money,nick)
                        balance = cur.fetchone()
                        print(f'Вы проиграли: {bet}')
                        print(f'Выпало число: {secret_number}')
                        print(f'Ваш баланс: {balance[0]}')
                    elif user_answer == 'м' and number < secret_number:
                        numLosem = -(bet)
                        cur.execute(updatePoints,(numLosem,nick))      #This works!!!!!!!!
                        conn.commit()
                        cur.execute(money,nick)
                        balance = cur.fetchone()
                        print(f'Вы проиграли: {bet}')
                        print(f'Выпало число: {secret_number}')
                        print(f'Ваш баланс: {balance[0]}')
                    elif user_answer == 'р' and number != secret_number:
                        numLoseeq = -(bet)
                        cur.execute(updatePoints,(numLoseeq,nick))      #This works!!!!!!!!
                        conn.commit()
                        cur.execute(money,nick)
                        balance = cur.fetchone()
                        print('Не повезло...')
                        print(f'Вы проиграли: {bet}')
                        print(f'Выпало число: {secret_number}')
                        print(f'Ваш баланс: {balance[0]}')
                    else:
                        print('Неверный ввод, повторите попытку!')
                        continue
    if balance[0] <= 0:
        print('\nУ вас закончились средства! Создайте новый аккаунт или обратитесь к администратору.')
    else:
        pass
    # except Exception:
    #   pass

#тип данных строка для ввода ставки

#угадай число пофиксить меньше (Угадайте, больше оно, меньше, или равно 82 (Б/М/Р): м Неверный ввод, повторите попытку!)

#Добавить ивент: подбросить монетку 3 раза подряд

#Добавить ивент: пройти бомбы до конца
