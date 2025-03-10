import os

import flask

import PSQLWiter as psql

app = flask.Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

@app.route("/psql/add")
def parsing():
    global psql_client
    url = flask.request.args.get("url")
    if url:
        try:
            psql_client.write_data([[url]])
            return "Succesfully written.\n", 200
        except BaseException as error:
            return "Unexpected errors occured!\n", 500
    else:
        return "Argument missed!\n", 500

@app.route("/psql/data")
def get_data():
    global psql_client
    try:
        json_data = psql_client.write_data_to_json(None) 
    except BaseException as error:
        return "Unexpected errors occured!\n", 500
    return flask.Response(json_data, mimetype='application/json')

@app.route("/psql/clear")
def clear():
    global psql_client
    try:
        psql_client.clear_table()
    except BaseException as error:
        return "Unexpected errors occured!\n", 500
    return "Table succesfully cleaned.\n", 200

if __name__ == '__main__':
    psql_client = psql.PSQLwriter(DATABASE_URL, "links")
    if psql_client is None:
        quit()
    app.run(debug=True, host='0.0.0.0', port=5555)
