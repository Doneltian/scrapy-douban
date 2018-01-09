import re
str = 'top250?start=0&filter='
str1 = 'top250?start=250&filter='
rx = re.compile('^top.*')
rx1 = re.compile('top250\?start\=\d&filter\=')
print(rx1.findall(str))
print(rx.findall(str1))
