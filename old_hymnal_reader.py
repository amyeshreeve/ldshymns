from PyPDF2 import PdfFileReader

reader = PdfFileReader("1835_hymnal.pdf")
count = 6
f = open("1835_hymnal.txt", "w", encoding="utf-8")

while count <= 123:
	page = reader.pages[count]
	words = page.extractText()
	words = words.replace('\n', ' ')
	words = words.replace('SACRED', '')
	words = words.replace('HYMNS', '')
	f.write(words)
	count += 1

f.close()
hymnal = open('1835_hymnal.txt', 'r', encoding="utf-8").read()

hymns = hymnal.split(" HYMN")
number = 0
while number < 93:
	title = "HYMN" + str(number)
	filename = title + ".txt"
	hymn = hymns[number]
	f = open(filename, "w", encoding="utf-8")
	f.write(hymn)
	f.close()
	number += 1