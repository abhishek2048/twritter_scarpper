from flask import Flask, jsonify, render_template
from twitter_scraper import scrape_twitter_trends
from pymongo import MongoClient

app = Flask(__name__)

# Configure MongoDB
client = MongoClient('mongodb+srv://Abhishek:DYvGt8z7jItKTnuL@abhishek.wcka65c.mongodb.net/twitter_trends.trends')
db = client.twitter_trends
collection = db.trends

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    scrape_twitter_trends()
    return "Scraping started!"

@app.route('/data')
def data():
    latest_record = collection.find_one(sort=[('_id', -1)])
    return jsonify(latest_record)

if __name__ == "__main__":
    app.run(debug=True)
