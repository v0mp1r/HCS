password=None
logo_choice = 2
logo = 2
print("Запуск скрипта...")
print("Версия: release 0.5")

def Start():
    global password
    user_password = None
    has_pub = os.path.isfile("public key.json") or os.path.isfile("my public key.json") # имеется ли публичный ключ
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    has_settings = os.path.isfile("settings.json") # имеются ли сохраненные настройки
    if has_settings:
        with open ("settings.json", "r", encoding="utf-8") as f:
            data_settings = json.load(f)
        if data_settings.get("password"):
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Найдено: {('Публичный ключ' if has_pub else '') + (', ' if has_pub and has_priv else '') + ('Приватный ключ' if has_priv else '') or '-'}") 
                if os.path.isfile("password.txt"):
                    if data_settings.get("secretpswd"):
                        user_password = getpass.getpass("Введите пароль: ").strip()
                    else:
                        user_password = input("Введите пароль: ").strip()
                    password_bytes = user_password.encode('utf-8')
                    sha256_bytes = hashlib.sha256(password_bytes).digest()
                    with open("password.txt", "r", encoding="utf-8") as f:
                        stored_hash = f.read().strip().encode('utf-8')
                    if bcrypt.checkpw(sha256_bytes, stored_hash):
                        break
                    else:
                        pass
                else:
                    print("Ошибка: Проверка пароля есть, а файла пароля нет. Настройки изменены. Если у вас был зашифрован приватный ключ, пересоздайте пару")
                    data_settings["password"] = False
                    data_settings["using_password_for_key"] = False
                    with open ("settings.json", "w", encoding="utf-8") as f:
                        json.dump(data_settings, f, indent=4)
                        user_password = None
                        break
    else:
        data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True, "secretpswd":False}
        with open ("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)
    logo_choice = data_settings["logo"]
    logo_choice = int(logo_choice)
    password = user_password
    main_menu()

def main_menu():
    global logo_choice
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        logo_2 = [
        r" ██╗  ██╗     ██████╗    ███████╗ ",
        r" ██║  ██║    ██╔════╝    ██╔════╝ ",
        r" ███████║    ██║         ███████╗ ",
        r" ██╔══██║    ██║         ╚════██║ ",
        r" ██║  ██║    ╚██████╗    ███████║ ",
        r" ╚═╝  ╚═╝     ╚═════╝    ╚══════╝ ",
        r" ──────────────────────────────── ",
        r"     HYBRID CRYPTO SYSTEM v0.5    ",
        r" █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ ",
        r" █         MAIN    MENU         █ ",
        r" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
    ]
        if logo_choice == 1:
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
        ##       HYBRID CRYPTO SYSTEM v0.5     ##
        #########################################
                        MAIN MENU                
''')
        elif logo_choice == 2:
            for line in logo_2:
                    print(line.rstrip().center(width))
        choice_main_menu = input('''
        ГЛАВНОЕ МЕНЮ:
    (1) Зашифровать сообщение
    (2) Расшифровать сообщение
    (3) Открыть меню генерации ключей
    (4) Перепроверить ключи и вывести значения
    (5) Импорт публичного ключа собеседника
    (6) Экспорт публичного ключа собеседнику
    (7) Очистить буфер обмена
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

def cleaner():
    try:
        pyperclip.copy("")
        print("Буфер обмена очищен")
    except Exception:
        print("Не удалось очистить буфер обмена")
    input("\nЧтобы продолжить, нажмите Enter")

def documentation():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        logo_2 = [
            r" ██╗  ██╗     ██████╗    ███████╗ ",
            r" ██║  ██║    ██╔════╝    ██╔════╝ ",
            r" ███████║    ██║         ███████╗ ",
            r" ██╔══██║    ██║         ╚════██║ ",
            r" ██║  ██║    ╚██████╗    ███████║ ",
            r" ╚═╝  ╚═╝     ╚═════╝    ╚══════╝ ",
            r" ──────────────────────────────── ",
            r"     HYBRID CRYPTO SYSTEM v0.5    ",
            r" █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ ",
            r" █         DOCUMENTATION        █ ",
            r" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
        ]
        if logo_choice == 1:
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
            ##       HYBRID CRYPTO SYSTEM v0.5     ##
            #########################################
                          DOCUMENTATION              
    ''')
        elif logo_choice == 2:
            for line in logo_2:
                print(line.rstrip().center(width))
        choice = input('''
        ДОКУМЕНТАЦИЯ
    (1) Как начать общаться с собеседником
    (2) Как работает скрипт
    (3) Журнал разработчика
    (9) Выйти в главное меню
    (0) Выйти
''')
        if choice in ["1","2","3","9","0"]:
            if choice == "1":
                print('''
        Как общаться?
    1. Как создать ключи и обменяться ими
    2. Как шифровать и расшифровывать сообщения
    3. Где можно общаться для обмена зашифрованных сообщений

1. Создание ключей сделано через меню генерации ключей(Путеводитель: Главное меню -> Меню гегерации ключей -> Сгенерировать новую пару). Обменяться ими можно через встроенные функции импорта и экспорта, но я настоятельно рекомендую обмениваться публичным ключом вживую(через флешку или иным способом), если вам ОЧЕНЬ необходима анонимность. В противном случае, есть шанс, что гос органы и хакеры могут узнать, что вы пишите.
2. Шифрование сообщений и их расшифровка выведены на главное меню. Если вы создали ключи и обменялись ими с собеседником, вы можете пересылать друг другу зашифрованные сообщения
3. Когда вы обменялись ключами(НЕобязательно лично, просто важно, чтобы ваше сообщение с ключом не подделали!), вы можете спокойно пересылать свои сообщения хоть в самих MAX, VK, TELEGA - ваши сообщения даже в них никто не прочитает
''')
                input("\nЧтобы продолжить, нажмите Enter")
            elif choice == "2":
                print('''
        Как работает скрипт
    1. Шифрования
    2. Структура

1. Шифрование происходит на уровне RSA-OAEP+AES+PSS. Сначала создается пара ключей на уровне RS-OAEP, а затем собеседники обмениваются своими публичными ключами. С помощью публичного ключа собеседника, шифруется ключ AES, который до этого должен был зашифровать само сообщение. Затем добавляется подпись с помощью своего приватного ключа. Для расшифровки, второй собеседник сравнивает подпись с помощью публичного ключа первого собеседника, затем расшифровывает AES ключ своим приватным ключом и этим же расшифрованным AES ключом расшифровывает сообщение
2. По структуре все ясно - код поделён на функции, в основном разделяющие разные меню. Также имеется докачка библиотек, если открывается не .exe файл
''')
                input("\nЧтобы продолжить, нажмите Enter")
            elif choice == "3":
                print('''
        Что добавилось в разных версиях?
    1. v0.5
    2. v0.4
    3. v0.3
    4. v0.2
    5. v0.1
1. Новая защита - OAEP, PSS. Теперь сообщение сильнее защищено. К паролю добавилась защита(теперь есть соль). Добавился getpass.
2. Новое меню и логотип, а также сжатие сообщений.
3. В этой версии добавилось намного больше функций, в отличие от прошлой. Экспорт и импорт ключей текстом, удаление их через меню. Добавлены настройки - вход в программу по паролю, а также шифрование приватного ключа.
4. Основной функционал. Добавилось намного больше защиты, в отличие от версии RSA(HCS v0.1), которыя использовала только RSA шифрование.
5. Самая первая версия. Очень небезопасна - можно подобрать ключи перебором.
''')
                input("\nЧтобы продолжить, нажмите Enter")
            elif choice == "9":
                break
            elif choice == "0":
                sys.exit()

def generate_menu(): #Вызывается из главного меню кнопкой №3
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        logo_2 = [
        r" ██╗  ██╗     ██████╗    ███████╗ ",
        r" ██║  ██║    ██╔════╝    ██╔════╝ ",
        r" ███████║    ██║         ███████╗ ",
        r" ██╔══██║    ██║         ╚════██║ ",
        r" ██║  ██║    ╚██████╗    ███████║ ",
        r" ╚═╝  ╚═╝     ╚═════╝    ╚══════╝ ",
        r" ──────────────────────────────── ",
        r"     HYBRID CRYPTO SYSTEM v0.5    ",
        r" █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ ",
        r" █        GENERATION MENU       █ ",
        r" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
    ]
        if logo_choice == 1:
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
        ##       HYBRID CRYPTO SYSTEM v0.5     ##
        #########################################
                    GENERATION MENU              
''')
        elif logo_choice == 2:
            for line in logo_2:
                print(line.rstrip().center(width))
        choice_generate_menu = input('''
        МЕНЮ ГЕНЕРАЦИИ:
    (1) Сгенерировать новую пару ключей
    (2) Сохранить свой публичный ключ в файл
    (8) Удалить ключи
    (9) Назад в главное меню
    (0) Выйти
''')
        if choice_generate_menu in ["1","2","8","9","0" ]:
            if choice_generate_menu == "1":
                generate_keys()
            elif choice_generate_menu == "2":
                save_pub_key()
            elif choice_generate_menu == "8":
                try:
                    if os.path.isfile("my public key.json"):
                        os.remove("my public key.json")
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
                input("\nНажмите Enter, чтобы продолжить")
            elif choice_generate_menu == "9":
                return
            elif choice_generate_menu == "0":
                sys.exit()
            break

