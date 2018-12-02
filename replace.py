#!python3

import sys, re, os
from checkcoding import *


def openFile(argv_, coding_):
	try:
		f = open(argv_, 'r', encoding=coding_)
		strings_ = f.readlines()
		f.close()
		return strings_
	except Exception as exc:
		print('Error: {}'.format(exc))
		sys.exit()


def saveFile(filename_, strings_, coding_):
	f = open(filename_, 'w', encoding=coding_)
	for string in strings_:
		f.write(string)
	f.close()


def usage():
	print('''Usage: instead [-f] [filename] [str1] [str2]
       str2 instead of str1 in filename and save it''')


if (len(sys.argv) == 5):
	if sys.argv[1] == '-f':
		if os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2]):
			coding = file_encoding(sys.argv[2])
			strings = openFile(sys.argv[2], coding)

			Regex = re.compile(sys.argv[3])
			isFind = False
			
			for string in strings:
				mo = Regex.search(string)
				if mo:
					isFind = True
					temp = string
					string = Regex.sub(sys.argv[4], string)
					strings[strings.index(temp)] = string
					print('源字符串: ' + temp.strip())
					print('替换后: {}\n'.format(string.strip()))
					
			if isFind == False:
				print('没有找到字符串: ' + sys.argv[3])
				sys.exit()

			isSave = input('保存副本[1] 覆盖原文件[2] 取消保存[n] : ')
			if isSave.lower() == 'n':
				sys.exit()
			elif isSave.lower() == '1':
				new_filename = sys.argv[2][:-3] + ".bak" + sys.argv[2][-3:]
				saveFile(new_filename, strings, coding)
			elif isSave.lower() == '2':
				saveFile(sys.argv[2], strings, coding)
			else:
				sys.exit()

		else:
			print(sys.argv[2] + ' no exists or not file！')
	else:
		usage()
else:
	usage()
