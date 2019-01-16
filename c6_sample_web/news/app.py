#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import os
import json
from flask import Flask
from flask import render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    title_list = []
    for file in os.listdir('../files'):
        with open(os.path.join('../files/', file)) as j:
            data = json.load(j)
            title_list.append(data['title'])

    return render_template('index.html', title_list=title_list)


@app.route('/files/<filename>')
def file(filename):
    with open('../files/' + filename + '.json') as j:
        data = json.load(j)
        content = data['content']

    return render_template('file.html', content=content)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