def check_keys(): # Вызывается из главного меню кнопкой №4
    global password
    os.system('cls' if os.name == 'nt' else 'clear')
    has_pub = os.path.isfile("public key.json") or os.path.isfile("my public key.json") # имеется ли публичный ключ
    if has_pub:
        if os.path.isfile("public key.json"):
            has_notmy_pub = True
            has_my_pub = False
        else:
            has_notmy_pub = False
            has_my_pub = True
    has_priv = os.path.isfile("private key.json") # имеется ли приватный ключ
    print(f"Найдено: {('Публичный ключ' if has_pub else '') + (', ' if has_pub and has_priv else '') + ('Приватный ключ' if has_priv else '') or '-'}\n")
    with open("settings.json","r", encoding="utf-8") as f:
        data_settings = json.load(f)
        using_password_for_key = data_settings.get("using_password_for_key")
    if has_pub:
        try:
            if has_notmy_pub:
                with open("public key.json","r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"----ПУБЛИЧНЫЙ КЛЮЧ(e, n)----\ne = {data['e']}\nn = {data['n']}\n")
            else:
                with open("my public key.json","r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"----ПУБЛИЧНЫЙ КЛЮЧ(e, n)----\ne = {data['e']}\nn = {data['n']}\n")
        except Exception as e:
            print(f"Ошибка чтения публичного ключа: {e}")
    if has_priv:
        try:
            with open("private key.json","r", encoding="utf-8") as f:
                data = json.load(f)
            if using_password_for_key:
                salt = bytes.fromhex(data["salt"])
                nonce = bytes.fromhex(data["nonce"])
                tag = bytes.fromhex(data["tag"])
                ciphertext = bytes.fromhex(data["ciphertext"])
                aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                secrets = json.loads(decrypted_bytes.decode('utf-8'))
                data = {
                    "n": data["n"],
                    "d": secrets["d"],
                    "p": secrets["p"],
                    "q": secrets["q"]
                }
            print(f"----ПРИВАТНЫЙ КЛЮЧ(d, n, p, q)----\nd = {data['d']}\nn = {data['n']}\np = {data['p']}\nq = {data['q']}\n")
        except Exception as e:
            print(f"Ошибка чтения приватного ключа: {e}")
    input("Чтобы продолжить, нажмите Enter")

def generate_keys(): # создание обоих ключей(перезаписывание если уже есть)
    global password
    if os.path.isfile("settings.json"):
        with open ("settings.json", "r", encoding = "utf-8") as f:
            data_settings = json.load(f)
        using_password_for_key = data_settings.get("using_password_for_key")
    else:
        with open ("settings.json", "w", encoding = "utf-8") as f:
            data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True}
            json.dump(data_settings, f, indent=4)
        using_password_for_key = False
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice_1 = input("При создании новой пары ключей, прошлая пара исчезнет. Пара ключей хранятся в той же папке, что и этот файл\n(1) Продолжить\n(9) Отмена\n(0) Выйти\n").strip()
        if(choice_1 in ["1","9","0"]):
            if (choice_1 == "1"):
                print("Создание ключей...")
                # Генерируем объект закрытого ключа (внутри уже содержатся p, q, d, n, e)
                private_key_obj = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048
                )
                # Извлекаем математические параметры из объекта ключа
                private_numbers = private_key_obj.private_numbers()
                e = private_numbers.public_numbers.e
                n = private_numbers.public_numbers.n
                d = private_numbers.d
                p = private_numbers.p
                q = private_numbers.q
                if using_password_for_key:
                    raw_key = {
                        "n": n,
                        "d": d,
                        "p": p,
                        "q": q,
                    }
                    #password глобальный
                    secrets = {
                        "d": raw_key["d"],
                        "p": raw_key["p"],
                        "q": raw_key["q"]
                    }
                    secrets_bytes = json.dumps(secrets).encode('utf-8')
                    salt = os.urandom(16)
                    nonce = os.urandom(12)
                    aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                    ciphertext, tag = cipher.encrypt_and_digest(secrets_bytes)
                    private_key = {
                        "n": raw_key["n"], 
                        "salt": salt.hex(),
                        "nonce": nonce.hex(),
                        "tag": tag.hex(),
                        "ciphertext": ciphertext.hex()
                    }
                else:
                    private_key = {"d": d, "p": p, "q": q, "n": n}
                public_key = {"e": e, "n": n}
                with open("my public key.json", 'w', encoding="utf-8") as f: 
                    json.dump(public_key, f, indent=4)
                    print("публичный ключ создан и сохранен в файл")
                with open("private key.json",'w', encoding="utf-8") as f:
                    json.dump(private_key, f, indent=4)
                    print("приватный ключ создан и сохранен в файл")
                    input("\nЧтобы продолжить, нажмите Enter")
                break
            if (choice_1 == "9"):
                break
            if(choice_1 == "0"):
                sys.exit()

