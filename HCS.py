password = None # Это для того, чтобы работал global password
def Start():
    global password 
    user_password = None
    print("Запуск скрипта...")
    has_pub = os.path.isfile("public key.json") # имеется ли публичный ключ
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    has_settings = os.path.isfile("settings.json") # имеются ли сохраненные настройки
    if has_settings:
        with open ("settings.json", "r", encoding="utf-8") as f:
            data_settings = json.load(f)
        if data_settings.get("password"):
            while True:
                user_password = input("Введите пароль: ").strip()
                hashed_password = hashlib.sha256(user_password.encode()).hexdigest()
                if os.path.isfile("password.hash"):
                    with open("password.hash", "r", encoding="utf-8") as f:
                        password_hash = f.read().strip()
                    if hashed_password == password_hash:
                        break
                    else:
                        print("Неверный пароль!")
                else:
                    print("Ошибка: Проверка пароля есть, а файла пароля нет. Настройки изменены. Если у вас был зашифрован приватный ключ, пересоздайте пару")
                    data_settings["password"] = False
                    data_settings["using_password_for_key"] = False
                    with open ("settings.json", "w", encoding="utf-8") as f:
                        json.dump(data_settings, f, indent=4)
                        user_password = None
                        break
    else:
        data_settings = {"password":False,"using_password_for_key":False,"colorama": False,"autocopy":True}
        with open ("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)
    print("Версия: release 0.3")
    print(f"Найдено: {('Публичный ключ' if has_pub else '') + (', ' if has_pub and has_priv else '') + ('Приватный ключ' if has_priv else '') or '-'}")
    print(r'''
        #########################################
        ##                                     ##
        ##   __    __    ______     ______     ##
        ##  |  |  |  |  /      |   /      |    ##
        ##  |  |__|  | |  ,----'  |  ,----'    ##
        ##  |   __   | |  |       |  `---.     ##
        ##  |  |  |  | |  `----.   |----' |    ##
        ##  |__|  |__|  \______|  |______/     ##
        ##                                     ##
        ##       HYBRID CRYPTO SYSTEM v3.0     ##
        #########################################
''')
    password = user_password
    main_menu()
def main_menu():
    while True:
        choice_main_menu = input('''
        ГЛАВНОЕ МЕНЮ:
    (1) Зашифровать сообщение
    (2) Расшифровать сообщение
    (3) Открыть меню генерации ключей
    (4) Перепроверить ключи и вывести значения
    (5) Импорт публичного ключа собеседника
    (6) Экспорт публичного ключа собеседнику
    (7) Очистить консоль и буфер обмена
    (8) Документация(инструкции, обновления)
    (9) Настройки
    (0) Выйти
    ''').strip()
        if choice_main_menu in ["1","2","3","4","5","6","7","8","9","0"]:
            if choice_main_menu == "1":
                crypter()
            elif choice_main_menu == "2":
                uncrypter()
            elif choice_main_menu == "3":
                generate_menu()
            elif choice_main_menu == "4":
                check_keys()
            elif choice_main_menu == "5":
                import_export_key("import")
            elif choice_main_menu == "6":
                import_export_key("export")
            elif choice_main_menu == "7":
                cleaner()
            elif choice_main_menu == "8":
                documentation()
            elif choice_main_menu == "9":
                settings()
            elif choice_main_menu == "0":
                sys.exit()
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов")

def cleaner():
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        pyperclip.copy("")
        print("Консоль и буфер обмена очищены.")
        print(r'''
        #########################################
        ##                                     ##
        ##   __    __    ______     ______     ##
        ##  |  |  |  |  /      |   /      |    ##
        ##  |  |__|  | |  ,----'  |  ,----'    ##
        ##  |   __   | |  |       |  `---.     ##
        ##  |  |  |  | |  `----.   |----' |    ##
        ##  |__|  |__|  \______|  |______/     ##
        ##                                     ##
        ##       HYBRID CRYPTO SYSTEM v3.0     ##
        #########################################
''')
    except Exception:
        print("Консоль очищена, но буфер обмена очистить не удалось.")

def documentation():
    while True:
        choice = input('''
    ДОКУМЕНТАЦИЯ
(1) Как начать общаться с собеседником
(2) Как работает скрипт
(3) Журнал разработчика
(9) Выйти в главное меню
(0) Выйти
''')
        if choice not in ["1","2","3","9","0"]:
            print("Неверный ввод!")
        else:
            if choice == "1":
                print('''
        Как общаться?
    1. Как создать ключи и обменяться ими
    2. Как шифровать и расшифровывать сообщения
    3. Где можно общаться для обмена зашифрованных сообщений

1. Создание ключей сделано через меню генерации ключей(Путеводитель: Главное меню -> Меню гегерации ключей -> Сгенерировать новую пару). Обменяться ими можно через встроенные функции импорта и экспорта, но я настоятельно рекомендую обмениваться публичным ключом вживую(через флешку или иным способом), если вам ОЧЕНЬ необходима анонимность. В противном случае, есть шанс, что гос органы и хакеры могут узнать, что вы пишите.
2. Шифрование сообщений и их расшифровка выведены на главное меню. Если вы создали ключи и обменялись ими с собеседником, вы можете пересылать друг другу зашифрованные сообщения
3. Когда вы обменялись ключами(желательно лично, допустим через накопители), вы можете спокойно пересылать свои сообщения хоть в самих MAX, VK, TELEGA - ваши сообщения даже в них никто не прочитает
''')
            elif choice == "2":
                print('''
        Как работает скрипт
    1. Шифрования
    2. Структура

1. Шифрование происходит на уровне RSA+AES+ЦП. Сначала создается пара ключей на уровне RSA, а затем собеседники обмениваются своими публичными ключами. С помощью публичного ключа собеседника, шифруется ключ AES, который до этого должен был зашифровать само сообщение. Затем добавляется подпись с помощью своего приватного ключа. Для расшифровки, второй собеседник сравнивает подпись с помощью публичного ключа первого собеседника, затем расшифровывает AES ключ своим приватным ключом и этим же расшифрованным AES ключом расшыфровывает сообщение
2. По структуре все ясно - код поделён на функции, в основном разделяющие разные меню. Также имеется докачка библиотек, если открывается не .exe файл
''')
            elif choice == "3":
                print('''
        Что добавилось в разных версиях?
    1. v3.0
    2. v2.0
    3. v1.0
1. В этой версии добавилось намного больше функций, в отличие от прошлой. Экспорт и импорт ключей текстом, удаление их через меню. Добавлены настройки - вход в программу по паролю, а также шифрование приватного ключа.
2. Основной функционал. Добавилось намного больше защиты, в отличие от версии RSA(HCS v1.0), которыя использовала только RSA шифрование.
3. Самая первая версия. Очень небезопасна - можно подобрать ключи перебором
''')
            elif choice == "9":
                break
            elif choice == "0":
                sys.exit()

def generate_menu(): #Вызывается из главного меню кнопкой №3
    while True:
        choice_generate_menu = input('''
    МЕНЮ ГЕНЕРАЦИИ:
(1) Сгенерировать новую пару ключей
(2) Восстановить публичный ключ из приватного
(8) Удалить ключи
(9) Назад в главное меню
(0) Выйти
''')
        if choice_generate_menu in ["1","2","8","9","0" ]:
            if choice_generate_menu == "1":
                generate_keys()
            elif choice_generate_menu == "2":
                recovery_pub_key()
            elif choice_generate_menu == "8":
                try:
                    if os.path.isfile("public key.json"):
                        os.remove("public key.json")
                        print("Удален публичный ключ")
                    else:
                        print("Ошибка: Не найден публичный ключ")
                except Exception:
                    print("Не удалось удалить публичный ключ")
                try:
                    if os.path.isfile("private key.json"):
                        os.remove("private key.json")
                        print("Удален приватный ключ")
                    else:
                        print("Ошибка: Не найден приватный ключ")
                except Exception:
                    print("Не удалось удалить приватный ключ")
            elif choice_generate_menu == "9":
                return
            elif choice_generate_menu == "0":
                sys.exit()
            break
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов\n")

def check_keys(): # Вызывается из главного меню кнопкой №4
    global password
    has_pub = os.path.isfile("public key.json") # имеется ли публичный ключ
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    print(f"Найдено: {('Публичный ключ' if has_pub else '') + (', ' if has_pub and has_priv else '') + ('Приватный ключ' if has_priv else '') or '-'}")
    with open("settings.json","r", encoding="utf-8") as f:
        data_settings = json.load(f)
        using_password_for_key = data_settings.get("using_password_for_key")
    if has_pub:
        try:
            with open("public key.json","r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"----ПУБЛИЧНЫЙ КЛЮЧ(e, n)----\ne = {data["e"]}\nn = {data["n"]}\n")
        except Exception as e:
            print(f"Ошибка чтения публичного ключа: {e}")
    if has_priv:
        try:
            with open("private key.json","r", encoding="utf-8") as f:
                data = json.load(f)
            if using_password_for_key:
                #password="1234..." Пароль вводится при входе
                key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                cipher = Fernet(key)
                data["d"] = cipher.decrypt(data["d"].encode()).decode()
            print(f"----ПРИВАТНЫЙ КЛЮЧ(d, n)----\nd = {data["d"]}\nn = {data["n"]}\n")
        except Exception as e:
            print(f"Ошибка чтения приватного ключа: {e}")

def generate_keys(): # создание обоих ключей(перезаписывание если уже есть)
    global password
    if os.path.isfile("settings.json"):
        with open ("settings.json", "r", encoding = "utf-8") as f:
            data_settings = json.load(f)
        using_password_for_key = data_settings.get("using_password_for_key")
    else:
        with open ("settings.json", "w", encoding = "utf-8") as f:
            data_settings = {"password":False,"using_password_for_key":False,"colorama": False,"autocopy":True}
            json.dump(data_settings, f, indent=4)
        using_password_for_key = False
    while True:
        choice_1 = input("При создании новой пары ключей, прошлая пара исчезнет. Пара ключей хранятся в той же папке, что и этот файл\n(1) Продолжить\n(9) Отмена\n(0) Выйти\n").strip()
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
                if using_password_for_key:
                    #password="1234..." Пароль вводится при входе
                    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                    cipher = Fernet(key)
                    d = cipher.encrypt(str(d).encode()).decode()
                    public_key = {"e": e, "n":n}
                    private_key = {"d": d, "n": n}
                else:
                    public_key = {"e": e, "n":n}
                    private_key = {"d": d, "n": n}
                with open("public key.json", 'w', encoding="utf-8") as f:
                    json.dump(public_key, f, indent=4)
                    print("публичный ключ создан и сохранен в файл")
                with open("private key.json",'w', encoding="utf-8") as f:
                    json.dump(private_key, f, indent=4)
                    print("приватный ключ создан и сохранен в файл")
                break
            if (choice_1 == "9"):
                print("Вы отменили генерацию ключей")
                return
            if(choice_1 == "0"):
                sys.exit()
        else:
            print("Вы ввели неверное число! Выберите один из предложенных вариантов")

def recovery_pub_key(): #Восстановление публичного ключа из приватного
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
    global password
    if os.path.isfile("public key.json") and os.path.isfile("private key.json"):
        with open("public key.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        e = data["e"]
        n = data["n"]
        with open ("private key.json", "r", encoding="utf-8") as f:
            data_priv = json.load(f)
            d, n_priv = data_priv["d"],data_priv["n"]
        if os.path.isfile("settings.json"):
            with open ("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
            autocopy = data_settings["autocopy"]
            using_password_for_key = data_settings.get("using_password_for_key")
            if using_password_for_key:
                using_password_for_key = data_settings["using_password_for_key"]
                #password="1234..." Пароль вводится при входе
                key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                cipher = Fernet(key)
                d = cipher.decrypt(d.encode()).decode()
        else:
            data_settings = {"password":False,"using_password_for_key":False,"colorama": False,"autocopy":True}
            with open ("settings.json", "w", encoding="utf-8") as f:
                json.dump(data_settings, f, indent=4)
        message = input("Введите сообщение: \nИли введите 0 для выхода в главное меню").strip()
        if message == "0":
            print("Вы вышли из создания сообщения")
        else:
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
            if data_settings["autocopy"]:
                pyperclip.copy(final_packet)
    else:
        if not os.path.isfile("public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not os.path.isfile("private key.json"):
            print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")

def uncrypter(): #Расшифровщик сообщения. Вызывается из главного меню кнопкой №2
    global password
    if os.path.isfile("public key.json") and os.path.isfile("private key.json"):
        with open("private key.json", "r", encoding="utf-8") as f:
            data_priv=json.load(f)
        d = data_priv["d"]
        n_priv = data_priv["n"]
        with open("public key.json", "r", encoding="utf-8") as f:
            data_pub = json.load(f)
        e, n_pub = data_pub["e"], data_pub["n"]
        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            data_settings = {"password":False,"using_password_for_key":False,"colorama": False,"autocopy":True}
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(data_settings, f, indent=4)
        while True:
            try:
                full_data = input("Вставьте зашифрованную строку: \nИли введите 0 для выхода в главное меню").strip()
                if full_data == "0":
                    print("Вы вышли из расшифрования сообщения")
                    break
                else:
                    if "|" in full_data:
                        main_data, signature_str = full_data.rsplit("|", 1)
                        signature = int(signature_str)
                        # Разделяем ключ и сообщение
                        crypted_aes_key_str, encoded_message = main_data.rsplit(":", 1)

                        if data_settings.get("using_password_for_key"):
                            key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                            cipher = Fernet(key)
                            d = cipher.decrypt(d.encode()).decode()
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
                            print("\nПОДПИСЬ ПОДТВЕРЖДЕНА: Сообщение подлинное(не поддельное)")
                            print(f"Текст: {decrypted_message}")
                            break
                        else:
                            print("!!!!\nВНИМАНИЕ: Подпись не верна! Сообщение подделано или повреждено")
                            print("Расшифрованное сообщение:")
                            print(decrypted_message)
                            break
                    else:
                        print("Ошибка: отсутствует подпись")
            except ValueError:
                print("Ошибка: Возможно, ключ не подходит или сообщение повреждено")
                break
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}\nВозможно, сообщение или ключ повреждены")
                break
    else:
        if not os.path.isfile("public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not os.path.isfile("private key.json"):
            print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")
def import_export_key(mode):
    while True:
        with open("settings.json", "r", encoding="utf-8") as f:
            data_settings = json.load(f)
        if mode == "import":
            choice_3 = input("Внимание: прошлый публичный ключ перезапишется\n(1)Продолжить\n(9)Назад в главное меню\n(0)Выйти\n")
            while choice_3 not in ["1","9","0"]:
                print("Неверный ввод!")
                choice_3 = input("Внимание: прошлый публичный ключ перезапишется\n(1)Продолжить\n(9)Назад в главное меню\n(0)Выйти\n")
            if choice_3 == "1":
                try:
                    input_key = input("Введите ключ: ")
                    if ":" in input_key:
                        e_str, n_str = input_key.split(":", 1)
                        e, n = int(e_str), int(n_str)
                        with open("public key.json", "w", encoding="utf-8") as f:
                            public_key = {"e": e, "n":n}
                            json.dump(public_key, f, indent=4)
                        break
                    else:
                        print("В этом ключе отсутствует разделитель!")
                        break
                except Exception:
                    input("Ошибка в чтении ключа")
            elif choice_3 == "9":
                return
            elif choice_3 == "0":
                sys.exit()
        elif mode == "export":
            if os.path.isfile("public key.json"):
                try:
                    with open("public key.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                    print_key = f"{data['e']}:{data['n']}"
                    print(print_key)
                    if data_settings.get("autocopy"):
                        pyperclip.copy(print_key)
                    break
                except Exception:
                    input("Ошибка чтения и вывода файла\nНажмите Enter, чтобы вернуться")
                    break
            else:
                input("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ\nНажмите Enter, чтобы вернуться")
                break

def settings():
    global password
    while True:
        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            with open("settings.json", "w", encoding="utf-8") as f:
                data_settings = {"password":False,"using_password_for_key":False,"colorama": False,"autocopy":True}
                json.dump(data_settings, f, indent=4)
        choice_settings = input(f'''
    МЕНЮ НАСТРОЕК
(1) Пароль - {data_settings.get("password")}
(2) Шифрование приватного ключа паролем - {data_settings.get("using_password_for_key")}
(3) Автокопирование - {data_settings.get("autocopy")}
(9) Выйти в главное меню
(0) Выйти
''')
        if choice_settings in ["1","2","3","9","0"]:
            if choice_settings == "1":
                if data_settings.get("password"):
                    if data_settings.get("using_password_for_key"):
                        if os.path.isfile("private key.json"):
                            try:
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                #password="1234..." Пароль вводится при входе
                                key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                                cipher = Fernet(key)
                                data["d"] = int(cipher.decrypt(data["d"].encode()).decode())
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=4)
                                data_settings["using_password_for_key"] = False
                                data_settings["password"] = False
                                password = None
                                os.remove("password.hash")
                                print("Вход с паролем выключен")
                                print("Шифрование приватного ключа паролем Выключено")
                            except Exception:
                                print("Не удалось расшифровать ключ")
                        else:
                            password = None
                            data_settings["using_password_for_key"] = False
                            data_settings["password"] = False
                            os.remove("password.hash")
                            print("Вход с паролем выключен")
                            print("Шифрование приватного ключа паролем Выключено")
                    else:
                        password = None
                        data_settings["password"] = False
                        os.remove("password.hash")
                        print("Вход с паролем выключен")
                else:
                    password = input("Введите новый пароль: ")
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    with open("password.hash", "w", encoding="utf-8") as f:
                        f.write(hashed_password)
                    data_settings["password"] = True    
            elif choice_settings == "2":
                if data_settings.get("password"):
                    if data_settings.get("using_password_for_key"):
                        if os.path.isfile("private key.json"):
                            try:
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                #password="1234..." Пароль вводится при входе
                                key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                                cipher = Fernet(key)
                                data["d"] = int(cipher.decrypt(data["d"].encode()).decode())
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=4)
                                data_settings["using_password_for_key"] = False
                                print("Шифрование приватного ключа паролем Выключено")
                            except Exception:
                                print("Не удалось расшифровать ключ")
                        else:
                            data_settings["using_password_for_key"] = False
                            print("Шифрование приватного ключа паролем Выключено")
                    else:
                        try:
                            if os.path.isfile("private key.json"):
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                #password="1234..." Пароль вводится при входе
                                key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
                                cipher = Fernet(key)
                                data["d"] = cipher.encrypt(str(data["d"]).encode()).decode()
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=4)
                                data_settings["using_password_for_key"] = True
                                print("Шифрование приватного ключа паролем Включено")
                            else:
                                data_settings["using_password_for_key"] = True
                                print("Шифрование приватного ключа паролем Включено")
                        except Exception:
                            print("Не удалось зашифровать ключ")
                else:
                    print("Эта функция недоступна: у вас не установлен пароль")
            elif choice_settings == "3":
                data_settings["autocopy"] = not data_settings["autocopy"]
            elif choice_settings == "9":
                return
            elif choice_settings == "0":
                sys.exit()
        else:
            print("Неверный ввод!")
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)

# Импорт критически важных библиотек и запуск
import sys, subprocess
required = ['sympy', 'cryptography', 'pyperclip']
missing = []
for lib in required:
    try:
        __import__(lib)
    except ImportError:
        missing.append(lib)
if missing:
    print(f"Библиотеки {missing} не найдены. Устанавливаю...")
    try:
        # Запускаем pip install через текущий интерпретатор Python
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        print("Установка завершена успешно!\n")
    except Exception as e:
        print(f'''\n[!] Ошибка при автоустановке: {e}
Пожалуйста, установите вручную: pip install {' '.join(missing)}''')
        input("Нажмите Enter, чтобы выйти...")
        sys.exit()
import random, os, json, base64, secrets, hashlib
import pyperclip
from sympy import mod_inverse, nextprime #Математические функции для генерации ключей
from cryptography.fernet import Fernet #Для AES ключа
try:
    Start()
except Exception as e:
    input(f"\n[!]Произошла непредвиденная ошибка: {e}\nНажмите Enter, чтобы выйти...")
    sys.exit()
