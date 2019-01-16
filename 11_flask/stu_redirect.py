from flask import Flask
from flask import render_template,redirect,url_for

app=Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('user_index',username='default'))

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html',usernamexx=username)

@app.route('/post/<int:post_id>')
def post_index(post_id):
    return 'Post {}'.format(post_id)

@app.route('/course/<coursename>')
def course_index(coursename):
    return 'Course: {}'.format(coursename)

if __name__ == '__main__':
    app.run()
