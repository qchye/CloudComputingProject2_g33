import controller
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory

app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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
    if request.method == 'POST' or request.method == 'GET':
        id = request.form['id']
        if id == "yun":
            filepath = controller.CombinePlot()
            return render_template('sentiment.html')
        if id == "Income vs Gig Economy Tweets":
            filepath = controller.get_income_tweet()
            return render_template('income_tweet.html', path=filepath)
        if id == "Gig Economy Business Popularity":
            filepath = controller.get_business_pop_location()
            fp2 = controller.get_business_popularity()
            return render_template('tweet_pop.html', vic_fp=filepath[0], nsw_fp=filepath[1],
            wa_fp=filepath[2], sa_fp=filepath[3], nt_fp=filepath[4], act_fp=filepath[5],
            qld_fp=filepath[6], tas_fp=filepath[7], overall=fp2)
        if id == "Unemployment vs Gig Economy Tweets":
            filepath = controller.get_unemployment_tweet()
            return render_template('unemp_tweet.html', unemp_year_state=filepath[0], unemp_year=filepath[1], tweet_year_state=filepath[2])
        if id == "alvin":
            median_age_path = controller.GetMedAgePopulation()
            elderly_pop_path = controller.GetElderlyPopPercentage()
            keywords_with_data = controller.GetUsefulKeywords()
            generated = False
            return render_template('state_sentiment_pop.html', median_age_path=median_age_path, elderly_pop_path=elderly_pop_path, keywords_with_data=keywords_with_data, generated=generated)

# Sentiment vs Elderly Population
@app.route('/sentiment_pop', methods=['GET', 'POST'])
def sentimentPop():
    if request.method == 'POST':
        median_age_path = controller.GetMedAgePopulation()
        elderly_pop_path = controller.GetElderlyPopPercentage()
        keywords_with_data = controller.GetUsefulKeywords()
        selected = request.form['keyword']
        generated = True

        (keyword_sentiment_path, isHypothesisTrue, isTasNegative, isSANegative,
         lowestSentState, lowestSentValue) = controller.GetKeywordSentiment(selected)

        return render_template('state_sentiment_pop.html', median_age_path=median_age_path, elderly_pop_path=elderly_pop_path,
         keyword_sentiment_path=keyword_sentiment_path, keywords_with_data=keywords_with_data, isHypothesisTrue=isHypothesisTrue, 
         isTasNegative=isTasNegative, isSANegative=isSANegative, lowestSentState=lowestSentState, lowestSentValue=lowestSentValue, generated=generated)

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


