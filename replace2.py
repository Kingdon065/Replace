#!python3

import sys, re, os
import argparse, logging
from checkcoding import *
from Color.color import Colored


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class replace_string:
    def __init__(self, args):
        self.args = args
        self.color = Colored()
        if not os.path.exists(self.args.root):
            log.info('[{}] no exists.'.format(self.args.root))
            sys.exit()

        self.encoding = check_encoding(self.args.root)
        self.lines = []

    def openFile(self):
        try:
            with open(self.args.root, 'r', encoding=self.encoding) as f:
                self.lines = f.readlines()
        except Exception as exc:
            log.error(exc)
            sys.exit()

    def saveFile(self, filename):
        f = open(filename, 'w', encoding=self.encoding)
        for line in self.lines:
            f.write(line)
        f.close()

    def replace(self):
        self.openFile()
        str_regex = re.compile(self.args.regex)
        isFind = False
        print('\nINFO - 当前文件: {}'.format(self.args.root))
        i = 1
        for line in self.lines:
            mo = str_regex.search(line)
            if mo:
                isFind = True
                temp = line
                line = str_regex.sub(self.args.object, line)
                self.lines[self.lines.index(temp)] = line
                log.info('源字符串: #{} "{}"'.format(i, self.color.green(temp.strip())))
                log.info('替换之后: #{} "{}"\n'.format(i, self.color.yellow(line.strip())))
            i += 1

        if isFind == False:
            log.info('INFO - 没有匹配到字符串[{}]'.format(self.args.regex))
            return

        # 如果匹配到结果，不再询问，直接执行覆盖原文件操作，执行此操作前最好备份
        if self.args.is_force:
            self.saveFile(self.args.root)
            return

        isSave = input('INFO - 保存副本[1] 覆盖原文件[2] 取消保存[n] : ')

        if isSave.lower() == '1':
            tmp = self.args.root.split('.')
            ext = tmp[-1]
            new_filename = self.args.root[:-len(ext)-1] + ".bak." + ext
            self.saveFile(new_filename)
        elif isSave.lower() == '2':
            self.saveFile(self.args.root)
        else:
            return

def run():
    parser = argparse.ArgumentParser(
        prog='replace2',
        description='Replace text in a file, then save this file.',
        epilog="replace in multiple files, it's best to put the files you want to replace in the same folder"
    )
    parser.add_argument(
        'root',
        metavar='path',
        help='specify a filename or directory'
    )
    parser.add_argument(
        '-r',
        '--regex',
        nargs='?',
        required=True,
        help='specify a regex string'
    )
    parser.add_argument(
        '-o',
        '--object',
        nargs='?',
        required=True,
        help='specify object string'
    )
    parser.add_argument(
        '-e',
        '--exts',
        nargs='+',
        default=['py', 'c', 'cpp', 'h', 'txt', 'bat', 'bak', 'java'],
        help='a list of file extension'
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        dest='is_force',
        default=False,
        help="Do not ask, directly overwrite the original file"
    )

    args = parser.parse_args()

    # 处理多文件
    if os.path.exists(args.root) and os.path.isdir(args.root):
        os.chdir(args.root)
        for folder, sub_folders, filenames in os.walk('.'):
            folder = os.path.abspath(folder)
            for filename in filenames:
                if os.path.splitext(filename)[1][1:] in args.exts:
                    args.root = os.path.join(folder, filename)
                    rps = replace_string(args)
                    rps.replace()
        return
    # 处理单文件
    rs = replace_string(args)
    rs.replace()

if __name__ == '__main__':
    run()
