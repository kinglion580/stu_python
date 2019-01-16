#!/usr/bin/env python3
# -*-coding:utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime
from pymongo import MongoClient


app = Flask(__name__)
app.config.update({
    'TEMPLATES_AUTO_RELOAD': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@localhost/kinglion3',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})

db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).kinglion2


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    @property
    def __file(self):
        return mongo.file.find_one({'_id': self.id})

    def add_tag(self, tag_name):
        mongo.file.update_one({'_id': self.id}, {
            '$addToSet': {'tag': tag_name}})
        return self.__file['tag']

    def remove_tag(self, tag_name):
        mongo.file.update_one({'_id': self.id}, {
            '$pull': {'tag': tag_name}})
        return self.__file['tag']

    @property
    def tags(self):
        return self.__file['tag']


@event.listens_for(File, 'after_insert')
def auto_create_mongodb_file(mapper, conn, file):
    mongo.file.insert_one({'_id': file.id})


@event.listens_for(File, 'after_delete')
def auto_delete_mongodb_file(mapper, conn, file):
    mongo.file.delete_one({'_id': file.id})


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    file = db.relationship('File')

    def __init__(self, name):
        self.name = name


def insert_datas():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(),
                 java, 'File Content-java is cool')
    file2 = File('Hello python', datetime.utcnow(),
                 python, 'File Content-python is cool')

    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)

    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())


@app.route('/files/<int:file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    db.create_all()
    if not Category.query.filter_by(name='Java').first():
        insert_datas()
    app.run()
