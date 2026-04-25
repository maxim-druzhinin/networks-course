def checksum(data):
    if len(data) % 2:
        data += b"\x00"

    total = sum( int.from_bytes(data[i:i + 2], "big") for i in range(0, len(data), 2))

    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)

    return (~total) & 0xFFFF


def verify_checksum(data: bytes, check: int):
    if len(data) % 2:
        data += b"\x00"
    return checksum(data + check.to_bytes(2, "big")) == 0


def run_tests():
    data = b"A crude awakening"
    check = checksum(data)

    print("Test 1:", verify_checksum(data, check))        # True
    print("Test 2:", verify_checksum(b"A cude awacening", check))  # False

    odd_data = b"abc"
    odd_check = checksum(odd_data)

    print("Test 3:", verify_checksum(odd_data, odd_check))    # True


if __name__ == "__main__":
    run_tests()