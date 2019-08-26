import _http, mydata
from flask import Flask, request
from flask.logging import create_logger
from flask.json import jsonify, JSONEncoder

devs_arr = mydata.devs_arr

app = Flask(__name__)
logger = create_logger(app)

@app.route("/")
def home():
    return 'Hello', 200

@app.route('/devs', methods=[_http.GET])
def devs():
    print('Type: {}'.format(request.is_xhr))
    return jsonify(devs_arr), 200

@app.route('/devs/<string:lang>', methods=[_http.GET])
def devs_per_lang(lang):
    devs_per_lang = [dev for dev in devs_arr if dev['lang'] == lang]
    return jsonify(devs_per_lang), 200

@app.route('/devs/<int:id>', methods=[_http.GET])
def devs_per_id(id):
    for dev in devs_arr:
        if dev['id'] == id:
            return jsonify(dev), 200
    return jsonify({'error': 'not found'}), 404

@app.route('/devs', methods=[_http.POST])
def save_dev():
    data = request.get_json()
    print('Tipo do dado: {}'.format(type(data)))
    print('Dado: {}'.format(data))
    data["id"] = len(devs_arr) + 1
    devs_arr.append(data)
    return jsonify(data), 201

@app.route('/devs/<int:id>', methods=[_http.PUT])
def update_dev(id):
    for dev in devs_arr:
        if dev['id'] == id:
            dev['lang'] = request.get_json()['lang']
            return jsonify(dev), 200
    return jsonify({'erro':'not found'}), 404

@app.route('/devs/<int:id>', methods=[_http.DELETE])
def delete_dev(id):
    devs_to_del = [dev for dev in devs_arr if dev['id'] == id]
    if len(devs_to_del) > 0:
        devs_arr.remove(devs_to_del[0])
        return jsonify(devs_to_del), 200
    else:
        return jsonify({'erro':'no deleted'}), 500


# start service
if __name__ == '__main__':
    app.run(debug=True)