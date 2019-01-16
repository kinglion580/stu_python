from flask import Flask

app=Flask(__name__)
app.config.from_pyfile('./config.py')

@app.route('/')
def index():
    str = app.config['WORLD']
    return str

if __name__ == '__main__':
    app.run()

