# HCS - Hybrid Cripto System
## Содержание/Contents
1. [Как работает / How does it work?](#1-как-работаетhow-does-it-work)
2. [Как запустить / How to launch](#2-как-запуститьhow-to-launch)
3. [Как cкачать / How to download](#3-как-скачатьhow-to-download)
## 1. Как работает(How does it work)
####   RU: Используется ключ AES, который шифрует сам текст. Этот ключ меняется каждое сообщение. Этот AES ключ шифруется RSA шифрованием(публичным ключом). После этого создается цифровая подпись. По итогу есть 2 пары ключей - пользователи должны были обменяться публичными ключами, а приватные оставить у себя. Публичный ключ шифрует AES ключ, а приватный - расшифровывает. AES ключ в свою очередь, зашифровывает и расшифровывает текст. Подпись создается наоборот - приватным ключом, а расшифровывается публичным. У RSA всегда по одной паре ключей для каждого собеседника.
####   EN: An AES key is used to encrypt the text itself. This key changes with each message. This AES key is encrypted with RSA encryption (the public key). A digital signature is then created. This results in two key pairs—the users exchanged public keys and kept their private ones. The public key encrypts the AES key, and the private key decrypts it. The AES key, in turn, encrypts and decrypts the text. The signature is created the other way around—with the private key and decrypted with the public key. With RSA, there is always one key pair for each interlocutor.
## 2. Как запустить(How to launch)
####   RU: Запускается файл с расширением ".py", в основном это файл с именем "HCS.py", с помощью скачанного python. В более новых версиях будет находиться "HCS.exe" - скомпилированный ".exe" файл, по сути, являющийся тем же самым приложением, скомпилированным из того же ".py" приложения. Создано это для тех, у кого нету установленного python, так как ".exe" будет работать на любых ПК
####   EN: A file with the ".py" extension is launched, typically a file named "HCS.py," using the downloaded Python. Newer versions will contain "HCS.exe"—a compiled ".exe" file, essentially the same application compiled from the same ".py" application. This is designed for those who don't have Python installed, as the ".exe" will run on any PC.
## 3. Как скачать(How to download)
####  RU: Перейдите в раздел [Releases](../../releases) и скачайте актуальный релиз или бета-версию
#### EN: Go to the [Releases](../../releases) section and download the latest release or beta version
