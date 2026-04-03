# Импорт критически важных библиотек
import random
from sympy import mod_inverse, nextprime
import os
import json

def Start():
    started = True
    print("Запуск скрипта...")
    print("Версия: release 0.1")
    has_pub = os.path.isfile("public key.json") # имеется ли публичный ключ
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    if has_pub and has_priv:
        print("Найдено: Публичный ключ, Приватный ключ\nНе найдено: -")
    if has_pub and not has_priv:
        print("Найдено: Публичный ключ\nНе найдено: Приватный ключ")
    if has_priv and not has_pub:
        print("Найдено: Приватный ключ\nНе найдено: Публичный ключ")
    if not has_priv and not has_pub:
        print("Найдено: -\nНе найдено: Публичный ключ, Приватный ключ")
    if started == True:
        print(r'''
==================================================
|                ____   ____    _                |
|               |  _ \ / ___|  / \               |
|               | |_) |\___ \ / _ \              |
|               |  _ <  ___) / ___ \             |
|               |_| \_\|____/_/   \_\            |
==================================================
RSA - Ассиметричное шифрованние
''')
    main_menu()
    
def main_menu():
    while True:
        choice_main_menu = input(r'''
        ГЛАВНОЕ МЕНЮ:
    (1) Зашифровать сообщение
    (2) Расшифровать сообщение
    (3) Открыть меню генерации ключей
    (4) Перепроверить ключи и вывести значения
    (0) Выйти
    ''').strip()
        if choice_main_menu in ["1","2","3","4","0"]:
            if choice_main_menu == "1":
                crypter()
            elif choice_main_menu == "2":
                uncrypter()
            elif choice_main_menu == "3":
                generate_menu()
            elif choice_main_menu == "4":
                check_keys()
            elif choice_main_menu == "0":
                exit()
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов")
    
def generate_menu(): #Вызывается из главного меню кнопкой № 3
    while True:
        choice_generate_menu = input(r'''
    МЕНЮ ГЕНЕРАЦИИ:
(1) Сгенерировать новую пару ключей
(2) Восстановить публичный ключ из приватного
(9) Назад в главное меню
(0) Выйти
''')
        if choice_generate_menu in ["1","2","9","0"]:
            if choice_generate_menu == "1":
                generate_keys()
            elif choice_generate_menu == "2":
                recovery_pub_key()
            elif choice_generate_menu == "9":
                return
            elif choice_generate_menu == "0":
                exit()
            break
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов\n")

def check_keys(): # Вызывается из главного меню кнопкой №4
    has_pub = os.path.isfile("public key.json") # имеется ли публичный ключ
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    if has_pub and has_priv:
        print("Найдено: Публичный ключ, Приватный ключ\nНе найдено: -")
    elif has_pub and not has_priv:
        print("Найдено: Публичный ключ\nНе найдено: Приватный ключ")
    elif has_priv and not has_pub:
        print("Найдено: Приватный ключ\nНе найдено: Публичный ключ")
    elif not has_priv and not has_pub:
        print("Найдено: -\nНе найдено: Публичный ключ, Приватный ключ")
    if has_pub:
        try:
            with open("public key.json","r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"----ОТКРЫТЫЙ КЛЮЧ (e, n)----\ne = {data["e"]}\nn = {data["n"]}\n")
        except Exception as e:
            print(f"Ошибка чтения публичного ключа: {e}")
    if has_priv:
        try:
            with open("private key.json","r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"----ЗАКРЫТЫЙ КЛЮЧ (d, n)----\nd = {data["d"]}\nn = {data["n"]}\n")
        except Exception as e:
            print(f"Ошибка чтения приватного ключа: {e}")

def generate_keys(): # создание обоих ключей(перезаписывание если уже есть)
    while True:
        choice_1 = input("При создании новой пары ключей, прошлая пара исчезнет. Пара ключей хранятся в той же папке, что и этот файл\n(1) - Продолжить\n(9) - Отмена\n(0) - Выйти\n").strip()
        if(choice_1 in ["1","9","0"]):
            if (choice_1 == "1"):
                print("Создание ключей...")
                # генерация и сохранение e, n и d, n в ключи
                p = nextprime(random.getrandbits(1024))
                q = nextprime(random.getrandbits(1024))
                e = 65537
                n = q * p
                Fn = (q-1) * (p-1)
                d = mod_inverse (e, Fn)
                with open("public key.json", 'w', encoding="utf-8") as f:
                    public_key = {"e": e, "n":n}
                    json.dump(public_key, f, indent=4)
                    print("публичный ключ создан и сохранен в файл")
                with open("private key.json",'w', encoding="utf-8") as f:
                    private_key = {"d": d, "n": n}
                    json.dump(private_key, f, indent=4)
                    print("приватный ключ создан и сохранен в файл")
                break
            if (choice_1 == "9"):
                print("Вы отменили генерацию ключей")
                return
            if(choice_1 == "0"):
                exit()
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов")

def  recovery_pub_key(): #Восстановление публичного ключа из приватного
    if os.path.isfile("private key.json"):
        with open("private key.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        e = 65537
        n = data["n"]
        print("\nПолучены данные из приватного ключа")
        with open("public key.json", 'w', encoding="utf-8") as f:
            public_key = {"e": e, "n":n}
            json.dump(public_key, f, indent=4)
            print("Публичный ключ создан и сохранен в файл")
    else:
        print("Не найден приватный ключ. Вернитесь в меню генерации для того, чтобы создать новую пару ключей")
        
def crypter(): #Шифровщик сообщения. Вызывается из главного меню кнопкой №1
    if os.path.isfile("public key.json"):
        with open("public key.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        e = data["e"]
        n = data["n"]
        message = input("Введите сообщение: ").strip()
        message_int = int.from_bytes(message.encode('utf-8'), 'big')
        crypted_int = pow(message_int, e, n)
        if crypted_int>=n:
            print("Сообщение слишком длинное для этого ключа!")
            return
        print("Зашифрованное сообщение:")
        print(crypted_int)
    else:
        print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        
def uncrypter(): #Расшифровщик сообщения. Вызывается из главного меню кнопкой №2
    if os.path.isfile("private key.json"):
        with open("private key.json","r", encoding="utf-8") as f:
            data=json.load(f)
        d = data["d"]
        n = data["n"]
        while True:
            try:
                crypted_int = input("вставьте зашифрованное сообщение: ").strip()
                if not crypted_int:
                    print("Вы ничего не ввели. Попробуйте еще раз.")
                    continue
                crypted_int = int(crypted_int)
                decrypted_int = pow(crypted_int, d, n)
                byte_size = (decrypted_int.bit_length() + 7) // 8
                decrypted_message = decrypted_int.to_bytes(byte_size, 'big').decode('utf-8')
                print(f"расшифрованное сообщение:\n {decrypted_message}")
                break
            except ValueError:
                print("Это не зашифрованное сообщение или вообще не целое числовое значение")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}\nВозможно, сообщение или ключ повреждены")
                break
    else:
        print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")

Start()
