def Start():
    started = True
    print("Запуск скрипта...")
    print("Версия: release 0.2")
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
        #########################################
        ##                                     ##
        ##   __    __    ______     ______     ##
        ##  |  |  |  |  /      |   /      |    ##
        ##  |  |__|  | |  ,----'  |  ,----'    ##
        ##  |   __   | |  |       |  `---.     ##
        ##  |  |  |  | |  `----.   |----'  |   ##
        ##  |__|  |__|  \______|  |______/     ##
        ##                                     ##
        ##       HYBRID CRYPTO SYSTEM v2.0     ##
        #########################################
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
        if choice_generate_menu in ["1","2","9","0" ]:
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
                p = nextprime(secrets.randbits(1024))
                q = nextprime(secrets.randbits(1024))
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
    if os.path.isfile("public key.json") and os.path.isfile("private key.json"):
        with open("public key.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        e = data["e"]
        n = data["n"]
        with open ("private key.json", "r", encoding="utf-8") as f:
            priv_data = json.load(f)
        d, n_priv = priv_data["d"],priv_data["n"]
        message = input("Введите сообщение: ").strip()
        # генерация AES
        aes_key = Fernet.generate_key()
        encrypt_aes = Fernet(aes_key)
        # Шифровка через AES
        crypted_message = encrypt_aes.encrypt(message.encode('utf-8'))
        # Шифруем ключ AES через RSA для передачи вместе с текстом
        aes_key_int = int.from_bytes(aes_key, 'big')
        if aes_key_int >= n:
            print("Ключ слишком велик для этого модуля n (довольно редкая ошибка, попробуйте заново)")
            return
        crypted_aes_key = pow(aes_key_int, e, n)
        encoded_message = crypted_message.decode('utf-8')
        data = {"aes_key": crypted_aes_key, "message": encoded_message}
        final_message = f"{crypted_aes_key}:{encoded_message}"
        # Цифровая подпись
        message_hash = hashlib.sha256(message.encode('utf-8')).digest()
        hash_int = int.from_bytes(message_hash, 'big')
        signature = pow(hash_int, d, n_priv)
        # Готовое сообщение
        final_packet = f"{final_message}|{signature}"
        print("Вот зашифрованное сообщение:")
        print(final_packet)
    else:
        if not os.path.isfile("public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not os.path.isfile("private key.json"):
            print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")


def uncrypter(): #Расшифровщик сообщения. Вызывается из главного меню кнопкой №2
    if os.path.isfile("public key.json") and os.path.isfile("private key.json"):
        with open("private key.json","r", encoding="utf-8") as f:
            data_priv=json.load(f)
        d = data_priv["d"]
        n_priv = data_priv["n"]
        with open("public key.json", "r", encoding="utf-8") as f:
            data_pub = json.load(f)
        e, n_pub = data_pub["e"], data_pub["n"]
        while True:
            try:
                full_data = input("Вставьте зашифрованную строку: ").strip()
                if "|" in full_data:
                    main_data, signature_str = full_data.rsplit("|", 1)
                    signature = int(signature_str)
                    # разделяем ключ и сообщение
                    crypted_aes_key_str, encoded_message = main_data.rsplit(":", 1)
                    # Расшифровываем AES ключ через RSA
                    crypted_aes_key_int = int(crypted_aes_key_str)
                    decrypted_aes_key_int = pow(crypted_aes_key_int, d, n_priv)
                    # Превращаем число обратно в байты ключа Fernet
                    byte_size = (decrypted_aes_key_int.bit_length() + 7) // 8
                    aes_key = decrypted_aes_key_int.to_bytes(byte_size, 'big')
                    # Расшифровываем сообщение через AES
                    uncoded_aes = Fernet(aes_key)
                    # Декодируем base64 обратно в байты и расшифровываем
                    decrypted_message = uncoded_aes.decrypt(encoded_message.encode('utf-8')).decode('utf-8')
                        
                    current_hash = hashlib.sha256(decrypted_message.encode('utf-8')).digest()
                    current_hash_int = int.from_bytes(current_hash, 'big')
                    decrypted_signature_hash = pow(signature, e, n_pub)
                    if current_hash_int == decrypted_signature_hash:
                        print("\nПОДПИСЬ ПОДТВЕРЖДЕНА: Сообщение подлинное(не поддельное).")
                        print(f"Текст: {decrypted_message}")
                        break
                    else:
                        print("!!!!\nВНИМАНИЕ: Подпись не верна! Сообщение подделано или повреждено.")
                        print("Расшифрованное сообщение:")
                        print(decrypted_message)
                        break
                else:
                    print("Ошибка: отсутствует подпись")
            except ValueError:
                print("Ошибка: Возможно, ключ не подходит или сообщение повреждено")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}\nВозможно, сообщение или ключ повреждены")
                break
    else:
        if not os.path.isfile("public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not os.path.isfile("private key.json"):
            print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")

# Импорт критически важных библиотек и запуск
try:
    import random
    from sympy import mod_inverse, nextprime #Математические функции для генерации ключей
    import os #Для удобной проверки наличия файлов ключей
    import json #Для сохранения ключей в .json файлы
    from cryptography.fernet import Fernet #Для AES ключа
    import base64
    import secrets
    import hashlib
except Exception as e:
    error_1 = input("Не скачаны зависимости\nЧтобы их скачать, откройте командную строку и введите: pip install sympy cryptography")
Start()
