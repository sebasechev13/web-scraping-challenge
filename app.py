# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import mars_scrape

#################################################
# Flask Setup
#################################################
app = Flask(__name__,template_folder='docs')

#################################################
# PyMongo Connection Setup

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = mars_scrape.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return render_template("index.html", mars=mars)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)