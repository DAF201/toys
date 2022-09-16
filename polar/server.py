from help import helper
import seedir
from flask import Flask, request, render_template, jsonify, send_from_directory
from file_handel import *
import func_timeout
import sys
app = Flask(__name__)


@app.errorhandler(500)
def error500(e):
    return jsonify({'error': str(e)})


@app.errorhandler(404)
def error404(e):
    return jsonify({'error': str(e)})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'icon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['get', 'post'])
def main_page():

    if 'WebKit' in str(request.headers):
        return render_template('home.html'), 418

    return helper


@app.route('/add', methods=['post'])
def add():
    try:
        add_file(
            request.args['dir'], request.files.getlist('files'))
        return seedir.seedir('./archive/%s' % request.args['dir'], printout=False, style='emoji')
    except Exception as e:
        return '%s' % str(e)


@app.route('/del', methods=['post'])
def delete():
    try:
        print(eval(request.args['files']))
        response = delete_file(
            request.args['dir'], eval(request.args['files']))
        return seedir.seedir('./archive/%s' % request.args['dir'], printout=False, style='emoji')
    except Exception as e:
        return '%s' % str(e)


@app.route('/archive', methods=['post'])
def archive():
    try:
        response = file_handle(request.files.getlist(
            'files'), request.args['dir'])
        return jsonify(response)
    except Exception as e:
        return '%s' % str(e)


@app.route('/destroy', methods=['post'])
def destroy():
    try:
        response = destory_archive(request.args['dir'])
        return jsonify(response)
    except Exception as e:
        return '%s' % str(e)


@app.route('/log', methods=['get'])
def log():
    try:
        return seedir.seedir('./archive/%s' % request.args['dir'], printout=False, style='emoji')
    except Exception as e:
        return '%s' % str(e)


@app.route('/fetch', methods=['get'])
def fetch():
    try:
        b64_map = fetch_file(request.args['dir'], eval(request.args['files']))
        return jsonify(b64_map)
    except Exception as e:
        return '%s' % str(e)


@app.route('/restore', methods=['get'])
def restore():
    try:
        target_dir = request.args['dir']
        response = restore_archive(target_dir)
        return jsonify(response)
    except Exception as e:
        return '%s' % str(e)


@func_timeout.func_set_timeout(60*15)
def run():
    app.run(host='0.0.0.0', port=1080)


try:
    run()
except:
    os.system('python3.8 '+sys.argv[0])
