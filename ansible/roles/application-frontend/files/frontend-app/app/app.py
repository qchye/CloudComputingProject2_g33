import controller
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory

app = Flask(__name__, static_url_path='')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Index
@app.route('/')
def index():
    filepath = controller.GetLocalGig()
    return render_template('home.html', path=filepath)

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
            filepath = controller.CombinePlot()
            return render_template('sentiment.html')
        if id == "rohan":
            return render_template('about.html')
        if id == "alvin":
            return render_template('state_sentiment_pop.html')


# Sentiment vs Elderly Population
@app.route('/sentiment_pop', methods=['GET', 'POST'])
def sentimentPop():
    median_age_path = controller.GetMedAgePopulation()
    elderly_pop_path = controller.GetElderlyPopPercentage()
    keywords_with_data = controller.GetUsefulKeywords()

    if request.method == 'POST':
        selected = request.form['keyword']

        (keyword_sentiment_path, isHypothesisTrue, isTasNegative, isSANegative,
         lowestSentState, lowestSentValue) = controller.GetKeywordSentiment(selected)

        return render_template('state_sentiment_pop.html', median_age_path=median_age_path, elderly_pop_path=elderly_pop_path, keyword_sentiment_path=keyword_sentiment_path, keywords_with_data=keywords_with_data, isHypothesisTrue=isHypothesisTrue, isTasNegative=isTasNegative, isSANegative=isSANegative, lowestSentState=lowestSentState, lowestSentValue=lowestSentValue)

    return render_template('state_sentiment_pop.html', median_age_path=median_age_path, elderly_pop_path=elderly_pop_path, keywords_with_data=keywords_with_data)


# Getting css file
@app.route('/content/<path:path>')
def serve_css(path):
    return send_from_directory('content', path)

# Getting img file
@app.route('/img/<path:path>')
def serve_img(path):
    return send_from_directory('img', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
