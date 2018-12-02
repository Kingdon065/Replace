#! python3

import chardet

# 说明：UTF兼容ISO8859-1和ASCII，GB18030兼容GBK，GBK兼容GB2312，GB2312兼容ASCII
CODES = ['ASCII', 'UTF-8', 'GBK', 'GB18030', 'BIG5', 'UTF-16',
         'UTF-16BE', 'UTF-16LE', 'UTF-32', 'UTF-32BE', 'UTF-32LE'
         ]
# UTF-8 BOM前缀字节
UTF_8_BOM = b'\xef\xbb\xbf'


def file_encoding(file_path: str):
    """
    获取文件编码类型

    :param file_path: 文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        return string_encoding(f.read())


def string_encoding(data: bytes):
    """
    获取字符编码类型

    :param data: 字节数据
    :return:
    """
    # 遍历编码类型
    for code in CODES:
        try:
            data.decode(encoding=code)
            if 'UTF-8' == code and data.startswith(UTF_8_BOM):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    return 'unknown'

def check_encoding(s):
    """
    get file encoding or bytes charset
    速度较慢

    :param s: file path or bytes data

    :return: encoding charset
    """

    if type(s) == str:
        f = open(s, 'rb')
        buffer = f.read()
        result = chardet.detect(buffer)
        return result['encoding']

    elif type(s) == bytes:
        result = chardet.detect(s)
        return result['encoding']

    else:
        raise TypeError('Unsupported parameter types!')