from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html',usernamexx=username)

@app.route('/post/<int:post_id>')
def post_index(post_id):
    return 'Post {}'.format(post_id)

@app.route('/course/<coursename>')
def course_index(coursename):
    return render_template('course_index.html',coursenamexx=coursename)

if __name__ == '__main__':
    app.run()
