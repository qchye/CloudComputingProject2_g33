import controller
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory

app = Flask(__name__, static_url_path='')

# Index
@app.route('/')
def index():
    filepath = controller.GetLocalGig()
    return render_template('home.html',path=filepath)

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Scenario
@app.route('/scenario', methods=['GET', 'POST'])
def scenario():
    if request.method == 'POST':
        id = request.form['id']
        if id == "yun":
            return render_template('about.html')
        if id == "rohan":
            return render_template('about.html')
        if id == "alvin":
            return render_template('about.html')


#Getting css file
@app.route('/content/<path:path>')
def serve_css(path):
    return send_from_directory('content', path)

#Getting img file
@app.route('/img/<path:path>')
def serve_img(path):
    return send_from_directory('img', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


