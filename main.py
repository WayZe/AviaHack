from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_name():
    return "IT IS HACKATON!!!"


@app.route('/something/')
def give_pass():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
