from flask import Flask, render_template, request, session, redirect, url_for
import nltk
from wordcloud import STOPWORDS
import pandas as pd
from joblib import load
import csv


app = Flask(__name__)
app.secret_key = '12345'  # secret_key, session'ı güvenli hale getirir


# Veriyi yükleme işlemi
veri = pd.read_csv('sentiment.csv')
veri = veri[['text', 'sentiment']]

# Metin verilerini temizleme ve özellik çıkarma işlemleri
tweets = []
stopwords_set = set(STOPWORDS)

for index, row in veri.iterrows():
    words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
    words_cleaned = [word for word in words_filtered
                     if 'http' not in word
                     and not word.startswith('@')
                     and not word.startswith('#')
                     and word != 'RT']
    words_without_stopwords = [word for word in words_cleaned if word not in stopwords_set]
    tweets.append((words_cleaned, row.sentiment))

# Nötr duyguları çıkart
veri = veri[veri.sentiment != "Neutral"]

# Kelime özelliklerini çıkar
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    features = wordlist.keys()
    return features

w_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in w_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# Modeli kaydetme işlemi
model_filename = 'sentiment_model.joblib'

#load(model_filename)
classifier = load(model_filename)



# Define a route for the home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Geçersiz kullanıcı adı/parola. Lütfen tekrar deneyin.'

    return render_template('login.html')



# CSV dosyasından veriyi okuma
tweet_data = pd.read_csv('tweets.csv')

# DataFrame'i bir dizi sözlüğe dönüştürme
example_tweets = tweet_data.to_dict('records')



@app.route('/')
def home():
    # Read the "tweets.csv" file each time the home page is accessed
    tweet_data = pd.read_csv('tweets.csv')
    example_tweets = tweet_data.to_dict('records')
    return render_template('index.html', example_tweets=example_tweets)

@app.route('/delete_tweet', methods=['POST'])
def delete_tweet():
    try:
        tweet_text = request.json.get('tweet_text')
        
        # tweets.csv dosyasını oku
        df = pd.read_csv('tweets.csv')

        # tweets.csv dosyasındaki ilgili tweet satırını sil
        df = df[df['text'] != tweet_text]

        # Güncellenmiş tweets.csv dosyasını kaydet
        df.to_csv('tweets.csv', index=False)

        # Güncellenmiş tweets.csv dosyasını döndür
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/graph')
def show_graph():
    return render_template('graph.htm')

# Define a route for sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        tweet_text = request.form['tweet_text']
        words_filtered = [e.lower() for e in tweet_text.split() if len(e) >= 3]
        words_cleaned = [word for word in words_filtered
                         if 'http' not in word
                         and not word.startswith('@')
                         and not word.startswith('#')
                         and word != 'RT']
        words_without_stopwords = [word for word in words_cleaned if word not in stopwords_set]

        # Use the classifier to predict sentiment
        prediction = classifier.classify(extract_features(words_without_stopwords))

        # Save the user input and prediction to "tweets.csv"
        with open('tweets.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([tweet_text, prediction])

        return render_template('analysis.html', tweet=tweet_text, prediction=prediction)



if __name__ == '__main__':
    app.run(debug=True, port=3500)
