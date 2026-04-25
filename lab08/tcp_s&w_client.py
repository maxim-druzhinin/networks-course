import socket
import random
from checksum import checksum

HOST = "127.0.0.1"
PORT = 11111
INPUT_FILE = "good_file.txt"
LOSS_PROB = 0.3


def lost():
    return random.random() < LOSS_PROB


def send_packet(sock, packet, seq):
    while True:
        if lost():
            print(f"Пакет {seq} потерян при отправке")
        else:
            packet_to_send = packet

            if random.random() < 0.15 and len(packet_to_send) > 5:
                print("Пакет повреждён!")
                packet_to_send = bytearray(packet_to_send)
                packet_to_send[5] ^= 0xFF
                packet_to_send = bytes(packet_to_send)

            sock.sendto(packet_to_send, (HOST, PORT))
            print(f"Отправлен пакет {seq}")

        try:
            ack, _ = sock.recvfrom(1)
            ack_num = ack[0]

            if ack_num == seq:
                print(f"Получен ACK {ack_num}")
                return

        except socket.timeout:
            print(f"Таймаут, повторная отправка пакета {seq}")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)

    seq = 0

    try:
        with open(INPUT_FILE, "rb") as f:
            while True:
                data = f.read(1024)

                if not data:
                    break

                payload = bytes([seq]) + data
                check = checksum(payload)
                packet = bytes([seq]) + check.to_bytes(2, "big") + data

                send_packet(sock, packet, seq)

                seq ^= 1

        payload = bytes([seq]) + b"EOF"
        check = checksum(payload)
        eof_packet = bytes([seq]) + check.to_bytes(2, "big") + b"EOF"
        send_packet(sock, eof_packet, seq)

        print("Передача завершена")

    except Exception as e:
        print("Ошибка клиента:", e)

    finally:
        sock.close()


if __name__ == "__main__":
    main()