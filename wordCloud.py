# -8- coding = utf-8 -*-
# @Time : 2022/9/27 17:15
# @File : wordCloud.py
# @Software : PyCharm


import jieba
import sqlite3

from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


conn = sqlite3.connect('book.db')
cur = conn.cursor()
sql = '''select instroduction from book250'''
data = cur.execute(sql)
print(data)
text = ''
for item in data:
    # print(type(item))
    text = text + item[0]
# print(text)
cur.close()
conn.close()

cut = jieba.cut(text)
# print(cut)
wordlist = []
for word in cut:
    if word == '的':
        continue
    else:
        wordlist.append(word)
# print(wordlist)
string = ' '.join(wordlist)
# string = ' '.join(cut)
# print(string)

img = Image.open('3.jpg')
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='simkai.ttf'
)
wc.generate_from_text(string)

fig = plt.figure()
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig('book_word.jpg',dpi=500)
print('保存完毕')



