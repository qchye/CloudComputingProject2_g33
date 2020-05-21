from flask import Flask, render_template
import controller
import couchdb_requests

app = Flask(__name__)
# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stateCount')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