def save_pub_key(): #Сохранение своего публичного ключа
    if os.path.isfile("private key.json"):
        with open("private key.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        e = 65537
        n = data["n"]
        print("\nПолучены данные из приватного ключа")
        with open("my public key.json", 'w', encoding="utf-8") as f:
            public_key = {"e": e, "n":n}
            json.dump(public_key, f, indent=4)
            print("Публичный ключ создан и сохранен в файл")
    else:
        print("Не найден приватный ключ. Вернитесь в меню генерации для того, чтобы создать новую пару ключей")
    input("\n\nЧтобы продолжить, нажмите Enter")
        
def crypter(): #Шифровщик сообщения. Вызывается из главного меню кнопкой №1
    global password
    os.system('cls' if os.name == "nt" else 'clear')
    if (os.path.isfile("public key.json") or os.path.isfile("my public key.json")) and os.path.isfile("private key.json"):
        if os.path.isfile("my public key.json") and not os.path.isfile("public key.json"):
            print("Внимание: сейчас используется ваш публичный ключ")
            whokey="my"
        else:
            whokey=None
        if whokey=="my":
            with open("my public key.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                e = data["e"]
                n = data["n"]
        else:
            with open("public key.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                e = data["e"]
                n = data["n"]
        if os.path.isfile("settings.json"):
            with open ("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
            autocopy = data_settings["autocopy"]
            using_password_for_key = data_settings["using_password_for_key"]
            if using_password_for_key:
                with open ("private key.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                salt = bytes.fromhex(data["salt"])
                nonce = bytes.fromhex(data["nonce"])
                tag = bytes.fromhex(data["tag"])
                ciphertext = bytes.fromhex(data["ciphertext"])
                aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                secrets = json.loads(decrypted_bytes.decode('utf-8'))
                data = {
                    "n_priv": data["n"],
                    "d": secrets["d"],
                    "p": secrets["p"],
                    "q": secrets["q"]
                }
                d=data["d"]
                q=data["q"]
                p=data["p"]
                n_priv=data["n_priv"]
            else:
                with open ("private key.json", "r", encoding="utf-8") as f:
                    data_priv = json.load(f)
                d = data_priv["d"]
                p = data_priv["p"]
                q = data_priv["q"]
                n_priv = data_priv["n"]
            d = int(d)
            p = int(p)
            q = int(q)
            n_priv = int(n_priv)
        else:
            data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True}
            with open ("settings.json", "w", encoding="utf-8") as f:
                json.dump(data_settings, f, indent=4)
        message = input("Введите сообщение или введите 0 для выхода в главное меню:\n").strip()
        if message == "":
            print("Вы ничего не ввели и нажали Enter")
        elif message == "0":
            print("Вы вышли из создания сообщения")
        else:
            # 1. Вычисляем CRT параметры, которые требует библиотека
            dmp1 = rsa.rsa_crt_dmp1(d, p)
            dmq1 = rsa.rsa_crt_dmq1(d, q)
            iqmp = rsa.rsa_crt_iqmp(p, q)
            # 2. Восстанавливаем программные объекты ключей RSA из чисел e, d, n
            # Это необходимо, чтобы библиотека понимала, с какими ключами работает
            public_key_obj = rsa.RSAPublicNumbers(e, n).public_key()
            private_key_obj = rsa.RSAPrivateNumbers(
                p=p, q=q, d=d, dmp1=dmp1, dmq1=dmq1, iqmp=iqmp, 
                public_numbers=rsa.RSAPublicNumbers(e, n_priv)
            ).private_key()
            # генерация AES
            aes_key = Fernet.generate_key()
            encrypt_aes = Fernet(aes_key)
            # Сжимаем сообщение (уровень 9 — максимальный)
            compressed_message = zlib.compress(message.encode('utf-8'), level=9)
            # Шифровка через AES
            crypted_message = encrypt_aes.encrypt(compressed_message)
            # 3. ИСПОЛЬЗУЕМ OAEP: Шифруем сам ключ AES через RSA
            # Библиотека автоматически накладывает случайную соль, XOR-маску и делает операцию pow()
            crypted_aes_bytes = public_key_obj.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            crypted_aes_key = base64.b64encode(crypted_aes_bytes).decode('utf-8')
            encoded_message = crypted_message.decode('utf-8')
            final_message = f"{crypted_aes_key}:{encoded_message}"
            # 4. ИСПОЛЬЗУЕМ PSS: Создаем современную цифровую подпись
            # Передаем сжатое сообщение (исходный массив байт) напрямую в метод подписи
            signature_bytes = private_key_obj.sign(
                compressed_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            signature = base64.b64encode(signature_bytes).decode('utf-8')
            # Готовое сообщение
            final_packet = f"{final_message}|{signature}"
            print("Вот зашифрованное сообщение:")
            print(final_packet)
            if data_settings["autocopy"]:
                pyperclip.copy(final_packet)
                print("Скопированно в буфер обмена")
    else:
        if not os.path.isfile("public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not os.path.isfile("private key.json"):
            print("Не найдено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")
    input("\nЧтобы продолжить, нажмите Enter")

def uncrypter(): #Расшифровщик сообщения. Вызывается из главного меню кнопкой №2
    global password
    os.system('cls' if os.name == 'nt' else 'clear')
    if (os.path.isfile("public key.json") or os.path.isfile("my public key.json")) and os.path.isfile("private key.json"):
        if os.path.isfile("my public key.json") and not os.path.isfile("public key.json"):
            whokey="my"
        else:
            whokey=None
        if whokey=="my":
            with open("my public key.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                e = data["e"]
                n_pub = data["n"]
        else:
            with open("public key.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                e = data["e"]
                n_pub = data["n"]
        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True}
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(data_settings, f, indent=4)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                full_data = input("Вставьте зашифрованную строку или введите 0 для выхода в главное меню:\n").strip()
                if full_data == "0":
                    print("Вы вышли из расшифрования сообщения")
                    break
                else:
                    if "|" in full_data:
                        main_data, signature_b64 = full_data.rsplit("|", 1) 
                        signature_bytes = base64.b64decode(signature_b64)
                        signature = int.from_bytes(signature_bytes, byteorder='big')
                        # Разделяем ключ и сообщение
                        crypted_aes_key_str, encoded_message = main_data.rsplit(":", 1)
                        if data_settings.get("using_password_for_key"):
                            with open ("private key.json", "r", encoding="utf-8") as f:
                                data = json.load(f)
                            salt = bytes.fromhex(data["salt"])
                            nonce = bytes.fromhex(data["nonce"])
                            tag = bytes.fromhex(data["tag"])
                            ciphertext = bytes.fromhex(data["ciphertext"])
                            aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                            cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                            decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                            secrets = json.loads(decrypted_bytes.decode('utf-8'))
                            data = {
                                "n_priv": data["n"],
                                "d": secrets["d"],
                                "p": secrets["p"],
                                "q": secrets["q"]
                            }
                            d=data["d"]
                            q=data["q"]
                            p=data["p"]
                            n_priv=data["n_priv"]
                        else:
                            with open("private key.json", "r", encoding="utf-8") as f:
                                data_priv=json.load(f)
                            d = data_priv["d"]
                            p = data_priv["p"]
                            q = data_priv["q"]
                            n_priv = data_priv["n"]
                        d = int(d)
                        p = int(p)
                        q = int(q)
                        n_priv = int(n_priv)
                        e = int(e)
                        # Рассчитываем CRT-компоненты для валидной сборки приватного ключа
                        n_pub = int(n_pub)
                        dmp1 = rsa.rsa_crt_dmp1(d, p)
                        dmq1 = rsa.rsa_crt_dmq1(d, q)
                        iqmp = rsa.rsa_crt_iqmp(p, q)
                        # Собираем официальные объекты ключей
                        public_key_obj = rsa.RSAPublicNumbers(e, n_pub).public_key()
                        private_key_obj = rsa.RSAPrivateNumbers(
                            p=p, q=q, d=d, dmp1=dmp1, dmq1=dmq1, iqmp=iqmp,
                            public_numbers=rsa.RSAPublicNumbers(e, n_priv)
                        ).private_key()
                        # Декодируем байты зашифрованного AES ключа
                        crypted_aes_key_bytes = base64.b64decode(crypted_aes_key_str)
                        # 1. Снимаем OAEP-дополнение и получаем чистый AES-ключ Fernet
                        aes_key = private_key_obj.decrypt(
                            crypted_aes_key_bytes,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        # Расшифровываем сообщение через AES
                        uncoded_aes = Fernet(aes_key)
                        decrypted_compressed = uncoded_aes.decrypt(encoded_message.encode('utf-8'))
                        # 2. Проверяем цифровую подпись PSS штатными средствами библиотеки
                        try:
                            public_key_obj.verify(
                                signature_bytes,
                                decrypted_compressed,  # Проверяем хэш именно от сжатых байт
                                padding.PSS(
                                    mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.MAX_LENGTH
                                ),
                                hashes.SHA256()
                            )
                            # Если метод .verify() не вызвал исключение InvalidSignature, значит подпись верна
                            print("\nПОДПИСЬ ПОДТВЕРЖДЕНА: Сообщение подлинное (не поддельное)")
                        except Exception:
                            print("!!!!\nВНИМАНИЕ: Подпись НЕ верна! Сообщение подделано или повреждено")
                        # Распаковываем текст в любом случае (даже при битой подписи, как в вашем оригинале)
                        decrypted_message = zlib.decompress(decrypted_compressed).decode('utf-8')
                        print(f"Текст: {decrypted_message}")
                        break
                    else:
                        print("Ошибка: отсутствует подпись")
                        break
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
    input("\nЧтобы продолжить, нажмите Enter")

def import_export_key(mode):
    if os.path.isfile("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as f:
            data_settings = json.load(f)
    else:
        data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True}
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)
    autocopy = data_settings["autocopy"]
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        logo_2 = [
        r" ██╗  ██╗     ██████╗    ███████╗ ",
        r" ██║  ██║    ██╔════╝    ██╔════╝ ",
        r" ███████║    ██║         ███████╗ ",
        r" ██╔══██║    ██║         ╚════██║ ",
        r" ██║  ██║    ╚██████╗    ███████║ ",
        r" ╚═╝  ╚═╝     ╚═════╝    ╚══════╝ ",
        r" ──────────────────────────────── ",
        r"     HYBRID CRYPTO SYSTEM v0.5    ",
        r" █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ ",
        r" █       IMPORT/EXPORT KEY      █ ",
        r" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
    ]
        if logo_choice == 1:
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
        ##       HYBRID CRYPTO SYSTEM v0.5     ##
        #########################################
                    IMPORT/EXPORT KEY              
''')
        elif logo_choice == 2:
            for line in logo_2:
                print(line.rstrip().center(width))
        if mode == "import":
            choice_3 = input("\nВнимание: прошлый публичный ключ перезапишется(возможно)\n(1)Продолжить\n(9)Назад в главное меню\n(0)Выйти\n")
            if choice_3 == "1":
                try:
                    input_key = input("Введите ключ: ")
                    if ":" in input_key:
                        e_str, n_str = input_key.split(":", 1)
                        e, n = int(e_str), int(n_str)
                        with open("public key.json", "w", encoding="utf-8") as f:
                            public_key = {"e": e, "n":n}
                            json.dump(public_key, f, indent=4)
                    else:
                        print("В этом ключе отсутствует разделитель!")
                    input("\nЧтобы продолжить, нажмите Enter")
                    break
                except Exception:
                    print("Ошибка в чтении ключа")
                    input("\nЧтобы продолжить, нажмите Enter")
            elif choice_3 == "9":
                return
            elif choice_3 == "0":
                sys.exit()
        elif mode == "export":
            if os.path.isfile("public key.json") or os.path.isfile("my public key.json"):
                try:
                    if os.path.isfile("my public key.json"):
                        with open("my public key.json", "r", encoding="utf-8") as f:
                            data = json.load(f)
                    else:
                        with open("public key.json", "r", encoding="utf-8") as f:
                            data = json.load(f)
                    print_key = f"{data['e']}:{data['n']}"
                    print("")
                    print(print_key)
                    if autocopy == True:
                        pyperclip.copy(print_key)
                        print("Скопираванно в буфер обмена")
                    input("\nЧтобы продолжить, нажмите Enter")
                    break
                except Exception:
                    input("Ошибка чтения и вывода файла\n\nНажмите Enter, чтобы вернуться")
                    break
            else:
                input("\nНе найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ\n\nНажмите Enter, чтобы вернуться")
                break

def settings():
    global password
    global logo_choice
    i=0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = os.get_terminal_size().columns
        logo_2 = [
        r" ██╗  ██╗     ██████╗    ███████╗ ",
        r" ██║  ██║    ██╔════╝    ██╔════╝ ",
        r" ███████║    ██║         ███████╗ ",
        r" ██╔══██║    ██║         ╚════██║ ",
        r" ██║  ██║    ╚██████╗    ███████║ ",
        r" ╚═╝  ╚═╝     ╚═════╝    ╚══════╝ ",
        r" ──────────────────────────────── ",
        r"     HYBRID CRYPTO SYSTEM v0.5    ",
        r" █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ ",
        r" █           SETTINGS           █ ",
        r" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█ "
    ]
        if logo_choice == 1:
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
        ##       HYBRID CRYPTO SYSTEM v0.5     ##
        #########################################
                        SETTINGS              
''')
        elif logo_choice == 2:
            for line in logo_2:
                print(line.rstrip().center(width))
        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            with open("settings.json", "w", encoding="utf-8") as f:
                data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True, "secretpswd":False}
                json.dump(data_settings, f, indent=4)
        choice_settings = input(f'''
    МЕНЮ НАСТРОЕК
(1) Пароль - {data_settings.get("password")}
(2) Шифрование приватного ключа паролем - {data_settings.get("using_password_for_key")}
(3) Автокопирование - {data_settings.get("autocopy")}
(4) Формат логотипа - {data_settings.get("logo")} / 2
(5) Скрытый ввод пароля на экране - {data_settings.get("secretpswd")}
(9) Выйти в главное меню
(0) Выйти
''').strip()
        if choice_settings in ["1","2","3", "4", "5", "9","0"]:
            if choice_settings == "1":
                if data_settings.get("password"):
                    if data_settings.get("using_password_for_key"):
                        if os.path.isfile("private key.json"):
                            try:
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                print(data)
                                salt = bytes.fromhex(data["salt"])
                                nonce = bytes.fromhex(data["nonce"])
                                tag = bytes.fromhex(data["tag"])
                                ciphertext = bytes.fromhex(data["ciphertext"])
                                print(salt)
                                print(nonce)
                                print(tag)
                                print(ciphertext)
                                aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                                cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                                decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                                secrets = json.loads(decrypted_bytes.decode('utf-8'))
                                full_private_key = {
                                    "n": data["n"],
                                    "d": secrets["d"],
                                    "p": secrets["p"],
                                    "q": secrets["q"]
                                }
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(full_private_key, f, indent=4)
                                data_settings["using_password_for_key"] = False
                                data_settings["password"] = False
                                password = None
                                os.remove("password.txt")
                                print("Вход с паролем выключен")
                                print("Шифрование приватного ключа паролем Выключено")
                            except Exception as e:
                                print("Не удалось расшифровать ключ", e)
                        else:
                            password = None
                            data_settings["using_password_for_key"] = False
                            data_settings["password"] = False
                            os.remove("password.txt")
                            print("Вход с паролем выключен")
                            print("Шифрование приватного ключа паролем Выключено")
                    else:
                        password = None
                        data_settings["password"] = False
                        os.remove("password.txt")
                        ("Вход с паролем выключен")
                else:
                    if data_settings.get("secretpswd"):
                        password = getpass.getpass("Введите новый пароль от 8 символов: ").strip()
                    else:
                        password = input("Введите новый пароль от 8 символов: ").strip()
                    password_bytes = password.encode('utf-8')
                    if len(password) < 8:
                        print("Ошибка: Пароль слишком короткий. Минимальное значение - 8 символов")
                    else:
                        sha256_bytes = hashlib.sha256(password_bytes).digest()
                        hashed_password = bcrypt.hashpw(sha256_bytes, bcrypt.gensalt())
                        with open("password.txt", "w", encoding="utf-8") as f:
                            f.write(hashed_password.decode('utf-8'))
                        data_settings["password"] = True
            elif choice_settings == "2":
                if data_settings.get("password"):
                    if data_settings.get("using_password_for_key"):
                        if os.path.isfile("private key.json"):
                            try:
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                salt = bytes.fromhex(data["salt"])
                                nonce = bytes.fromhex(data["nonce"])
                                tag = bytes.fromhex(data["tag"])
                                ciphertext = bytes.fromhex(data["ciphertext"])
                                aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                                cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                                decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                                secrets = json.loads(decrypted_bytes.decode('utf-8'))
                                full_private_key = {
                                    "n": data["n"],
                                    "d": secrets["d"],
                                    "p": secrets["p"],
                                    "q": secrets["q"]
                                }
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(full_private_key, f, indent=4)
                                data_settings["using_password_for_key"] = False
                                print("Шифрование приватного ключа паролем Выключено")
                            except Exception:
                                print("Не удалось расшифровать ключ: ")
                        else:
                            data_settings["using_password_for_key"] = False
                            print("Шифрование приватного ключа паролем Выключено")
                    else:
                        try:
                            if os.path.isfile("private key.json"):
                                with open("private key.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                raw_key = {
                                    "n": data["n"],
                                    "d": data["d"],
                                    "p": data["p"],
                                    "q": data["q"],
                                }
                                #password глобальный
                                secrets = {
                                    "d": raw_key["d"],
                                    "p": raw_key["p"],
                                    "q": raw_key["q"]
                                }
                                secrets_bytes = json.dumps(secrets).encode('utf-8')
                                salt = os.urandom(16)
                                nonce = os.urandom(12)
                                aes_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
                                cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                                ciphertext, tag = cipher.encrypt_and_digest(secrets_bytes)
                                data = {
                                    "n": raw_key["n"], 
                                    "salt": salt.hex(),
                                    "nonce": nonce.hex(),
                                    "tag": tag.hex(),
                                    "ciphertext": ciphertext.hex()
                                }
                                with open("private key.json", "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=4)
                                data_settings["using_password_for_key"] = True
                                print("Шифрование приватного ключа паролем Включено")
                            else:
                                data_settings["using_password_for_key"] = True
                                print("Шифрование приватного ключа паролем Включено")
                        except Exception as e:
                            print("Не удалось зашифровать ключ: ", e)
                else:
                    print("Эта функция недоступна: у вас не установлен пароль")
            elif choice_settings == "3":
                data_settings["autocopy"] = not data_settings["autocopy"]
            elif choice_settings == "4":
                if logo_choice == 1:
                    logo_choice = 2
                elif logo_choice == 2:
                    logo_choice = 1
                else:
                    logo_choice = 2
                data_settings["logo"] = logo_choice
                with open("settings.json", "w", encoding="utf-8") as f:
                    json.dump(data_settings, f, indent=4)
            elif choice_settings == "5":
                data_settings["secretpswd"] = not data_settings["secretpswd"]
            elif choice_settings == "9":
                return
            elif choice_settings == "0":
                sys.exit()
            input("Для продолжения нажмите Enter")
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)
# Импорт критически важных библиотек и запуск
import sys, subprocess
required = ['sympy', 'cryptography', 'pyperclip', 'bcrypt', 'Crypto']
missing = []
for lib in required:
    try:
        __import__(lib)
    except ImportError as e:
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
import random, os, json, base64, secrets, hashlib, zlib
import shutil
import pyperclip
import bcrypt
import getpass
from sympy import mod_inverse, nextprime #Математические функции для генерации ключей
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet #Для AES ключа
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
try:
    Start()
except Exception as e:
    input(f"\n[!]Произошла непредвиденная ошибка: {e}\nНажмите Enter, чтобы выйти...")
    sys.exit()
