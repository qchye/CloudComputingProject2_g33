from flask import Flask, render_template
import controller

app = Flask(__name__)
# Index
@app.route('/')
def index():
    return render_template('home.html',searched=False)

# About
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stateCount')
def stateCount():
    filepath = controller.GetLocalGig()

    return render_template('home.html', path=filepath, searched= True)

@app.route('/income_tweets')
def stateCount():
    filepath = controller.GetLocalGig()

    return render_template('home.html', path=filepath, searched= True)
# Scenario
@app.route('/scenario', methods=['GET', 'POST'])
def scenario():
    if request.method == 'POST':
        id = request.form['id']
        if id == "yun":
            return render_template('about.html')
        if id == "Mean Income vs Gig Economy Related Tweets":
            return render_template('income_tweet.html')
        if id == "Gig Economy Business Popularity":
            return render_template('tweet_pop.html')
        if id == "Unemployment vs Gig Economy Related Tweets":
            return render_template('unemp_tweet.html')
        if id == "alvin":
            return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

