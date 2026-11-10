logo_choice = 2
logo = 2
print("Запуск скрипта...")
print("Версия: release 0.6")
class KeyManager:
    def __init__(self, key_file="private key.json"):
        self.key_file = key_file
        self._secret_buf = None
        self._pwd_buf = None
        self.is_unlocked = False

    def set_password(self, password: str = None):
        self._wipe(self._pwd_buf)
        self._pwd_buf = bytearray(password.encode("utf-8")) if password else None

    def get_password(self) -> str:
        return self._pwd_buf.decode("utf-8") if self._pwd_buf else None

    def _derive_key(self, password: str, salt: bytes) -> bytearray:
        raw_key = Argon2id(salt=salt,length=32,iterations=3,lanes=4,memory_cost=65536,).derive(password.encode("utf-8"))
        return bytearray(raw_key)

    def _wipe(self, buf: bytearray):
        if buf:
            for i in range(len(buf)):
                buf[i] = 0

    def set_keys(self, n: int, d: int, p: int, q: int):
        """Удобный метод, чтобы положить в память только что сгенерированные ключи."""
        self._wipe(self._secret_buf)
        full_keys = {"n": n, "d": d, "p": p, "q": q}
        self._secret_buf = bytearray(json.dumps(full_keys).encode("utf-8"))
        self.is_unlocked = True

    def get_key_parts(self) -> dict:
        """Возвращает словарь: n, d, p, q."""
        if not self.is_unlocked or self._secret_buf is None:
            raise RuntimeError("Ключи заблокированы или не загружены")
        return json.loads(self._secret_buf.decode("utf-8"))

    def load_keys(self, password: str = None) -> bool:
        """Загружает ключи с диска в память (сам понимает, зашифрован файл или нет)."""
        if not os.path.isfile(self.key_file):
            return False

        with open(self.key_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "ciphertext" in data:
            if not password:
                raise ValueError("Ключ зашифрован, требуется пароль")

            salt = bytes.fromhex(data["salt"])
            nonce = bytes.fromhex(data["nonce"])
            tag = bytes.fromhex(data["tag"])
            ciphertext = bytes.fromhex(data["ciphertext"])

            aes_key = self._derive_key(password, salt)
            try:
                decrypted = bytearray(
                    AESGCM(bytes(aes_key)).decrypt(nonce, ciphertext + tag, None)
                )
            finally:
                self._wipe(aes_key)

            secrets = json.loads(decrypted.decode("utf-8"))
            self._wipe(decrypted)
        else:
            secrets = data

        self.set_keys(data["n"], secrets["d"], secrets["p"], secrets["q"])
        if password:
            self.set_password(password)
        return True

    def _atomic_write(self, data_dict: dict):
        target_dir = os.path.dirname(os.path.abspath(self.key_file))
        fd, tmp_path = tempfile.mkstemp(dir=target_dir, prefix=".tmp_key_")
        try:
            if os.name != "nt":
                os.chmod(tmp_path, 0o600)

            with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
                json.dump(data_dict, tmp_file, indent=4)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            os.replace(tmp_path, self.key_file)

            if os.name != "nt":
                os.chmod(self.key_file, 0o600)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

    def save_encrypted(self, password: str = None):
        """Шифрует d, p, q через Argon2id + AES-GCM и сохраняет на диск."""
        pwd = password or self.get_password()
        if not pwd:
            raise ValueError("Не задан пароль для шифрования ключа")
        parts = self.get_key_parts()

        secrets_bytes = bytearray(
            json.dumps({"d": parts["d"], "p": parts["p"], "q": parts["q"]}).encode("utf-8")
        )

        salt = os.urandom(16)
        nonce = os.urandom(12)
        aes_key = self._derive_key(pwd, salt)

        try:
            encrypted = AESGCM(bytes(aes_key)).encrypt(nonce, bytes(secrets_bytes), None)
        finally:
            self._wipe(aes_key)
            self._wipe(secrets_bytes)

        data = {
            "n": parts["n"],
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "tag": encrypted[-16:].hex(),
            "ciphertext": encrypted[:-16].hex()
        }
        self._atomic_write(data)

    def save_plain(self):
        """Сохраняет n, d, p, q в открытом виде."""
        self._atomic_write(self.get_key_parts())

    def lock(self):
        """Затирает буферы с ключами и паролем нулями в памяти."""
        self._wipe(self._secret_buf)
        self._wipe(self._pwd_buf)
        self._secret_buf = None
        self._pwd_buf = None
        self.is_unlocked = False

    def __del__(self):
        self.lock()

# Создаем один глобальный объект хранилища для всего скрипта
vault = KeyManager("private key.json")

def Start():
    global logo_choice
    user_password = None
    has_pub = os.path.isfile("public key.json") or os.path.isfile("my public key.json")
    has_priv = os.path.isfile("private key.json")
    has_settings = os.path.isfile("settings.json")

    if has_settings:
        with open("settings.json", "r", encoding="utf-8") as f:
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
                        vault.set_password(user_password)
                        if has_priv:
                            try:
                                t0 = time.perf_counter()
                                vault.load_keys(user_password)
                                unlock_ms = (time.perf_counter() - t0) * 1000
                                if data_settings.get("developermode"):
                                    print("----- Режим разрабочика -----")
                                    print(f"Argon2id + AES-GCM расшифровка заняла {unlock_ms:.1f} мс")
                                    print(f"В памяти заблокировано: {len(vault._secret_buf)} байт (bytearray)")
                                    input(f"----- Режим разрабочика -----\nНажмите Enter...")
                            except Exception as e:
                                print(f"Ошибка загрузки приватного ключа: {e}")
                                input("Нажмите Enter...")
                        break
                else:
                    print("Ошибка: Проверка пароля есть, а файла пароля нет. Настройки изменены. Если у вас был зашифрован приватный ключ, пересоздайте пару")
                    data_settings["password"] = False
                    data_settings["using_password_for_key"] = False
                    with open("settings.json", "w", encoding="utf-8") as f:
                        json.dump(data_settings, f, indent=4)
                    user_password = None
                    break
    else:
        data_settings = {"logo": 2, "checkupdates": True, "developermode": False}

    # Если пароль на вход не стоял, но файл ключа есть — грузим его в память
    if has_priv and not vault.is_unlocked:
        try:
            vault.load_keys()
        except Exception as e:
            print(f"Ошибка загрузки приватного ключа: {e}")

    logo_choice = int(data_settings.get("logo", 2))
    if data_settings.get("developermode"):
        print(f"\n-----Режим разработчика-----")
        print(json.dumps(data_settings, indent=4, ensure_ascii=False))
        input(f"----------------------------\nEnter для продолжения")
    if data_settings.get("checkupdates", True):
        check_updates(True, data_settings.get("developermode", False))
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
        r"     HYBRID CRYPTO SYSTEM v0.6    ",
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
        ##       HYBRID CRYPTO SYSTEM v0.6     ##
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
            r"     HYBRID CRYPTO SYSTEM v0.6    ",
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
            ##       HYBRID CRYPTO SYSTEM v0.6     ##
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
        r"     HYBRID CRYPTO SYSTEM v0.6    ",
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
        ##       HYBRID CRYPTO SYSTEM v0.6     ##
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
                        vault.lock()
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
    if os.path.isfile("settings.json"):
        with open("settings.json","r", encoding="utf-8") as f:
            data_settings = json.load(f)
            using_password_for_key = data_settings.get("using_password_for_key")
    else:
        data_settings = {"developermode": False}
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
            if vault.is_unlocked:
                priv_data = vault.get_key_parts()
                print(f"----ПРИВАТНЫЙ КЛЮЧ(d, n, p, q)----\nd = {priv_data['d']}\nn = {priv_data['n']}\np = {priv_data['p']}\nq = {priv_data['q']}\n")
                if data_settings.get("developermode"):
                    with open("private key.json", "r", encoding="utf-8") as f:
                        disk_data = json.load(f)
                    print("--- Режим разработчика [СОСТОЯНИЕ ФАЙЛА НА ДИСКЕ] ---")
                    if "ciphertext" in disk_data:
                        print(f"Статус: ЗАШИФРОВАН (Argon2id + AES-GCM)")
                        print(f"Salt (16 байт): {disk_data['salt']}")
                        print(f"Nonce (12 байт): {disk_data['nonce']}")
                        print(f"GCM Tag (16 байт): {disk_data['tag']}")
                        print(f"Длина шифротекста: {len(bytes.fromhex(disk_data['ciphertext']))} байт")
                    else:
                        print("Статус: ОТКРЫТЫЙ ВИД (не зашифрован)")
                    print("-----------------------------------------------------\n")
            else:
                print("Приватный ключ заблокирован.\n")
        except Exception as e:
            print(f"Ошибка чтения приватного ключа: {e}")
    input("Чтобы продолжить, нажмите Enter")

def generate_keys(): # создание обоих ключей(перезаписывание если уже есть)
    if os.path.isfile("settings.json"):
        with open ("settings.json", "r", encoding = "utf-8") as f:
            data_settings = json.load(f)
    else:
            data_settings = {"password": False, "using_password_for_key": False, "logo": 2, "autocopy": True, "msgsize": 1, "developermode": False, "checkupdates": True}
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice_1 = input("При создании новой пары ключей, прошлая пара исчезнет. Пара ключей хранятся в той же папке, что и этот файл\n(1) Продолжить\n(9) Отмена\n(0) Выйти\n").strip()
        if(choice_1 in ["1","9","0"]):
            if (choice_1 == "1"):
                print("Создание ключей...")
                if data_settings.get("msgsize") == "1":
                    msgsize=2048
                elif data_settings.get("msgsize") == "2":
                    msgsize=3072
                else:
                    msgsize=4096
                # Генерируем объект закрытого ключа (внутри уже содержатся p, q, d, n, e)
                t0 = time.perf_counter()
                private_key_obj = rsa.generate_private_key(public_exponent=65537, key_size=msgsize)
                gen_time = time.perf_counter() - t0
                # Извлекаем математические параметры из объекта ключа
                private_numbers = private_key_obj.private_numbers()
                e = private_numbers.public_numbers.e
                n = private_numbers.public_numbers.n
                d = private_numbers.d
                p = private_numbers.p
                q = private_numbers.q
                vault.set_keys(n, d, p, q)
                if data_settings.get("using_password_for_key") and vault.get_password():
                    vault.save_encrypted()
                else:
                    vault.save_plain()
                print("Приватный ключ создан и сохранен в файл")
                public_key = {"e": e, "n": n}
                with open("my public key.json", 'w', encoding="utf-8") as f: 
                    json.dump(public_key, f, indent=4)
                print("Публичный ключ создан и сохранен в файл")
                if data_settings.get("developermode"):
                    print("\n--- Режим разработчика ---")
                    print(f"Время генерации RSA-{msgsize}: {gen_time:.3f} сек.")
                    print(f"Длина p: {p.bit_length()} бит | Длина q: {q.bit_length()} бит")
                    print(f"Длина модуля n: {n.bit_length()} бит")
                    print("\n--------------------------\n")
                    input("\nЧтобы продолжить, нажмите Enter")
                break
            elif choice_1 == "9":
                break
            elif choice_1 == "0":
                vault.lock()
                sys.exit()

def save_pub_key(): #Сохранение своего публичного ключа
    if vault.is_unlocked:
        priv_data = vault.get_key_parts()
        e = 65537
        n = priv_data["n"]
        print("\nПолучены данные из приватного ключа")
        with open("my public key.json", 'w', encoding="utf-8") as f:
            public_key = {"e": e, "n": n}
            json.dump(public_key, f, indent=4)
        print("Публичный ключ создан и сохранен в файл")
    else:
        print("Не найден или не загружен приватный ключ. Вернитесь в меню генерации для создания новой пары ключей")
    input("\n\nЧтобы продолжить, нажмите Enter")
        
def crypter():  # Шифровщик сообщения. Вызывается из главного меню кнопкой №1
    os.system('cls' if os.name == "nt" else 'clear')
    if (os.path.isfile("public key.json") or os.path.isfile("my public key.json")) and vault.is_unlocked:
        if os.path.isfile("my public key.json") and not os.path.isfile("public key.json"):
            print("Внимание: сейчас используется ваш публичный ключ")
            pub_file = "my public key.json"
        else:
            pub_file = "public key.json"

        with open(pub_file, "r", encoding="utf-8") as f:
            pub_data = json.load(f)
            e = int(pub_data["e"])
            n = int(pub_data["n"])

        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            data_settings = {"password": False, "using_password_for_key": False, "logo": 2, "autocopy": True, "msgsize": 1, "developermode": False, "checkupdates": True}

        keys = vault.get_key_parts()
        d = int(keys["d"])
        p = int(keys["p"])
        q = int(keys["q"])
        n_priv = int(keys["n"])

        message = input("Введите сообщение или введите 0 для выхода в главное меню:\n").strip()
        if message == "":
            print("Вы ничего не ввели и нажали Enter")
        elif message == "0":
            print("Вы вышли из создания сообщения")
        else:
            # 1. Вычисляем CRT параметры
            dmp1 = rsa.rsa_crt_dmp1(d, p)
            dmq1 = rsa.rsa_crt_dmq1(d, q)
            iqmp = rsa.rsa_crt_iqmp(p, q)

            # 2. Восстанавливаем объекты ключей RSA
            public_key_obj = rsa.RSAPublicNumbers(e, n).public_key()
            private_key_obj = rsa.RSAPrivateNumbers(
                p=p, q=q, d=d, dmp1=dmp1, dmq1=dmq1, iqmp=iqmp,
                public_numbers=rsa.RSAPublicNumbers(e, n_priv)
            ).private_key()

            # Генерация AES и сжатие
            aes_key = Fernet.generate_key()
            encrypt_aes = Fernet(aes_key)
            raw_msg_bytes = message.encode('utf-8')
            compressed_message = zlib.compress(raw_msg_bytes, level=9)
            crypted_message = encrypt_aes.encrypt(compressed_message)

            # 3. OAEP шифрование ключа AES (длина строго равна размеру ключа получателя в байтах)
            crypted_aes_bytes = public_key_obj.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # 4. PSS цифровая подпись (длина строго равна размеру нашего ключа в байтах)
            signature_bytes = private_key_obj.sign(
                compressed_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Склеиваем сырые байты подряд без разделителей и кодируем в единый Base64
            raw_packet = crypted_aes_bytes + crypted_message + signature_bytes
            final_packet = base64.b64encode(raw_packet).decode('utf-8')

            if data_settings.get("developermode"):
                print("\n--- Режим разработчика ----------------")
                print(f"Ключ собеседника (n): {n.bit_length()} бит ({len(crypted_aes_bytes)} байт)")
                print(f"Наш ключ подписи (n_priv): {n_priv.bit_length()} бит ({len(signature_bytes)} байт)")
                print(f"Текст: {len(raw_msg_bytes)} байт -> zlib: {len(compressed_message)} байт -> Fernet: {len(crypted_message)} байт")
                print(f"Итоговый сырой пакет: {len(raw_packet)} байт -> Base64: {len(final_packet)} символов")
                print("---------------------------------------\n")

            print("Вот зашифрованное сообщение:")
            print(final_packet)
            if data_settings.get("autocopy"):
                pyperclip.copy(final_packet)
                print(f"\n*Скопировано в буфер обмена*")
    else:
        if not os.path.isfile("public key.json") and not os.path.isfile("my public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not vault.is_unlocked:
            print("Не найдено или не загружено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")
    input("\nЧтобы продолжить, нажмите Enter")


def uncrypter():  # Расшифровщик сообщения. Вызывается из главного меню кнопкой №2
    os.system('cls' if os.name == 'nt' else 'clear')
    if (os.path.isfile("public key.json") or os.path.isfile("my public key.json")) and vault.is_unlocked:
        if os.path.isfile("my public key.json") and not os.path.isfile("public key.json"):
            pub_file = "my public key.json"
        else:
            pub_file = "public key.json"

        with open(pub_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            e = int(data["e"])
            n_pub = int(data["n"])

        if os.path.isfile("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                data_settings = json.load(f)
        else:
            data_settings = {"password": False, "using_password_for_key": False, "logo": 2, "autocopy": True, "msgsize": 1, "developermode": False, "checkupdates": True}

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                full_data = input("Вставьте зашифрованную строку или введите 0 для выхода в главное меню:\n").strip()
                if full_data == "0":
                    print("Вы вышли из расшифрования сообщения")
                    break
                else:
                    # Декодируем единый массив сырых байт
                    raw_packet = base64.b64decode(full_data)

                    # Достаем наши ключи из памяти
                    keys = vault.get_key_parts()
                    d = int(keys["d"])
                    p = int(keys["p"])
                    q = int(keys["q"])
                    n_priv = int(keys["n"])

                    # Вычисляем точные размеры блоков в байтах по длине модулей n
                    priv_len = (n_priv.bit_length() + 7) // 8  # Длина зашифрованного AES-ключа
                    pub_len = (n_pub.bit_length() + 7) // 8    # Длина подписи собеседника

                    # Защита от слишком коротких или обрезанных строк
                    if len(raw_packet) <= priv_len + pub_len:
                        print("Ошибка: пакет поврежден или слишком короткий для текущих ключей")
                        break

                    # Разрезаем пакет без разделителей
                    crypted_aes_key_bytes = raw_packet[:priv_len]
                    signature_bytes = raw_packet[-pub_len:]
                    crypted_message_bytes = raw_packet[priv_len:-pub_len]

                    if data_settings.get("developermode"):
                        print("\n--- Режим разработчика ------------")
                        print(f"Всего получено байт: {len(raw_packet)}")
                        print(f"Отрезано AES-ключа (по нашему n_priv {n_priv.bit_length()} бит): {len(crypted_aes_key_bytes)} байт")
                        print(f"Отрезано подписи (по n_pub собеседника {n_pub.bit_length()} бит): {len(signature_bytes)} байт")
                        print(f"Тело сообщения: {len(crypted_message_bytes)} байт")
                        print("----------------------------------\n")

                    # Рассчитываем CRT-компоненты для валидной сборки приватного ключа
                    dmp1 = rsa.rsa_crt_dmp1(d, p)
                    dmq1 = rsa.rsa_crt_dmq1(d, q)
                    iqmp = rsa.rsa_crt_iqmp(p, q)

                    # Собираем официальные объекты ключей
                    public_key_obj = rsa.RSAPublicNumbers(e, n_pub).public_key()
                    private_key_obj = rsa.RSAPrivateNumbers(
                        p=p, q=q, d=d, dmp1=dmp1, dmq1=dmq1, iqmp=iqmp,
                        public_numbers=rsa.RSAPublicNumbers(e, n_priv)
                    ).private_key()

                    # 1. Снимаем OAEP-дополнение и получаем чистый AES-ключ Fernet
                    aes_key = private_key_obj.decrypt(
                        crypted_aes_key_bytes,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )

                    # Расшифровываем сообщение через AES (передаем байты напрямую)
                    uncoded_aes = Fernet(aes_key)
                    decrypted_compressed = uncoded_aes.decrypt(crypted_message_bytes)

                    # 2. Проверяем цифровую подпись PSS (пишем только если есть проблема)
                    try:
                        public_key_obj.verify(
                            signature_bytes,
                            decrypted_compressed,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                        )
                    except Exception:
                        print("\n[!] ВНИМАНИЕ: Подпись НЕ верна! Сообщение подделано или повреждено")

                    # Распаковываем текст
                    decrypted_message = zlib.decompress(decrypted_compressed).decode('utf-8')
                    print(f"Текст: {decrypted_message}")
                    break
            except ValueError:
                print("Ошибка: Возможно, ключ не подходит или сообщение повреждено")
                break
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}\nВозможно, сообщение или ключ повреждены")
                break
    else:
        if not os.path.isfile("public key.json") and not os.path.isfile("my public key.json"):
            print("Не найдено: публичный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей или восстановить, если имеется приватный ключ")
        if not vault.is_unlocked:
            print("Не найдено или не загружено: приватный ключ\nЧтобы его создать, нужно сгенерировать новую пару ключей")
    input("\nЧтобы продолжить, нажмите Enter")

def import_export_key(mode):
    if os.path.isfile("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as f:
            data_settings = json.load(f)
    else:
        data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True, "secretpswd":False, "msgsize": 1, "developermode": False, "checkupdates": True}
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
        r"     HYBRID CRYPTO SYSTEM v0.6    ",
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
        ##       HYBRID CRYPTO SYSTEM v0.6     ##
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
        r"     HYBRID CRYPTO SYSTEM v0.6    ",
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
        ##       HYBRID CRYPTO SYSTEM v0.6     ##
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
            data_settings = {"password":False,"using_password_for_key":False,"logo": 2,"autocopy":True, "secretpswd":False, "msgsize": 1, "developermode": False, "checkupdates": True}
        choice_settings = input(f'''
    МЕНЮ НАСТРОЕК
(1) Пароль - {data_settings.get("password")}
(2) Шифрование приватного ключа паролем - {data_settings.get("using_password_for_key")}
(3) Автокопирование - {data_settings.get("autocopy")}
(4) Формат логотипа - {data_settings.get("logo")} / 2
(5) Скрытый ввод пароля на экране - {data_settings.get("secretpswd")}
(6) Выбор длины ключа - {data_settings.get("msgsize")} /3
(7) Режим разработчика - {data_settings.get("developermode")}
(8) Автоматическая проверка обновлений - {data_settings.get("checkupdates")}
(9) Выйти в главное меню
(0) Выйти
''').strip()
        if choice_settings in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            if choice_settings == "1":
                if data_settings.get("password"):
                    # Выключаем вход по паролю
                    if data_settings.get("using_password_for_key"):
                        try:
                            if vault.is_unlocked:
                                vault.save_plain()
                            data_settings["using_password_for_key"] = False
                            print("Шифрование приватного ключа паролем Выключено")
                        except Exception as e:
                            print("Не удалось расшифровать ключ:", e)
                            # Если расшифровать не вышло — прерываем отключение пароля, чтобы не потерять доступ
                            continue

                    vault.set_password(None)
                    data_settings["password"] = False
                    if os.path.isfile("password.txt"):
                        os.remove("password.txt")
                    print("Вход с паролем выключен")

                else:
                    # Включаем вход по паролю
                    if data_settings.get("secretpswd"):
                        new_password = getpass.getpass("Введите новый пароль от 8 символов: ").strip()
                    else:
                        new_password = input("Введите новый пароль от 8 символов: ").strip()

                    if len(new_password) < 8:
                        print("Ошибка: Пароль слишком короткий. Минимальное значение - 8 символов")
                    else:
                        vault.set_password(new_password)
                        password_bytes = new_password.encode('utf-8')
                        sha256_bytes = hashlib.sha256(password_bytes).digest()
                        hashed_password = bcrypt.hashpw(sha256_bytes, bcrypt.gensalt())
                        with open("password.txt", "w", encoding="utf-8") as f:
                            f.write(hashed_password.decode('utf-8'))
                        data_settings["password"] = True
                        print("Вход с паролем включен")

            elif choice_settings == "2":
                if data_settings.get("password"):
                    if data_settings.get("using_password_for_key"):
                        # Выключаем шифрование ключа
                        try:
                            if vault.is_unlocked:
                                vault.save_plain()
                            data_settings["using_password_for_key"] = False
                            print("Шифрование приватного ключа паролем Выключено")
                        except Exception as e:
                            print("Не удалось сохранить ключ в открытом виде:", e)
                    else:
                        # Включаем шифрование ключа
                        try:
                            if vault.is_unlocked:
                                vault.save_encrypted()
                            data_settings["using_password_for_key"] = True
                            print("Шифрование приватного ключа паролем Включено")
                        except Exception as e:
                            print("Не удалось зашифровать ключ:", e)
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
            elif choice_settings == "6":
                msgsize = input(f"Справка: реальной роли почти не играет из-за гибридной системы, но сильнее грузит процессор\nВыберите размер ключа:\n1) 2048 Стандарт\n2) 3072 Лучше\n3) 4096 Максимально\n")
                if msgsize.strip() in ["1", "2", "3"]:
                    data_settings["msgsize"] = msgsize
                else:
                    print("Вы не выбрали")
            elif choice_settings == "7":
                data_settings["developermode"] = not data_settings["developermode"]
            elif choice_settings == "8":
                data_settings["checkupdates"] = not data_settings["checkupdates"]
            elif choice_settings == "9":
                return
            elif choice_settings == "0":
                sys.exit()
            input("Для продолжения нажмите Enter")
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(data_settings, f, indent=4)
            
CURRENT_VERSION = "0.6"
RAW_SCRIPT_URL = "https://raw.githubusercontent.com/v0mp1r/HCS/main/HCS.py"
RELEASES_URL = "https://github.com/v0mp1r/HCS/releases"
def check_updates(silent=False, developermode=False):
    """Проверяет наличие новой версии на GitHub и открывает страницу скачивания в браузере."""
    try:
        if not silent:
            print("Проверка обновлений...")

        req = urllib.request.Request(RAW_SCRIPT_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            remote_code = response.read().decode('utf-8')

        # Ищем строчку CURRENT_VERSION = "..." в коде на GitHub
        match = re.search(r'CURRENT_VERSION\s*=\s*["\']([^"\']+)["\']', remote_code)
        if not match:
            if not silent:
                print("Не удалось определить версию на сервере.")
            return

        remote_version = match.group(1)

        if remote_version != CURRENT_VERSION:
            print(f"\n[!] Доступно обновление: {CURRENT_VERSION} -> {remote_version}")
            choice = input("Открыть страницу скачивания в браузере? (1 - Да / 2 - Позже): ").strip()
            if choice == "1":
                webbrowser.open(RELEASES_URL)
                print("Страница открыта в браузере.")
        else:
            if not silent:
                print(f"У вас установлена актуальная версия ({CURRENT_VERSION}).")
        if developermode == True:
            print("----- Режим разрабочика -----")
            print(f"[DEV MODE] Запрос к: {RAW_SCRIPT_URL}")
            print(f"[DEV MODE] HTTP Статус: {response.status} | Локальная версия: {CURRENT_VERSION} | На сервере: {remote_version}")
            print("-----------------------------")
    except Exception as e:
        if not silent:
            print(f"Не удалось проверить обновления: {e}")
    if developermode == True:
        input(f"\nEnter для продолжения")

# Импорт критически важных библиотек и запуск
import sys, subprocess, random, os, json, base64, secrets, hashlib, zlib, tempfile, shutil, pyperclip, bcrypt, getpass, urllib.request, re, webbrowser, time
required = ['cryptography', 'pyperclip', 'bcrypt']
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
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
try:
    Start()
except Exception as e:
    input(f"\n[!]Произошла непредвиденная ошибка: {e}\nНажмите Enter, чтобы выйти...")
    sys.exit()
