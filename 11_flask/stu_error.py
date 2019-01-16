from flask import Flask
from flask import render_template,redirect,url_for
from flask import request, make_response, abort

app=Flask(__name__)

@app.route('/')
def index():
    usernamezz=request.cookies.get('usernameyy')
    return 'Hello {}'.format(usernamezz)

@app.route('/user/<username>')
def user_index(username):
    resp = make_response(render_template('user_index.html',usernamexx=username))
    resp.set_cookie('usernameyy',username)
    if username == 'invalid':
        abort(404)
    return resp

@app.route('/post/<int:post_id>')
def post_index(post_id):
    return 'Post {}'.format(post_id)

@app.route('/course/<coursename>')
def course_index(coursename):
    return 'Course: {}'.format(coursename)

@app.errorhandler(404)
#def not_found(error)
def not_found(xxx):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
