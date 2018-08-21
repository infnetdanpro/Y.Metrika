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


def tags_validate():
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
    return flask.redirect('/api/1.0/tags/')

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


@app.route('/api/1.0/tags/', methods=['GET'])
def get_tags():
    with db_conn() as db:
        tuples = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats")
        tags = []
        for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime ) in tuples:
            tags.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
        return resp(200, {"tags": tags})


@app.route('/api/1.0/tags/<int:tags_id>', methods=['GET'])
def get_tags_id(tags_id):
    with db_conn() as db:
        listes = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats WHERE id = %s" % (tags_id))
        tags = [] 
        for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime) in listes:
            tags.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
        return resp(200, {"tags": tags})


'''@app.route('/api/1.0/tags/search/', methods=['POST'])
def search():
    if not request.json:
        abort(400)
    print ((request.json['query']))
    return json.dumps(request.json)
    #return resp(200, {"tags": searchword})'''

@app.route('/api/1.0/tags/search/', methods=['POST'])
def search():
    searchword = (request.json['query'])
    if searchword:
        tags = []
        with db_conn() as db:
            listes = db.query("SELECT id, keyword, searchsystem, visit, bouncerate, deeppage, visittime FROM stats WHERE keyword LIKE '%"+str(searchword)+"%'")
            tags = []
            for (id, keyword, searchsystem, visit, bouncerate, deeppage, visittime) in listes:
                tags.append({"id": id, "keyword": keyword, "searchsystem": searchsystem, "bouncerate": bouncerate, "deeppage": deeppage, "visittime": visittime})
            return resp(200, {"tags": tags})
    else:
        return abort(400)

if __name__ == '__main__':
    app.run()