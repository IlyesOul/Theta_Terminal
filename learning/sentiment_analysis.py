import statistics
import requests as req
import json

def sentiment_decision(tickers):

    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={tickers}&apikey=9D3IEU1D8KMP3SN6'
    json_response = req.get(url).json()
    sentiment_scores = [json_response['feed'][i]['overall_sentiment_score'] for i in range(len(json_response['feed']))]
    avg_sentiment_score = statistics.mean(sentiment_scores)
    if avg_sentiment_score < .15:
        return "Low"
    elif .20 > avg_sentiment_score > .15:
        return "Good"
    elif avg_sentiment_score > .20:
        return "High"

