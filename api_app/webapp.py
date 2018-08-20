import postgresql
import json
import flask
from flask import request

app = flask.Flask(__name__)

def db_conn():
    return postgresql.open('pq://postgres@localhost/panel')

def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def stats_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" + " to application/json?")
        return (None, errors)

    for field_name in ['id', 'keyword']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(
          field_name))

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/stats/')

# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})


@app.route('/api/1.0/stats/', methods=['GET'])
def get_stats():
    with db_conn() as db:
        tuples = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats")
        stats = []
        for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime ) in tuples:
            stats.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
        return resp(200, {"stats": stats})


@app.route('/api/1.0/stats/<int:stats_id>', methods=['GET'])
def get_stats_id(stats_id):
    with db_conn() as db:
        listes = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats WHERE id = %s" % (stats_id))
        stats = [] 
        for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime) in listes:
            stats.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
        return resp(200, {"stats": stats})


@app.route('/api/1.0/stats/search/', methods=['GET'])
def search():
    searchword = request.args.get('query', '')
    if searchword != '':
        stats = []
        with db_conn() as db:
            listes = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats WHERE keyword LIKE '%"+str(searchword)+"%'")
            stats = []
            for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime) in listes:
                stats.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
            return resp(200, {"stats": stats})
    else:
        return resp(404)

if __name__ == '__main__':
    app.run()