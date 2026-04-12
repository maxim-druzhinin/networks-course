from ftplib import FTP, error_perm
import sys
import os

HOST = "ftp.dlptest.com"
PORT = 21
LOGIN = "dlpuser"
PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"


def print_usage():
    print("\n".join([
        "Usage:",
        "client.py -ls",
        "client.py -get [filename]",
        "client.py -put [filename]"
    ]))


ftp = FTP()

try:
    ftp.connect(HOST, PORT)
    ftp.login(LOGIN, PASSWORD)
    print(ftp.getwelcome())

    if len(sys.argv) == 1:
        print_usage()
        ftp.quit()
        sys.exit(1)

    command = sys.argv[1]

    if command == "-ls":
        if len(sys.argv) != 2:
            print("Usage: client.py -ls")
            ftp.quit()
            sys.exit(1)

        for obj in ftp.nlst():
            print(obj)

    elif command == "-get":
        if len(sys.argv) != 3:
            print("Usage: client.py -get [filename]")
            ftp.quit()
            sys.exit(1)

        filename = sys.argv[2]

        with open(filename, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)

        print(f"Файл '{filename}' успешно скачан")

    elif command == "-put":
        if len(sys.argv) != 3:
            print("Usage: client.py -put [filename]")
            ftp.quit()
            sys.exit(1)

        filename = sys.argv[2]

        if not os.path.exists(filename):
            print(f"Файл '{filename}' не существует")
            ftp.quit()
            sys.exit(1)

        with open(filename, "rb") as f:
            ftp.storbinary(f"STOR {filename}", f)

        print(f"Файл '{filename}' успешно загружен")

    else:
        print(f"Неизвестная команда: {command}")
        print_usage()
        ftp.quit()
        sys.exit(1)

    ftp.quit()

except FileNotFoundError:
    print("Ошибка: локальный файл не найден")
    try:
        ftp.quit()
    except:
        pass
    sys.exit(1)

except error_perm as e:
    print(f"FTP ошибка: {e}")
    try:
        ftp.quit()
    except:
        pass
    sys.exit(1)

except Exception as e:
    print(f"Ошибка: {e}")
    try:
        ftp.quit()
    except:
        pass
    sys.exit(1)