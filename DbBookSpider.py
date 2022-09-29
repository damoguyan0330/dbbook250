# -8- coding = utf-8 -*-
# @Time : 2022/9/23 16:25
# @File : DbBookSpider.py
# @Software : PyCharm

import requests,time,sqlite3,os
import fake_useragent
from lxml import etree
import xlwt

def get_page(url):
    time.sleep(0.5)
    page = requests.get(headers=headers,url=url).text
    # print(page)
    # with open('dbbook.html','w',encoding='utf-8') as f:
    #     f.write(page)
    return page

def parse_page():
    datalist = []
    for i in range(10):
        url = base_url + str(i*25)
        page = get_page(url)
        tree = etree.HTML(page)
        table_list = tree.xpath('//*[@id="content"]/div/div[1]/div/table')
        # print(table_list)
        for table in table_list:
            data = []
            book_detail_src = table.xpath('./tr/td[1]/a/@href')[0]
            data.append(book_detail_src)
            img_src = table.xpath('./tr/td[1]/a/img/@src')[0]
            data.append(img_src)
            cname = table.xpath('./tr/td[2]/div[1]/a/@title')[0]
            print(f'正在爬取{cname}')
            data.append(cname)
            ename_f = table.xpath('./tr/td[2]/div[1]/span/text()')
            if len(ename_f) == 0:
                ename = ''
            else:
                ename = ename_f[0]
            data.append(ename)

            author = table.xpath('./tr/td[2]/p[1]/text()')[0]
            data.append(author)
            rate = table.xpath('./tr/td[2]/div[2]/span[2]/text()')[0]
            data.append(rate)
            c_num = table.xpath('./tr/td[2]/div[2]/span[3]/text()')[0].split('\n')[1].strip().split('人')[0]
            data.append(c_num)
            short_comment = table.xpath('./tr/td[2]/p[2]/span/text()')
            if len(short_comment) == 0:
                short_comment = ''
            else:
                short_comment = short_comment[0]
            data.append(short_comment)
            # print(data)
            datalist.append(data)
    print(datalist)
    return datalist

def saveToE():
    datalist = parse_page()
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('豆瓣图书top250', cell_overwrite_ok=False)
    col = ('图书详情链接','图书图片链接','图书中文名','图书英文名','作者','豆瓣评分','评价人数','短评')
    for i in range(8):
        sheet.write(0,i,col[i])
    for a in range(len(datalist)):
        # print(f'正在爬取第{a+1}本书')
        data = datalist[a]
        # print(data)
        for b in range(8):
            sheet.write(a+1,b,data[b])
    book.save('豆瓣图书top250.xls')


def init_db():
    # if not os.path.exists(db_path):
    #     os.mkdir(db_path)
    if os.path.exists(db_path):
        os.remove(db_path)
    sql = '''
    create table book250
    (
    id integer primary key autoincrement,
    info_link text,
    pic_link text,
    cname varchar,
    ename varchar,
    author varchar,
    score numeric,
    rated numeric,
    instroduction text
    )
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveToDb():
    init_db()
    datalist = parse_page()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for data in datalist:
        print('data>>>',data)
        for i in range(len(data)):
            if i == 5 or i == 6:
                continue
            else:
                data[i] = '"' + data[i] + '"'
        sql = '''insert into book250(info_link,pic_link,cname,ename,author,score,rated,instroduction) values(%s)'''%','.join(data)
        print(sql)

        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    ua = fake_useragent.UserAgent().random
    headers = {
        'User-Agent':ua
    }
    # print(ua)
    t_1 = time.strftime("%Y_%m_%d_%X",time.localtime()).split(':')
    t = '_'.join(t_1)
    # print(t)

    db_path = f'book_{t}.db'
    # print(db_path)


    base_url = f'https://book.douban.com/top250?start='
    # print(base_url)
    # parse_page()

    # saveToE()
    saveToDb()

