from flask import Flask, jsonify, render_template
from twitter_scraper import scrape_twitter_trends
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure MongoDB using environment variable
MONGODB_URL = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URL)
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
