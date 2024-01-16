import unittest
from Criminalingo_sentimet_analyzer.app import app
from Criminalingo_sentimet_analyzer.joblib import load

class SentimentAnalysisTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.classifier = load('sentiment_model.joblib')

    def test_sentiment_analysis_prediction(self):
        tweet_text = 'This is a positive tweet.'
        response = self.app.post('/analyze', data={'tweet_text': tweet_text})
        prediction = response.data.decode('utf-8').split('<span>')[1].split('</span>')[0]
        self.assertEqual(prediction, self.classifier.classify(tweet_text.lower()))

if __name__ == '__main__':
    unittest.main()
