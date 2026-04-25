import socket
import random
import os
from checksum import checksum, verify_checksum

HOST = "127.0.0.1"
PORT = 11111
OUTPUT_FILE = "received_file.txt"
LOSS_PROB = 0.3


def lost():
    return random.random() < LOSS_PROB


def send_ack(sock, addr, seq):
    if lost():
        print(f"ACK {seq} потерян")
        return
    sock.sendto(bytes([seq]), addr)
    print(f"Отправлен ACK {seq}")


def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    expected_seq = 0
    print("Сервер запущен")

    try:
        with open(OUTPUT_FILE, "wb") as f:
            while True:
                packet, client_addr = sock.recvfrom(2048)

                if lost():
                    print("Пакет потерян")
                    continue

                seq = packet[0]
                received_check = int.from_bytes(packet[1:3], "big")
                data = packet[3:]
                payload = bytes([seq]) + data

                if not verify_checksum(payload, received_check):
                    print("Ошибка контрольной суммы")
                    continue                

                if data == b"EOF":
                    send_ack(sock, client_addr, seq)
                    print("Файл получен.")
                    break

                if seq == expected_seq:
                    f.write(data)
                    print(f"Получен пакет {seq}")
                    send_ack(sock, client_addr, seq)
                    expected_seq ^= 1
                else:
                    print(f"Дубликат пакета {seq}")
                    send_ack(sock, client_addr, seq)

    except Exception as e:
        print("Ошибка сервера:", e)

    finally:
        sock.close()


if __name__ == "__main__":
    main()