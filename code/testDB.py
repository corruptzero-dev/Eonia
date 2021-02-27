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
checker = "SELECT * FROM userdata WHERE nick = %s and passwd = %s;"
checkNick = "SELECT * FROM userdata WHERE nick = %s"
checkPasswd = "SELECT * FROM userdata WHERE passwd = %s;"
updatePoints = "UPDATE userdata SET balance = balance + %s WHERE nick = %s"
money = "SELECT balance FROM userdata WHERE nick = %s"

while True:
    nick = input('Введите Ваш ник: ').replace(' ', '')
    passwd = input('Введите Ваш пароль: ').replace(' ', '')
    if passwd and nick:
        if not conn.cursor().execute(checker,(nick,passwd)):
            conn.select_db('sql5395376')
            conn.cursor().execute(inserter,(nick,passwd))
            conn.commit()
            print(f'Регистрация пользователя {nick} прошла успешно!')
            #close connection!
            break
        else:
            conn.select_db('sql5395376')        
            if conn.cursor().execute(checker,(nick,passwd)):
                print(f'\nДобро пожаловать, {nick}!')
                #close connection!
                break
            else:
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
                    #close connection!
                    break
                            
                elif conn.cursor().execute(checkPasswd,(passwd)) == False:
                    print(f'Неверный пароль для пользователя {nick}. Повторите попытку.')
                    continue
    else:
        print('Пароль и/или ник не могут быть пустыми. Повторите попытку.')
        continue
print('\nЕсли вы хотите узнать правила или ваш баланс, напишите "rules" или "balance" соответственно на следующем шаге.')

# def getBalance():
#   with conn.cursor() as cur:                      
#     cur.execute(money,nick)
#     balance = cur.fetchone()
#     print(f'Ваш баланс: {balance[0]}')
#     return balance[0]

# points = 1000     -- NO MORE NEED TO USE GLOBAL VARIABLE points! 

