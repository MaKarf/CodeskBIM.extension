import binascii


def string_to_byte_array():
    """Python 2.x version"""
    date = raw_input("Enter date in yyyy-mm-dd format: ")
    """Convert the string to a byte array"""
    byte_array = bytearray(date)

    """Convert the byte array to a byte string (hexadecimal representation)"""
    byte_string = binascii.hexlify(byte_array)

    print(byte_string)
