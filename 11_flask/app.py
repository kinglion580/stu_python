from flask import Flask

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'a random string'
    })

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run()
