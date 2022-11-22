from flask import Flask, render_template, request, jsonify
import requests
import time
import chat_predict
from flask_cors import CORS
import sqlite3

from flask_paginate import Pagination, get_page_parameter
app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

# Test-------------------

@app.route('/test')
def i():  # put application's code here
    return render_template("test.html")



#------------------------------


@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/movie')
def movie():

    datalist = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from JaktentEvent"
    data =cur.execute(sql)
    #print(data)
    for item in data :
        datalist.append(item)

    cur.close()
    conn.close()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    start = (page - 1) * limit
    end = start + limit
    res = datalist[start:end]
    pagination = Pagination(page=page, total=len(datalist), per_page=limit)
    return render_template("movie.html", movies=res, pagination=pagination)


@app.route('/score')
def score():
    return render_template("score.html")

@app.route('/team')
def team():
    return render_template("wordcloud.html")

@app.route('/re')
def re():
    a = request.args.get("b")
    print(a)
    datalist = []
    rdata = []
    pdata = []

    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()

    sql2 = "select * from JaktentEvent"
    data2 = cur.execute(sql2)
    for item in data2:
        if a in item[0]:
            rdata.append(item)

    num = rdata[0][9]


    sql1 = "select id2 from similar where number > 0.2 and id = ?"
    v = (num,)
    data1 = cur.execute(sql1,v)
    for i in data1:
        datalist.append(i[0])
    print(datalist)

    for item in datalist:
        sql3 = "select * from JaktentEvent where id = ? "
        v = (item,)
        data3 = cur.execute(sql3,v)
        for a in data3:
            pdata.append(a)

    cur.close()
    conn.close()

    return render_template("wordcloud.html",movies = pdata )

@app.route('/word')
def word():
    datalist = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from JaktentSpeaker"
    data =cur.execute(sql)

    for item in data :
        datalist.append(item)


    cur.close()
    conn.close()
    page2 = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    start = (page2 - 1) * limit
    end = start + limit
    res = datalist[start:end]
    pagination = Pagination(page=page2, total=len(datalist), per_page=limit)
    return render_template("word.html", speakers=res, pagination=pagination)



@app.route('/searchword')
def searchword():
    p = request.args.get("p")

    datalist = []

    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()

    sql = "select * from JaktentSpeaker "
    data = cur.execute(sql)
    print(data)
    for item in data:
        if p in item[0]:
            datalist.append(item)
    cur.close()
    conn.close()

    page2 = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    start = (page2 - 1) * limit
    end = start + limit
    res = datalist[start:end]
    pagination = Pagination(page=page2, total=len(datalist), per_page=limit)
    return render_template("word.html", speakers=res, pagination=pagination)


@app.route('/search')
def search():
    q = request.args.get("q")

    datalist = []

    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()

    sql = "select * from JaktentEvent "
    data = cur.execute(sql)

    for item in data:
        if q in item[0]:
            datalist.append(item)
    cur.close()
    conn.close()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    start = (page - 1) * limit
    end = start + limit
    res = datalist[start:end]
    pagination = Pagination(page=page, total=len(datalist), per_page=limit)
    return render_template("movie.html", movies=res, pagination=pagination)

# Flask construction for word frequency analysis
@app.route('/Filmmaking')
def F():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Filmmaking' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Literature')
def L():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Literature' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Digital-technology')
def D():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Digital-technology' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Food-industry')
def Food():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Food-industry' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Pandemic')
def P():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Pandemic' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Social-media')
def S():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Social-media' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Children')
def C():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Children' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Book-industry')
def B():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Book-industry' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Virtual-film-class')
def V():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Virtual-film-class' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/Feminism')
def Fe():
    list = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select * from content"
    data =cur.execute(sql)
    print(type(data))
    for item in data :
        if 'Feminism' in item[1] :
            list.append(item[0])
    print(list)
    datalist = []
    for item in list:
        sql = "select * from JaktentEvent where id = ? "
        v = (item,)
        dat = cur.execute(sql,v)
        for i in dat:
            datalist.append(i)
    cur.close()
    conn.close()

    return render_template("event.html",movies = datalist)

@app.route('/predict1', methods=['POST'])
def update_task():
    # Solve the cross-domain problem of data transmission when the front-end and back-end are separated and developed
    CORS(app, supports_credentials=True,resources=r'/*')
    input = request.form.get('input')
    result = chat_predict.predict([input])
    result = result.replace('\n', '<br/>')

    # connect the database
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "insert into recording(question,recording) values(?,?) "

    cur.execute(sql,(input,result))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'result':result})


if __name__ == '__main__':
    app.run()
