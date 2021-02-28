# Тестовая версия
import random
import pymysql
import time

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

while True:
    nick = input('Введите Ваш ник: ').replace(' ', '')
    passwd = input('Введите Ваш пароль: ').replace(' ', '')
    if conn.cursor().execute(checkNick,(nick)) == False:
        reg = input(f'Пользователя с именем {nick} нет. Хотите ли вы его создать? (Y/N)').lower()
        if reg == 'y':
            while True:
                passwd = input('Введите Ваш пароль: ')
                check = input('Подтвердите Ваш пароль: ')
                if passwd==check:
                    if isBlank(passwd):
                        print('Пароли не могут быть пустыми. Повторите попытку.')
                        continue
                    elif isBlank(checkPasswd):
                        print('\nПароли не могут быть пустыми. Повторите попытку.\n')
                        continue
                    else:
                        conn.cursor().execute(inserter,(nick,passwd))
                        print(f'Регистрация пользователя {nick} прошла успешно!')
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
                #close connection!
                break
        else:
            print(f'Неверный пароль для пользователя {nick}. Повторите попытку.')
            continue

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
    while balance[0] > 0:
        with conn.cursor() as cur:
            cur.execute(money,nick)
            balance = cur.fetchone()
            userChoice = input('\nВыберите, в какой режим вы хотите сыграть:\nБомбы, Угадай число, Монетка(Б/У/М): ').lower()
            if userChoice == 'rules':
                print('''Правила:
        Бомбы: Случайным образом было загадано число(N) в указанном промежутке.
                Вам требуется угадать одно из остальных чисел, кроме N.
                С каждым шагом интервал будет уменьшаться, но и выигрыш будет увеличиваться соответственно шансу.
        Угадай число: Компьютером будет загадано одно число(A), 
                      которое доступно только ему, а также будет сгенерировано второе число, которое вы будете видеть на экране(B).
                      Ваша задача угадать, окажется ли число A больше, меньше либо равно B.
                      Чем ближе число B к 50, тем сложнее угадать, и тем больше ваш выигрыш в случае победы.
        Монетка: Суть игры довольно проста, "подкидывается монетка" и нужно угадать, какая сторона окажется сверху.
                  В данном режиме, в случае выигрыша ставки удваиваются.
                  ______________________________________________________
                  Чтобы выйти из игры, в любой момент напишите "exit".''')
                print('                                   Желаем Удачи!\n')
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
            elif userChoice not in ('б','у','м','exit','rating'):
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
                                        print(f'Ваш баланс: {balance[0]}')
                                        continue
                                    else:
                                        print(f'Вы выиграли: {bet*0.3}')
                                        win2 = bet*0.3
                                        print(f'Бомба была в ячейке: {bomb2} \n')
                                        cur.execute(updatePoints,(win2,nick))      #This works!!!!!!!!
                                        conn.commit()
                                        cur.execute(money,nick)
                                        balance = cur.fetchone()
                                        print(f'Ваш баланс: {balance[0]}')
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
                                                print(f'Ваш баланс: {balance[0]}')
                                        else:
                                            print('Неверный ввод. Повторите попытку.\n')
                                            continue
                                    else:
                                        print('Спасибо за игру.')
                                        continue
                                else:
                                    print('Неверный ввод. Повторите попытку.\n')
                                    continue
                            else:
                                print('Спасибо за игру.')
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
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (10, 25) or number in range(75, 90):
                            numWinb2 = bet * 0.25
                            cur.execute(updatePoints,(numWinb2,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.25}')
                            print(f'Выпало число: {secret_number}')
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (25, 75):
                            numWinb3 = bet
                            cur.execute(updatePoints,(numWinb3,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet}')
                            print(f'Выпало число: {secret_number}')
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
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (10, 25) or number in range(75, 90):
                            numWinm2 = bet * 0.25
                            cur.execute(updatePoints,(numWinm2,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet * 0.25}')
                            print(f'Выпало число: {secret_number}')
                            print(f'Ваш баланс: {balance[0]}')
                        elif number in range (25, 75):
                            numWinm3 = bet
                            cur.execute(updatePoints,(numWinm3,nick))      #This works!!!!!!!!
                            conn.commit()
                            cur.execute(money,nick)
                            balance = cur.fetchone()
                            print(f'Вы выиграли: {bet}')
                            print(f'Выпало число: {secret_number}')
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

#Монетка реализовать опечатку в выборе стороны