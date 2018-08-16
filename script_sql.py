# -*- coding: utf-8 -*-
#put in cmd.exe: chcp 65001 (utf-8)
#SEO-продвижение и оптимизация сайта с результатами: http://seo-infnet.ru/
import requests
import json
import psycopg2
import time

def parsing_html(page):
    page_metrika = requests.get(page, verify=False)
    json_format = page_metrika.json()
    json_metrics = json.loads(page_metrika.text)
    return json_metrics

def connect(dbname, user, host, password):
    access = "dbname='%s' user='%s' host='%s' password='%s'" % (dbname, user, host, password)
    with psycopg2.connect(access) as conn:
        cur = conn.cursor()
        return 'Connected! \n'
        global conn
        global cur

def insertion(keyword, searchsystem, visit, bouncerate, deeppage, visittime):
    query = """INSERT INTO stats (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime) VALUES (DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s')""" % (keyword, searchsystem, visit, bouncerate, deeppage, visittime)
    return (query)

def execute_insert(sql):
    try:
        cur.execute(sql)
        conn.commit()
        return 'SQL Success!'
    except:
        return 'I can\'t write!'

def view_stats(sql_query):
    cur.execute(sql_query)
    rows = cur.fetchall()
    global rows

def close_con():
    cur.close()


if __name__ == "__main__":
    print(connect('panel', 'postgres', 'localhost', 'asdwx123'))
    html = parsing_html('https://api-metrika.yandex.ru/stat/v1/data?preset=sources_search_phrases&limit=10000&pretty=true&date1=2015-08-10&date2=2018-08-11&id=23220061&oauth_token=AQAAAAACPju0AAUlKa2hb5GQsEVOrhj984J9NYk')
    for l in html['data']:
        list_dim = []
        list_met = []
        for k in l['dimensions']:
            list_dim.append(k['name'])
        for p in l['metrics']:
            list_met.append(p)
        sql_query = insertion(list_dim[0].replace("'", ""), list_dim[1], list_met[0], list_met[2], list_met[3], list_met[4])
        print(sql_query)
        print(execute_insert(sql_query))
        time.   sleep (0.5)
    close_con()
    '''print(connect('panel', 'postgres', 'localhost', ''))
    sql_elements = view_stats("""SELECT * FROM stats WHERE searchsystem = 'Яндекс' LIMIT 10""")
    for elements in rows:
        print(elements)
    close_con()'''