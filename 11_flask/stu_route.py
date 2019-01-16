from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/user/<username>')
def user_index(username):
    return 'hello {}'.format(username)

@app.route('/post/<int:post_id>')
def post_index(post_id):
    return 'Post {}'.format(post_id)

@app.route('/courses/<coursename>')
def course_index(coursename):
    return 'Course: {}'.format(coursename)

if __name__ == '__main__':
    app.run()
