from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#make an app instance
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
mongo = PyMongo(app)

'''Define the Routes'''

#index
@app.route('/')
def home():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    print(mars_data)
    mars.update({}, mars_data, upsert=True)
    print("saved!")
    return redirect("/", code=302)

#run the app
if __name__ == '__main__':
    app.run(debug=True)