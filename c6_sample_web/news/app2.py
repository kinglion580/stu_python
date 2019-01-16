#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import os
import json
from flask import Flask
from flask import render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


class Files(object):

    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        result = {}
        for filename in os.path.abspath('../files'):
            with open('../' + filename) as f:
                result[filename[:-5]] = json.load(f)
        return result

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self, filename):
        return self._files.get(filename)


files = Files()


@app.route('/')
def index():
    return render_template('index.html', title_list=files.get_title_list())


@app.route('/files/<filename>')
def file(filename):
    file_item = files.get_by_filename(filename)
    if not file_item:
        abort(404)
    return render_template('file.html', file_item)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
