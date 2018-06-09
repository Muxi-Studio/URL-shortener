"""
import random
upper_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_char = upper_char.lower()
number_char = "0123456789"
l=list(upper_char+lower_char+number_char)
random.shuffle(l)
print(l)
"""

"""
 使用随机的字符表表示62进制数，防止生成的短码具有连续性，
 该字符表一经生成不可改动
"""

base = ['4', 'F', 'k', 't', 'd', 'u', 'L', 'h', 'W', 'G', 'U', 'P',
        'X', 'q', 'H', '2', 'm', 'e', 'y', 'I', 'o', 'f', '5', 'b',
        'N', 'M', 'O', 'x', 'D', '0', 'r', 'Z', 's', 'n', '3', 'J',
        'c', '8', 'R', 'Q', 'z', 'S', '6', 'K', 'C', 'w', 'E', '1',
        'g', 'a', 'T', 'p', 'B', 'j', 'Y', 'V', '7', 'i', 'A', '9',
        'l', 'v']


def transform(_origin):
    if not _origin:
        return "4"
    result = ""
    while _origin:
        remainder = _origin % 62
        quotient = _origin // 62
        result += base[remainder]
        _origin = quotient
    return result

if __name__ == '__main__':
    print(transform(0))
    print(transform(1))
    print(transform(2))
    print(transform(100))
    print(transform(5002566555))