with conn.cursor() as cur:                      
  cur.execute(money,nick)
  balance = cur.fetchone()
  while balance[0] > 0:
    if balance[0] <= 0:
      print('У вас закончились средства! Создайте новый аккаунт или обратитесь к администратору.')
      break
    else:
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
        elif userChoice not in ('б','у','м','exit','logout'):
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
                print('Вы проиграли: ' + str(bet))
                lose1 = -bet
                cur.execute(updatePoints,(lose1,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print(f'Ваш баланс: {balance[0]}')
                continue
              else:
                print('Верно!\n')
                print('Вы выиграли: ' + str(bet*0.2))
                # points += bet*0.2
                win1 = bet*0.2
                print('Бомба была в ячейке: ' + str(bomb) + '\n')
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
                      # points -= bet*1.2
                      lose2 = -(bet*1.2)
                      print('Вы проиграли: '+ str(bet*1.2))
                      cur.execute(updatePoints,(lose2,nick))      #This works!!!!!!!!
                      conn.commit()
                      cur.execute(money,nick)
                      balance = cur.fetchone()
                      print(f'Ваш баланс: {balance[0]}')
                      continue
                    else:
                      print('Вы выиграли: ' + str(bet*0.3))
                      # points += bet*0.3
                      win2 = bet*0.3
                      print('Бомба была в ячейке: '+ str(bomb2) + '\n')
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
                          # points -= bet*1.5
                          lose3 = -(bet*1.5)
                          print('Вы проиграли: '+ str(bet*1.5))
                          cur.execute(updatePoints,(lose3,nick))      #This works!!!!!!!!
                          conn.commit()
                          cur.execute(money,nick)
                          balance = cur.fetchone()
                          print(f'Ваш баланс: {balance[0]}')
                          continue
                        else:
                          print('Вы выиграли: ' + str(bet*2.5))
                          # points += bet*2.5
                          print('Бомба была в ячейке: ' + str(bomb) + '\n')
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
            userCoin = int(input("\nВыберите: Орёл или Решка\nОрел - 0, Решка - 1: "))
            coin = random.randint(0, 1)
            if userCoin not in (0, 1):
              print('\nНеправильно введены данные!')
              continue
            elif userCoin == coin:
              print("Верно!")
              print('Вы выиграли: ' + str(bet))
              winCoin = bet
              cur.execute(updatePoints,(winCoin,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              # conn.close()
              # print(conn.cursor().execute(money,nick))          #Returns 1 - need to fix
              print(f'Ваш баланс: {balance[0]}')
            else:
              print("Не повезло...")
              print('Вы проиграли: ' + str(bet))
              loseCoin = -(bet)
              cur.execute(updatePoints,(loseCoin,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              # conn.close()
              # print(conn.cursor().execute(money,nick))     #Returns 1 - need to fix
              print(f'Ваш баланс: {balance[0]}')
          elif userChoice == 'у':
            number = random.randint(1, 100)
            secret_number = random.randint(1,100)
            user_answer = input('\nБыло загадано число ' + str(number) + ', также было загадано второе число.\nУгадайте, больше оно, меньше, или равно ' + str(number) + ' ' + '(Б/М/Р): ').lower()
            if user_answer == 'б' and number < secret_number:
              if number in range (1, 11) or number in range(90, 101):
                # points += bet * 0.1
                numWinb1 = bet * 0.1
                cur.execute(updatePoints,(numWinb1,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet * 0.1))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              elif number in range (10, 25) or number in range(75, 90):
                # points += bet * 0.25
                numWinb2 = bet * 0.25
                cur.execute(updatePoints,(numWinb2,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet * 0.25))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              elif number in range (25, 75):
                # points += bet
                numWinb3 = bet
                cur.execute(updatePoints,(numWinb3,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              else:
                print('Ошибка, повторите попытку.')
            elif user_answer == 'м' and number > secret_number: 
              if number in range (1, 11) or number in range(90, 101):
                # points += bet * 0.1
                numWinm1 = bet * 0.1
                cur.execute(updatePoints,(numWinm1,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet * 0.1))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              elif number in range (10, 25) or number in range(75, 90):
                # points += bet * 0.25
                numWinm2 = bet * 0.25
                cur.execute(updatePoints,(numWinm2,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet * 0.25))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              elif number in range (25, 75):
                # points += bet
                numWinm3 = bet 
                cur.execute(updatePoints,(numWinm3,nick))      #This works!!!!!!!!
                conn.commit()
                cur.execute(money,nick)
                balance = cur.fetchone()
                print('Вы выиграли: ' + str(bet))
                print('Выпало число: ' + str(secret_number))         
                print(f'Ваш баланс: {balance[0]}')
              else:
                print('Ошибка, повторите попытку.')
            elif user_answer == 'р' and number == secret_number:
              # points = bet * 100
              numWineq = bet * 100
              cur.execute(updatePoints,(numWineq,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              print('Ничего себе!')
              print('Вы выиграли: ' + str(bet * 100))
              print('Выпало число: ' + str(secret_number))         
              print(f'Ваш баланс: {balance[0]}')
            elif user_answer == 'б' and number > secret_number:
              # points -= bet
              numLoseb = -(bet) 
              cur.execute(updatePoints,(numLoseb,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              print('Вы проиграли: ' + str(bet))
              print('Выпало число: ' + str(secret_number))         
              print(f'Ваш баланс: {balance[0]}')
            elif user_answer == 'м' and number < secret_number:
              # points -= bet
              numLosem = -(bet) 
              cur.execute(updatePoints,(numLosem,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              print('Вы проиграли: ' + str(bet))
              print('Выпало число: ' + str(secret_number))         
              print(f'Ваш баланс: {balance[0]}')
            elif user_answer == 'р' and number != secret_number:
              # points -= bet
              numLoseeq = -(bet) 
              cur.execute(updatePoints,(numLoseeq,nick))      #This works!!!!!!!!
              conn.commit()
              cur.execute(money,nick)
              balance = cur.fetchone()
              print('Не повезло...')
              print('Вы проиграли: ' + str(bet))
              print('Выпало число: ' + str(secret_number))         
              print(f'Ваш баланс: {balance[0]}')
            else:
              print('Неверный ввод, повторите попытку!')
              continue
          
  # except Exception:
  #   pass

#Убрать пробелы из ников