from flask import Flask,render_template,request
import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,'book_2022_09_28_09_25_54.db')
app = Flask(__name__)


@app.route('/')
def index():
    # return 'Hello World!'
    return render_template('index.html')

@app.route('/index')
def home():
    return index()

from mypage import Pagination
@app.route('/book')
def book():
    datalist = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = 'select * from book250'
    data = cursor.execute(sql)
    for item in data:
        # print('item>>>',item)
        datalist.append(item)
    page_obj = Pagination(current_page=request.args.get("page", 1),all_count=len(datalist), per_page_num=50)
    index_list = datalist[page_obj.start:page_obj.end]
    html = page_obj.page_html()

    # path = request.path
    # pager_obj = Pagination(request.args.get("page", 1), len(datalist), path, request.args, per_page_count=10)
    # print('request.args>>>',request.args)
    # index_list = datalist[pager_obj.start:pager_obj.end]
    # html = pager_obj.page_html()


    return render_template("book.html", index_list=index_list, html=html)

# print('datalist>>>',datalist)
#     return render_template('book.html',books=datalist,page_obj=page_obj)

@app.route('/score')
def score():
    score = []
    num = []
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = 'select score,count(score) from book250 group by score'
    data = cur.execute(sql)
    for item in data:
        print(item)
        score.append(str(item[0]))
        num.append(item[1])
    return render_template('score.html',score=score,num=num)

@app.route('/word')
def wordcloud():

    return render_template('word.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
