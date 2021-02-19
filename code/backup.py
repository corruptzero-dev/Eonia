import random

points = 1000 #Вынести в бд
print('\nЕсли вы хотите узнать правила, напишите "rules" на следующем шаге.\n')
while points > 0:
  try:
    if points <= 0:
      print('У вас закончились средства! Перезапустите программу.')
      break
    else:
      userChoice = input('Выберите, в какой режим вы хотите сыграть:\nБомбы, Угадай число, Монетка(Б/У/М): ').lower()
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
                  В данном режиме, в случае выигрыша ставки удваиваются.''')
        print('                               Желаем Удачи!\n')
        continue
      bet = int(input('Введите ставку: '))
      if bet > points:
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
              points -= bet
              print('Вы проиграли: ' + str(bet))
              print(points)
              continue
            else:
              print('Верно!\n')
              print('Вы выиграли: ' + str(bet*0.2))
              points += bet*0.2
              print('Бомба была в ячейке: ' + str(bomb) + '\n')
              print('Ваш текущий баланс: ' + str(points))
              cont = input("Хотите продолжить?(Y/N): ").lower()
              if cont == "y":
                bomb2 = random.randint(1,3)
                userBomb2 = int(input("В одной из трех ячеек лежит бомба. \nУгадайте ячейку, в которой её НЕТ: "))
                if int(userBomb2) in range (1,4):
                  if userBomb2 == bomb2:
                    print('Вы взорвались!\n')
                    points -= bet*1.2
                    print('Вы проиграли: '+ str(bet*1.2))
                    print('Ваш текущий баланс: ' + str(points))
                    continue
                  else:
                    print('Вы выиграли: ' + str(bet*0.3))
                    points += bet*0.3
                    print('Бомба была в ячейке: '+ str(bomb2) + '\n')
                    print('Ваш текущий баланс: ' + str(points))
                  cont2 = input("Хотите продолжить?(Y/N): ").lower()
                  if cont2 =="y":
                    bomb3 = random.randint(1,2)
                    userBomb3 = int(input("\nВ одной из двух ячеек лежит бомба. \nУгадайте ячейку, в которой её НЕТ: "))
                    if int(userBomb3) in range (1,3):
                      if userBomb3 == bomb3:
                        print('Вы взорвались!\n')
                        points -= bet*1.5
                        print('Вы проиграли: '+ str(bet*1.5))
                        print('Ваш текущий баланс: ' + str(points))
                        continue
                      else:
                        print('Вы выиграли: ' + str(bet*2.5))
                        points += bet*2.5
                        print('Бомба была в ячейке: ' + str(bomb) + '\n')
                        print('Победитель!')
                        print('Ваш текущий баланс: ' + str(points))
                    else:
                      print('Неверный ввод. Повторите попытку.\n')
                      continue
                  else:
                    print('Ладно')
                    continue
                else:
                  print('Неверный ввод. Повторите попытку.\n')
                  continue
              else:
                print('Ладно.')
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
            points += bet
            print("\nВаш текущий баланс: " + str(points))
          else:
            print("Не повезло...")
            print('Вы проиграли: ' + str(bet))
            points -= bet
            print("\nВаш текущий баланс: " + str(points))
            cont = input("\nХотите продолжить?(Y/N)").lower()
            if cont == "y":
              continue
            else:
              print('Будем рады видеть вас снова!')
              break
        elif userChoice == 'у':
          number = random.randint(1, 100)
          secret_number = random.randint(1,100)
          user_answer = input('\nБыло загадано число ' + str(number) + ', также было загадано второе число.\nУгадайте, больше оно, меньше, или равно ' + str(number) + ' ' + '(Б/М/Р): ').lower()
          if user_answer == 'б' and number < secret_number:
            if number in range (1, 11) or number in range(90, 101):
              points += bet * 0.1
              print('Вы выиграли: ' + str(bet * 0.1))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            elif number in range (10, 25) or number in range(75, 90):
              points += bet * 0.25
              print('Вы выиграли: ' + str(bet * 0.25))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            elif number in range (25, 75):
              points += bet
              print('Вы выиграли: ' + str(bet))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            else:
              print('Ошибка, повторите попытку.')
          elif user_answer == 'м' and number > secret_number: 
            if number in range (1, 11) or number in range(90, 101):
              points += bet * 0.1
              print('Вы выиграли: ' + str(bet * 0.1))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            elif number in range (10, 25) or number in range(75, 90):
              points += bet * 0.25
              print('Вы выиграли: ' + str(bet * 0.25))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            elif number in range (25, 75):
              points += bet
              print('Вы выиграли: ' + str(bet))
              print('Выпало число: ' + str(secret_number))         
              print('Ваш текущий баланс: ' + str(points))
            else:
              print('Ошибка, повторите попытку.')
          elif user_answer == 'р' and number == secret_number:
            points = bet * 100
            print('Ничего себе!')
            print('Вы выиграли: ' + str(bet * 100))
            print('Выпало число: ' + str(secret_number))         
            print('Ваш текущий баланс: ' + str(points))
          elif user_answer == 'б' and number > secret_number:
            points -= bet
            print('Вы проиграли: ' + str(bet))
            print('Выпало число: ' + str(secret_number))         
            print('Ваш текущий баланс: ' + str(points))
          elif user_answer == 'м' and number < secret_number:
            points -= bet
            print('Вы проиграли: ' + str(bet))
            print('Выпало число: ' + str(secret_number))         
            print('Ваш текущий баланс: ' + str(points))
          elif user_answer == 'р' and number != secret_number:
            points -= bet
            print('Не повезло...')
            print('Вы проиграли: ' + str(bet))
            print('Выпало число: ' + str(secret_number))         
            print('Ваш текущий баланс: ' + str(points))
          else:
            print('Неверный ввод, повторите попытку!')
            continue
          cont = input('\nХотите ли Вы продолжить игру?(y/n): ').lower()
          if cont == 'y':
            continue
          elif cont == 'n':
            print('Спасибо за игру')
            break
          else:
            print('Неверный ввод, повторите попытку.')
        elif userChoice not in ('б','у','м'):
          print('\nТакого режима нет. Повторите попытку.\n')
  except Exception:
    print('Возникла ошибка. Повторите попытку.')


# Не удалены "cont", + не реализован выход из игры на любом этапе. Бэкап.